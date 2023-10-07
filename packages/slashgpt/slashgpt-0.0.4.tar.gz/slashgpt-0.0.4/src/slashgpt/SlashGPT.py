import json
import os
import platform
import re
from typing import Optional

from gtts import gTTS

try:
    from playsound import playsound
except ImportError:
    print("no playsound. pip install playsound")

from slashgpt.chat_config_with_manifests import ChatConfigWithManifests
from slashgpt.chat_session import ChatSession
from slashgpt.function.jupyter_runtime import PythonRuntime
from slashgpt.utils.help import LONG_HELP, ONELINE_HELP
from slashgpt.utils.print import print_bot, print_debug, print_error, print_function, print_info, print_warning
from slashgpt.utils.utils import InputStyle

if platform.system() == "Darwin":
    # So that input can handle Kanji & delete
    import readline  # noqa: F401


"""
utility functions for Main class
"""


def play_text(text, lang):
    audio_obj = gTTS(text=text, lang=lang, slow=False)
    audio_obj.save("./output/audio.mp3")
    try:
        playsound("./output/audio.mp3")
    except NameError:
        print("no playsound. pip install playsound")


"""
ChatSlashConfig is a singleton, which holds global states, including various secret keys and the list of manifests for SlashGPT app.
"""


class ChatSlashConfig(ChatConfigWithManifests):
    """
    A subclass of ChatConfigManifest, which maintains the audio flag.
    """

    def __init__(self, base_path: str, path_manifests: str, llm_models: Optional[dict] = None, llm_engine_configs: Optional[dict] = None):
        """
        Args:

            base_path (str): path to the "base" folder.
            path_manifests (str): path to the manifests folder (json or yaml)
            llm_models (dict, optional): collection of custom LLM model definitions
            llm_engine_configs (dict, optional): collection of custom LLM engine definitions
        """
        super().__init__(base_path, path_manifests, llm_models, llm_engine_configs)
        self.audio: Optional[str] = None
        """Flag indicating if the audio mode is on or not"""

    def __get_manifests_keys(self):
        return sorted(self.manifests.keys())

    def help_list(self):
        return (f"/{(key+'         ')[:12]} {self.manifests.get(key).get('title')}" for key in self.__get_manifests_keys())


"""
Main is a singleton, which process the input from the user and manage chat sessions.
"""


class SlashGPT:
    def __init__(self, config: ChatSlashConfig, manifests_manager, agent_name: str):
        self.config = config
        self.manifests_manager = manifests_manager
        self.llm_model = self.config.get_default_llm_model()
        self.session = ChatSession(self.config, default_llm_model=self.llm_model)
        self.exit = False
        self.runtime = PythonRuntime(self.config.base_path + "/output/notebooks")
        self.switch_session(agent_name)

    """
    switchSession terminate the current chat session and start a new.
    The key specifies the AI agent.
    """

    def switch_session(self, agent_name: str, intro: bool = True):
        if agent_name is None:
            self.session = ChatSession(self.config, default_llm_model=self.llm_model)
            return

        if self.config.has_manifest(agent_name):
            manifest = self.config.manifests.get(agent_name)
            self.session = ChatSession(self.config, default_llm_model=self.llm_model, manifest=manifest, agent_name=agent_name, intro=intro)
            if self.config.verbose:
                print_info(
                    f"Activating: {self.session.title()} (model={self.session.llm_model.name()}, temperature={self.session.temperature()}, max_token={self.session.llm_model.max_token()})"
                )
            else:
                print_info(f"Activating: {self.session.title()}")
            if self.session.manifest.get("notebook"):
                (result, _) = self.runtime.create_notebook(self.session.llm_model.name())
                print_info(f"Created a notebook: {result.get('notebook_name')}")

            if self.session.intro_message:
                print_bot(self.session.botname(), self.session.intro_message)
        else:
            print_error(f"Invalid slash command: {agent_name}")

    def parse_question(self, question: str):
        key = question[1:].strip()
        commands = re.split(r"\s+", key)
        return (key, commands)

    def detect_input_style(self, question: str):
        (key, commands) = self.parse_question(question)
        if len(question) == 0:
            return InputStyle.HELP
        elif key[:6] == "sample":
            return InputStyle.SAMPLE
        elif question[0] == "/":
            return InputStyle.SLASH
        else:
            return InputStyle.TALK

    def display_oneline_help(self):
        print(ONELINE_HELP)

    def process_sample(self, question: str):
        (key, commands) = self.parse_question(question)
        if commands[0] == "sample" and len(commands) > 1:
            sub_key = commands[1]
            sub_manifest_data = self.config.manifests.get(sub_key)
            if sub_manifest_data:
                sample = sub_manifest_data.get("sample")
                if sample:
                    print(f"\033[95m\033[1m{self.session.username()}: \033[95m\033[0m{sample}")
                    return sample
            else:
                agents = self.session.manifest.get("agents")
                if agents:
                    print("/sample {agent}: " + ", ".join(agents))
                else:
                    print_error(f"Error: No manifest named '{sub_key}'")
        elif commands[0] == "samples":
            samples = list(map(lambda x: f"/{x}: {self.session.manifest.get(x)}", self.session.manifest.samples()))
            print("\n".join(samples))
            return None
        elif key[:6] == "sample":
            sample = self.session.manifest.get(key)
            if sample:
                print(f"\033[95m\033[1m{self.session.username()}: \033[95m\033[0m{sample}")
                return sample
            print_error(f"Error: No {key} in the manifest file")
        return None

    """
    If the question start with "/", process it as a Slash command.
    Otherwise, return (roleInput, question) as is.
    Notice that some Slash commands returns (role, question) as well.
    """

    def process_slash(self, question: str):
        (key, commands) = self.parse_question(question)
        if commands[0] == "help":
            if len(commands) == 1:
                print(LONG_HELP)
                list = "\n".join(self.config.help_list())
                print(f"Agents:\n{list}")
            if len(commands) == 2:
                manifest_data = self.config.manifests.get(commands[1])
                if manifest_data:
                    print(json.dumps(manifest_data, indent=2, ensure_ascii=False))
        elif key == "bye":
            self.runtime.stop()
            self.exit = True
        elif key == "verbose" or key == "v":
            self.config.verbose = not self.config.verbose
            print_debug(f"Verbose Mode: {self.config.verbose}")
        elif commands[0] == "audio":
            if len(commands) == 1:
                self.config.audio = None if self.config.audio else "en"
            elif commands[1] == "off":
                self.config.audio = None if commands[1] == "off" else commands[1]
            print(f"Audio mode: {self.config.audio}")
        elif key == "prompt":
            if self.session.history.len() >= 1:
                print(self.session.history.get_data(0, "content"))
            if self.config.verbose and self.session.functions:
                print_debug(self.session.functions)
        elif commands[0] == "history":
            if len(commands) == 1:
                print(json.dumps(self.session.history.messages(), ensure_ascii=False, indent=2))
                print(json.dumps(self.session.history.preset_messages(), ensure_ascii=False, indent=2))
            elif len(commands) > 1 and commands[1] == "pop":
                self.session.history.pop()
        elif key == "functions":
            if self.session.functions:
                print(json.dumps(self.session.functions, indent=2))
        elif key == "manifest":
            print(json.dumps(self.session.manifest.manifest(), indent=2))
        elif commands[0] == "llm" or commands[0] == "llms":
            if len(commands) > 1 and self.config.llm_models and self.config.llm_models.get(commands[1]):
                self.llm_model = self.config.get_llm_model_from_key(commands[1])
                self.session.set_llm_model(self.llm_model)
            else:
                if self.config.llm_models is None:
                    raise RuntimeError("self.config.llm_models must be set")
                print("/llm: " + ",".join(self.config.llm_models.keys()))
        elif key == "current_llm":
            print(self.session.llm_model.name())
        elif key == "new":
            self.switch_session(self.session.agent_name, intro=False)
        elif commands[0] == "autotest":
            self.auto_test(commands)
        elif commands[0] == "switch":
            if len(commands) > 1 and self.manifests_manager.get(commands[1]):
                self.switch_manifests(commands[1])
            else:
                print("/switch {manifest}: " + ", ".join(self.manifests_manager.keys()))
        elif commands[0] == "import":
            self.import_data(commands)
        elif commands[0] == "reload":
            self.config.reload()
        elif self.config.has_manifest(commands[0]):
            messages = self.session.history.nonpreset_messages()  # for "-chain" option
            self.switch_session(commands[0])
            if len(commands) > 1 and commands[1] == "-chain":
                if self.config.verbose:
                    print_debug(f"Chaining {len(messages)} messages")
                for m in messages:
                    self.session.history.append_message(m.get("role"), m.get("content"), m.get("name"), False)

        else:
            print_error(f"Invalid slash command: {key}")

    def auto_test(self, commands):
        file_name = commands[1] if len(commands) > 1 else "default"
        file_path = f"{self.config.base_path}/test/{file_name}.json"
        if not os.path.exists(file_path):
            print_warning(f"No test script named {file_name}")
            return
        self.config.verbose = True
        with open(file_path, "r") as f:
            scripts = json.load(f)
            self.switch_manifests(scripts.get("manifests") or "main")
            for message in scripts.get("messages"):
                self.test(**message)
        self.config.verbose = False

    def import_data(self, commands):
        if len(commands) == 1:
            files = self.session.history.session_list()
            for file in files:
                print(str(file["id"]) + ": " + file["name"])
            return
        else:
            log = self.session.history.get_session_data(commands[1])
            if log:
                if len(commands) == 2:
                    self.session.history.restore(log)
                    print("imported")
                    return
                if len(commands) == 3 and commands[2] == "show":
                    print(json.dumps(log, indent=2, ensure_ascii=False))
                    return

        print("/import: list all histories")
        print("/import {num}: import history")
        print("/import {num} show: show history")

    def switch_manifests(self, key):
        m = self.manifests_manager[key]
        self.config.switch_manifests(self.config.base_path + "/" + m["manifests_dir"])
        self.switch_session(m["default_agent_name"])

    def test(self, agent, message=None, messages=None):
        self.switch_session(agent)
        if message:
            print(f"\033[95m\033[1m{self.session.username()}: \033[95m\033[0m{message}")
            self.talk(message)
        if messages:
            for m in messages:
                print(f"\033[95m\033[1m{self.session.username()}: \033[95m\033[0m{m}")
                self.talk(m)

    def process_llm(self):
        try:
            # Ask LLM to generate a response.
            (res, function_call) = self.session.call_llm()

            if res:
                print_bot(self.session.botname(), res)

                if self.config.audio:
                    play_text(res, self.config.audio)

            if function_call:
                (action_data, action_method) = function_call.emit_data(self.config.verbose)
                if action_method:
                    # All emit methods must be processed here
                    if action_method == "switch_session":
                        self.switch_session(action_data.get("manifest"), intro=False)
                        self.query_llm(action_data.get("message"))
                else:
                    (
                        function_message,
                        function_name,
                        should_call_llm,
                    ) = function_call.process_function_call(
                        self.session.history,
                        self.runtime,
                        self.config.verbose,
                    )
                    if function_message:
                        print_function(function_name, function_message)

                    if should_call_llm:
                        self.process_llm()

        except Exception as e:
            print_error(f"Exception: Restarting the chat :{e}")
            self.switch_session(self.session.agent_name)
            if self.config.verbose:
                raise

    """
    the main loop
    """

    def start(self):
        while not self.exit:
            self.input_and_talk()

    def input_and_talk(self):
        try:
            self.talk(input(f"\033[95m\033[1m{self.session.username()}: \033[95m\033[0m").strip())
        except KeyboardInterrupt:
            self.exit = True
            print("bye")
        except EOFError:
            self.exit = True
            print("bye")

    def talk(self, question):
        mode = self.detect_input_style(question)
        if mode == InputStyle.HELP:
            self.display_oneline_help()
        elif mode == InputStyle.SLASH:
            self.process_slash(question)
        else:
            if mode == InputStyle.SAMPLE:
                question = self.process_sample(question)
            if question:
                if isinstance(question, list):
                    for q in question:
                        self.query_llm(self.session.manifest.format_question(q))
                else:
                    self.query_llm(self.session.manifest.format_question(question))

    def query_llm(self, question):
        self.session.append_user_question(question)
        self.process_llm()
