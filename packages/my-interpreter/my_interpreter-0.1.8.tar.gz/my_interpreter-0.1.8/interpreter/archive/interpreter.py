"""
Right off the bat, to any contributors (a message from Killian):

First of all, THANK YOU. Open Interpreter is ALIVE, ALL OVER THE WORLD because of YOU.

While this project is rapidly growing, I've decided it's best for us to allow some technical debt.

The code here has duplication. It has imports in weird places. It has been spaghettified to add features more quickly.

In my opinion **this is critical** to keep up with the pace of demand for this project.

At the same time, I plan on pushing a significant re-factor of `interpreter.py` and `code_interpreter.py` ~ September 21st.

After the re-factor, Open Interpreter's source code will be much simpler, and much more fun to dive into.

Especially if you have ideas and **EXCITEMENT** about the future of this project, chat with me on discord: https://discord.gg/6p3fD6rBVm

- killian
"""

from .cli import cli
from .utils import merge_deltas, parse_partial_json
from .message_block import MessageBlock
from .code_block import CodeBlock
from .code_interpreter import CodeInterpreter
from .get_hf_llm import get_hf_llm
from openai.error import RateLimitError 

import os
import time
import traceback
import json
import platform
import openai
import litellm
import pkg_resources
import uuid

import getpass
import requests
import tokentrim as tt
from rich import print
from rich.markdown import Markdown
from rich.rule import Rule

try:
  import readline
except:
  # Sometimes this doesn't work (https://stackoverflow.com/questions/10313765/simple-swig-python-example-in-vs2008-import-error-internal-pyreadline-erro)
  pass

# Function schema for gpt-4
function_schema = {
  "name": "run_code",
  "description":
  "Executes code on the user's machine and returns the output",
  "parameters": {
    "type": "object",
    "properties": {
      "language": {
        "type": "string",
        "description":
        "The programming language",
        "enum": ["python", "R", "shell", "applescript", "javascript", "html"]
      },
      "code": {
        "type": "string",
        "description": "The code to execute"
      }
    },
    "required": ["language", "code"]
  },
}

# Message for when users don't have an OpenAI API key.
missing_api_key_message = """> 未找到 OpenAI API 密钥

要使用“GPT-4”（推荐），请提供 OpenAI API 密钥。

要使用“Code-Llama”（免费但功能较弱），请按“enter”。
"""

# Message for when users don't have an OpenAI API key.
missing_azure_info_message = """> 找不到 Azure OpenAI 服务 API 信息

要使用“GPT-4”（推荐），请提供 Azure OpenAI API 密钥、API 基础、部署名称和 API 版本。

要使用“Code-Llama”（免费但功能较弱），请按“enter”。
"""

confirm_mode_message = """
**My Interpreter** 在运行代码之前需要你的回复y批准,可使用“my-interpreter -y”来绕过这个要求。

按“CTRL-C”退出。
"""

# Create an API Budget to prevent high spend


class Interpreter:

  def __init__(self):
    self.messages = []
    self.temperature = 0.001
    self.api_key = None
    self.auto_run = False
    self.local = False
    self.model = "gpt-4"
    self.debug_mode = False
    self.api_base = None # Will set it to whatever OpenAI wants
    self.context_window = 2000 # For local models only
    self.max_tokens = 750 # For local models only
    # Azure OpenAI
    self.use_azure = False
    self.azure_api_base = None
    self.azure_api_version = None
    self.azure_deployment_name = None
    self.azure_api_type = "azure"
    
    # Get default system message
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'system_message.txt'), 'r') as f:
      self.system_message = f.read().strip()

    # Store Code Interpreter instances for each language
    self.code_interpreters = {}

    # No active block to start
    # (blocks are visual representation of messages on the terminal)
    self.active_block = None

    # Note: While Open Interpreter can use Llama, we will prioritize gpt-4.
    # gpt-4 is faster, smarter, can call functions, and is all-around easier to use.
    # This makes gpt-4 better aligned with Open Interpreters priority to be easy to use.
    self.llama_instance = None

  def cli(self):
    # The cli takes the current instance of Interpreter,
    # modifies it according to command line flags, then runs chat.
    cli(self)

  def get_info_for_system_message(self):
    """
    获取系统消息的相关信息。
    """

    info = ""

    # Add user info
    username = getpass.getuser()
    current_working_directory = os.getcwd()
    operating_system = platform.system()

    info += f"[User Info]\nName: {username}\nCWD: {current_working_directory}\nOS: {operating_system}"

    if not self.local:

      # Open Procedures is an open-source database of tiny, up-to-date coding tutorials.
      # We can query it semantically and append relevant tutorials/procedures to our system message:

      # Use the last two messages' content or function call to semantically search
      query = []
      for message in self.messages[-2:]:
        message_for_semantic_search = {"role": message["role"]}
        if "content" in message:
          message_for_semantic_search["content"] = message["content"]
        if "function_call" in message and "parsed_arguments" in message["function_call"]:
          message_for_semantic_search["function_call"] = message["function_call"]["parsed_arguments"]
        query.append(message_for_semantic_search)

      # Use them to query Open Procedures
      url = "https://open-procedures.replit.app/search/"

      try:
        relevant_procedures = requests.get(url, data=json.dumps(query)).json()["procedures"]
        info += "\n\n# 推荐程序\n" + "\n---\n".join(relevant_procedures) + "\n在您的计划中，包括步骤，如果存在，**确切的代码片段**（特别是对于弃用）请注意，**将它们写入您的计划 - 在每个编号的步骤下方**，因为一旦您执行第一行代码，它们就会消失，所以如果您需要它们，请立即将它们写下来）从上述过程中，如果它们与任务。再次强调，如果上述过程中的**逐字代码片段**与任务相关，请直接将其包含在您的计划中。**"
      except:
        # For someone, this failed for a super secure SSL reason.
        # Since it's not stricly necessary, let's worry about that another day. Should probably log this somehow though.
        pass

    elif self.local:

      # Tell Code-Llama how to run code.
      info += "\n\n要运行代码，请在 markdown 中编写受保护的代码块（即 ```python、R 或 ```shell）。当你用```关闭它时，它就会运行。然后你会得到它的输出。"
      # We make references in system_message.txt to the "function" it can call, "run_code".

    return info

  def reset(self):
    """
    Resets the interpreter.
    """
    self.messages = []
    self.code_interpreters = {}

  def load(self, messages):
    self.messages = messages


  def handle_undo(self, arguments):
    # Removes all messages after the most recent user entry (and the entry itself).
    # Therefore user can jump back to the latest point of conversation.
    # Also gives a visual representation of the messages removed.

    if len(self.messages) == 0:
      return
    # Find the index of the last 'role': 'user' entry
    last_user_index = None
    for i, message in enumerate(self.messages):
        if message.get('role') == 'user':
            last_user_index = i

    removed_messages = []

    # Remove all messages after the last 'role': 'user'
    if last_user_index is not None:
        removed_messages = self.messages[last_user_index:]
        self.messages = self.messages[:last_user_index]

    print("") # Aesthetics.

    # Print out a preview of what messages were removed.
    for message in removed_messages:
      if 'content' in message and message['content'] != None:
        print(Markdown(f"**已删除的消息:** `\"{message['content'][:30]}...\"`"))
      elif 'function_call' in message:
        print(Markdown(f"**删除了代码块:**")) # TODO: Could add preview of code removed here.
    
    print("") # Aesthetics.

  def handle_help(self, arguments):
    commands_description = {
      "%debug [true/false]": "切换调试模式。不带参数或使用 'true' 时，将进入调试模式。使用 'false' 时，将退出调试模式。",
      "%reset": "重置当前会话。",
      "%undo": "从消息历史记录中删除以前的消息及其响应。",
      "%save_message [path]": "将消息保存到指定的 JSON 路径。如果未提供路径，则默认为 'messages.json'。",
      "%load_message [path]": "从指定的 JSON 路径加载消息。如果未提供路径，则默认为 'messages.json'。",
      "%help": "显示此帮助消息。",
    }

    base_message = [
      "> **可用命令：**\n\n"
    ]

    # Add each command and its description to the message
    for cmd, desc in commands_description.items():
      base_message.append(f"- `{cmd}`: {desc}\n")

    additional_info = [
      "\n\n如需进一步帮助，请加入我们的 Discord 社区或考虑为该项目的开发做出贡献。"
    ]

    # Combine the base message with the additional info
    full_message = base_message + additional_info

    print(Markdown("".join(full_message)))


  def handle_debug(self, arguments=None):
    if arguments == "" or arguments == "true":
        print(Markdown("> 进入调试模式"))
        print(self.messages)
        self.debug_mode = True
    elif arguments == "false":
        print(Markdown("> 退出调试模式"))
        self.debug_mode = False
    else:
        print(Markdown("> 调试命令的未知参数。"))

  def handle_reset(self, arguments):
    self.reset()
    print(Markdown("> 重置完成"))

  def default_handle(self, arguments):
    print(Markdown("> 未知的命令"))
    self.handle_help(arguments)

  def handle_save_message(self, json_path):
    if json_path == "":
      json_path = "messages.json"
    if not json_path.endswith(".json"):
      json_path += ".json"
    with open(json_path, 'w') as f:
      json.dump(self.messages, f, indent=2)

    print(Markdown(f"> 消息 json 导出到 {os.path.abspath(json_path)}"))

  def handle_load_message(self, json_path):
    if json_path == "":
      json_path = "messages.json"
    if not json_path.endswith(".json"):
      json_path += ".json"
    if os.path.exists(json_path):
      with open(json_path, 'r') as f:
        self.load(json.load(f))
      print(Markdown(f"> 消息 json 加载自 {os.path.abspath(json_path)}"))
    else:
      print(Markdown("未找到文件，请检查路径并重试。"))


  def handle_command(self, user_input):
    # split the command into the command and the arguments, by the first whitespace
    switch = {
      "help": self.handle_help,
      "debug": self.handle_debug,
      "reset": self.handle_reset,
      "save_message": self.handle_save_message,
      "load_message": self.handle_load_message,
      "undo": self.handle_undo,
    }

    user_input = user_input[1:].strip()  # Capture the part after the `%`
    command = user_input.split(" ")[0]
    arguments = user_input[len(command):].strip()
    action = switch.get(command,
                        self.default_handle)  # Get the function from the dictionary, or default_handle if not found
    action(arguments)  # Execute the function

  def chat(self, message=None, return_messages=False):

    # Connect to an LLM (an large language model)
    if not self.local:
      # gpt-4
      self.verify_api_key()

    # ^ verify_api_key may set self.local to True, so we run this as an 'if', not 'elif':
    if self.local:

      # Code-Llama
      if self.llama_instance == None:

        # Find or install Code-Llama
        try:
          self.llama_instance = get_hf_llm(self.model, self.debug_mode, self.context_window)
          if self.llama_instance == None:
            # They cancelled.
            return
        except:
          traceback.print_exc()
          # If it didn't work, apologize and switch to GPT-4

          print(Markdown("".join([
            f"> 无法安装 `{self.model}`。",
            f"\n\n**常见修复：** 您可以按照下面链接中的简单设置文档来解决常见错误。\n\n```\nhttps://github.com/KillianLucas/open-interpreter /tree/main/docs\n```",
            f"\n\n**如果您已经尝试过，但仍然收到错误，我们可能没有为您的系统构建正确的 `{self.model}` 支持。**",
            "\n\n*( 在本地运行语言模型是一项艰巨的任务！*如果您了解跨平台/架构实现这一点的最佳方法，请加入 Open Interpreter 社区 Discord 并考虑为项目的开发做出贡献。)",
            "\n\n按 Enter 键切换到‘GPT-4’（推荐）。"
          ])))
          input()

          # Switch to GPT-4
          self.local = False
          self.model = "gpt-4"
          self.verify_api_key()

    # Display welcome message
    welcome_message = ""

    if self.debug_mode:
      welcome_message += "> 进入调试模式"

      

    # If self.local, we actually don't use self.model
    # (self.auto_run is like advanced usage, we display no messages)
    if not self.local and not self.auto_run:

      if self.use_azure:
        notice_model = f"{self.azure_deployment_name} (Azure)"
      else:
        notice_model = f"{self.model.upper()}"
      welcome_message += f"\n> 模型设置: `{notice_model}`\n\n**提示：**要在本地运行，请使用 `interpreter --local`"
      
    if self.local:
      welcome_message += f"\n> 模型设置: `{self.model}`"

    # If not auto_run, tell the user we'll ask permission to run code
    # We also tell them here how to exit Open Interpreter
    if not self.auto_run:
      welcome_message += "\n\n" + confirm_mode_message

    welcome_message = welcome_message.strip()

    # Print welcome message with newlines on either side (aesthetic choice)
    # unless we're starting with a blockquote (aesthetic choice)
    if welcome_message != "":
      if welcome_message.startswith(">"):
        print(Markdown(welcome_message), '')
      else:
        print('', Markdown(welcome_message), '')

    # Check if `message` was passed in by user
    if message:
      print(f"user message: {message}")
      # If it was, we respond non-interactivley
      self.messages.append({"role": "user", "content": message})
      self.respond()

    else:
      # If it wasn't, we start an interactive chat
      while True:
        try:
          user_input = input("> ").strip()
        except EOFError:
          break
        except KeyboardInterrupt:
          print()  # Aesthetic choice
          break

        # Use `readline` to let users up-arrow to previous user messages,
        # which is a common behavior in terminals.
        try:
          readline.add_history(user_input)
        except:
          # Sometimes this doesn't work (https://stackoverflow.com/questions/10313765/simple-swig-python-example-in-vs2008-import-error-internal-pyreadline-erro)
          pass

        # If the user input starts with a `%`
        if user_input.startswith("%"):
          self.handle_command(user_input)
          continue

        # Add the user message to self.messages
        self.messages.append({"role": "user", "content": user_input})

        # Respond, but gracefully handle CTRL-C / KeyboardInterrupt
        try:
          self.respond()
        except KeyboardInterrupt:
          pass
        finally:
          # Always end the active block. Multiple Live displays = issues
          self.end_active_block()

    if return_messages:
        return self.messages

  def verify_api_key(self):
    """
    确保我们有 AZURE_API_KEY 或 OPENAI_API_KEY。
    """
    if self.use_azure:
      all_env_available = (
        ('AZURE_API_KEY' in os.environ or 'OPENAI_API_KEY' in os.environ) and
        'AZURE_API_BASE' in os.environ and
        'AZURE_API_VERSION' in os.environ and
        'AZURE_DEPLOYMENT_NAME' in os.environ)
      if all_env_available:
        self.api_key = os.environ.get('AZURE_API_KEY') or os.environ['OPENAI_API_KEY']
        self.azure_api_base = os.environ['AZURE_API_BASE']
        self.azure_api_version = os.environ['AZURE_API_VERSION']
        self.azure_deployment_name = os.environ['AZURE_DEPLOYMENT_NAME']
        self.azure_api_type = os.environ.get('AZURE_API_TYPE', 'azure')
      else:
        # This is probably their first time here!
        self._print_welcome_message()
        time.sleep(1)

        print(Rule(style="white"))

        print(Markdown(missing_azure_info_message), '', Rule(style="white"), '')
        response = input("Azure OpenAI API key: ")

        if response == "":
          # User pressed `enter`, requesting Code-Llama

          print(Markdown(
            "> 切换到 `Code-Llama`...\n\n**提示：** 运行 `my-interpreter --local` 自动使用 `Code-Llama`。"),
                '')
          time.sleep(2)
          print(Rule(style="white"))



          # Temporarily, for backwards (behavioral) compatability, we've moved this part of llama_2.py here.
          # AND BELOW.
          # This way, when folks hit interpreter --local, they get the same experience as before.
          import inquirer

          print('', Markdown("**My Interpreter** 将使用 `Code Llama` 进行本地执行。使用箭头键设置模型。"), '')

          models = {
              '7B': 'TheBloke/CodeLlama-7B-Instruct-GGUF',
              '13B': 'TheBloke/CodeLlama-13B-Instruct-GGUF',
              '34B': 'TheBloke/CodeLlama-34B-Instruct-GGUF'
          }

          parameter_choices = list(models.keys())
          questions = [inquirer.List('param', message="参数数量（越小速度越快，越大能力越强）", choices=parameter_choices)]
          answers = inquirer.prompt(questions)
          chosen_param = answers['param']

          # THIS is more in line with the future. You just say the model you want by name:
          self.model = models[chosen_param]
          self.local = True




          return

        else:
          self.api_key = response
          self.azure_api_base = input("Azure OpenAI API base: ")
          self.azure_deployment_name = input("GPT 的 Azure OpenAI 部署名称: ")
          self.azure_api_version = input("Azure OpenAI API version: ")
          print('', Markdown(
            "**提示：** 要保存此密钥供以后使用，请在 Mac/Linux 上运行 `export AZURE_API_KEY=your_api_key AZURE_API_BASE=your_api_base AZURE_API_VERSION=your_api_version AZURE_DEPLOYMENT_NAME=your_gpt_deployment_name` 或在 Mac/Linux 上运行 `setx AZURE_API_KEY your_api_key AZURE_API_BASE your_api_base AZURE_API_VERSION Windows 上的 your_api_version AZURE_DEPLOYMENT_NAME your_gpt_deployment_name`。"),
                '')
          time.sleep(2)
          print(Rule(style="white"))

      litellm.api_type = self.azure_api_type
      litellm.api_base = self.azure_api_base
      litellm.api_version = self.azure_api_version
      litellm.api_key = self.api_key
    else:
      if self.api_key == None:
        if 'OPENAI_API_KEY' in os.environ:
          self.api_key = os.environ['OPENAI_API_KEY']
        else:
          # This is probably their first time here!
          self._print_welcome_message()
          time.sleep(1)

          print(Rule(style="white"))

          print(Markdown(missing_api_key_message), '', Rule(style="white"), '')
          response = input("OpenAI API key: ")

          if response == "":
              # User pressed `enter`, requesting Code-Llama

              print(Markdown(
                "> 切换到 `Code-Llama`...\n\n**提示：** 运行 `my-interpreter --local` 以自动使用 `Code-Llama`。"),
                    '')
              time.sleep(2)
              print(Rule(style="white"))



              # Temporarily, for backwards (behavioral) compatability, we've moved this part of llama_2.py here.
              # AND ABOVE.
              # This way, when folks hit interpreter --local, they get the same experience as before.
              import inquirer

              print('', Markdown("**My Interpreter** 将使用 `Code Llama` 进行本地执行。使用箭头键设置模型。"), '')

              models = {
                  '7B': 'TheBloke/CodeLlama-7B-Instruct-GGUF',
                  '13B': 'TheBloke/CodeLlama-13B-Instruct-GGUF',
                  '34B': 'TheBloke/CodeLlama-34B-Instruct-GGUF'
              }

              parameter_choices = list(models.keys())
              questions = [inquirer.List('param', message="参数数量（越小速度越快，越大能力越强）", choices=parameter_choices)]
              answers = inquirer.prompt(questions)
              chosen_param = answers['param']

              # THIS is more in line with the future. You just say the model you want by name:
              self.model = models[chosen_param]
              self.local = True




              return

          else:
              self.api_key = response
              print('', Markdown("**提示：** 要保存此密钥供以后使用，请在 Mac/Linux 上运行 `export OPENAI_API_KEY=your_api_key` 或在 Windows 上运行 `setx OPENAI_API_KEY your_api_key`。"), '')
              time.sleep(2)
              print(Rule(style="white"))

      litellm.api_key = self.api_key
      if self.api_base:
        litellm.api_base = self.api_base

  def end_active_block(self):
    if self.active_block:
      self.active_block.end()
      self.active_block = None

  def respond(self):
    # Add relevant info to system_message
    # (e.g. current working directory, username, os, etc.)
    info = self.get_info_for_system_message()

    # This is hacky, as we should have a different (minified) prompt for CodeLLama,
    # but for now, to make the prompt shorter and remove "run_code" references, just get the first 2 lines:
    if self.local:
      self.system_message = "\n".join(self.system_message.split("\n")[:2])
      self.system_message += "\n只做用户要求你做的事情，然后询问他们下一步想做什么。"

    system_message = self.system_message + "\n\n" + info

    if self.local:
      messages = tt.trim(self.messages, max_tokens=(self.context_window-self.max_tokens-25), system_message=system_message)
    else:
      messages = tt.trim(self.messages, self.model, system_message=system_message)

    if self.debug_mode:
      print("\n", "向 LLM 发送“消息”:", "\n")
      print(messages)
      print()

    # Make LLM call
    if not self.local:
      
      # GPT
      max_attempts = 3  
      attempts = 0  
      error = ""

      while attempts < max_attempts:
        attempts += 1
        try:

            if self.use_azure:
              response = litellm.completion(
                  f"azure/{self.azure_deployment_name}",
                  messages=messages,
                  functions=[function_schema],
                  temperature=self.temperature,
                  stream=True,
                  )
            else:
              if self.api_base:
                # The user set the api_base. litellm needs this to be "custom/{model}"
                response = litellm.completion(
                  api_base=self.api_base,
                  model = "custom/" + self.model,
                  messages=messages,
                  functions=[function_schema],
                  stream=True,
                  temperature=self.temperature,
                )
              else:
                # Normal OpenAI call
                response = litellm.completion(
                  model=self.model,
                  messages=messages,
                  functions=[function_schema],
                  stream=True,
                  temperature=self.temperature,
                )
            break
        except litellm.BudgetExceededError as e:
          print(f"由于超出了您的 LLM API 预算限制，因此您将转为本地模型。预算：{litellm.max_budget} |当前成本：{litellm._current_cost}")
          
          print(Markdown(
                "> 切换到 `Code-Llama`...\n\n**提示：** 运行 `my-interpreter --local` 以自动使用 `Code-Llama`。"),
                    '')
          time.sleep(2)
          print(Rule(style="white"))



          # Temporarily, for backwards (behavioral) compatability, we've moved this part of llama_2.py here.
          # AND ABOVE.
          # This way, when folks hit interpreter --local, they get the same experience as before.
          import inquirer

          print('', Markdown("**My Interpreter** 将使用 `Code Llama` 进行本地执行。使用箭头键设置模型。"), '')

          models = {
              '7B': 'TheBloke/CodeLlama-7B-Instruct-GGUF',
              '13B': 'TheBloke/CodeLlama-13B-Instruct-GGUF',
              '34B': 'TheBloke/CodeLlama-34B-Instruct-GGUF'
          }

          parameter_choices = list(models.keys())
          questions = [inquirer.List('param', message="参数数量（越小速度越快，越大能力越强）", choices=parameter_choices)]
          answers = inquirer.prompt(questions)
          chosen_param = answers['param']

          # THIS is more in line with the future. You just say the model you want by name:
          self.model = models[chosen_param]
          self.local = True
          continue
        except RateLimitError as rate_error:  # Catch the specific RateLimitError
            print(Markdown(f"> 我们达到了速率限制。冷却 {attempts} 秒..."))
            time.sleep(attempts)  
            max_attempts += 1
        except Exception as e:  # Catch other exceptions
            if self.debug_mode:
              traceback.print_exc()
            error = traceback.format_exc()
            time.sleep(3)
      else:
        if self.local: 
          pass
        else:
          raise Exception(error)
            
    if self.local:
      # Code-Llama



      # Convert messages to prompt
      # (This only works if the first message is the only system message)

      def messages_to_prompt(messages):


        for message in messages:
          # Happens if it immediatly writes code
          if "role" not in message:
            message["role"] = "assistant"


        # Falcon prompt template
        if "falcon" in self.model.lower():

          formatted_messages = ""
          for message in messages:
            formatted_messages += f"{message['role'].capitalize()}: {message['content']}\n"
          formatted_messages = formatted_messages.strip()

        else:
          # Llama prompt template

          # Extracting the system prompt and initializing the formatted string with it.
          system_prompt = messages[0]['content']
          formatted_messages = f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n"

          # Loop starting from the first user message
          for index, item in enumerate(messages[1:]):
              role = item['role']
              content = item['content']

              if role == 'user':
                  formatted_messages += f"{content} [/INST] "
              elif role == 'function':
                  formatted_messages += f"Output: {content} [/INST] "
              elif role == 'assistant':
                  formatted_messages += f"{content} </s><s>[INST] "

          # Remove the trailing '<s>[INST] ' from the final output
          if formatted_messages.endswith("<s>[INST] "):
              formatted_messages = formatted_messages[:-10]

        return formatted_messages

      prompt = messages_to_prompt(messages)
      # Lmao i can't believe this works (it does need this btw)
      if messages[-1]["role"] != "function":
        prompt += "让我们来探讨一下。顺便说一下，我可以通过在 markdown 代码块中编写代码来在您的机器上运行代码。这适用于 shell、javascript、python、R 和 applescript。我将尝试为您的任务做到这一点。反正， "
      elif messages[-1]["role"] == "function" and messages[-1]["content"] != "No output":
        prompt += "鉴于我刚刚运行的代码的输出， "
      elif messages[-1]["role"] == "function" and messages[-1]["content"] == "No output":
        prompt += "鉴于我刚刚运行的代码没有产生输出, "


      if self.debug_mode:
        # we have to use builtins bizarrely! because rich.print interprets "[INST]" as something meaningful
        import builtins
        builtins.print("文本提示发送至 LLM:\n", prompt)

      # Run Code-Llama

      response = self.llama_instance(
        prompt,
        stream=True,
        temperature=self.temperature,
        stop=["</s>"],
        max_tokens=750 # context window is set to 1800, messages are trimmed to 1000... 700 seems nice
      )

    # Initialize message, function call trackers, and active block
    self.messages.append({})
    in_function_call = False
    llama_function_call_finished = False
    self.active_block = None

    for chunk in response:
      if self.use_azure and ('choices' not in chunk or len(chunk['choices']) == 0):
        # Azure OpenAI Service may return empty chunk
        continue

      if self.local:
        if "content" not in messages[-1]:
          # This is the first chunk. We'll need to capitalize it, because our prompt ends in a ", "
          chunk["choices"][0]["text"] = chunk["choices"][0]["text"].capitalize()
          # We'll also need to add "role: assistant", CodeLlama will not generate this
          messages[-1]["role"] = "assistant"
        delta = {"content": chunk["choices"][0]["text"]}
      else:
        delta = chunk["choices"][0]["delta"]

      # Accumulate deltas into the last message in messages
      self.messages[-1] = merge_deltas(self.messages[-1], delta)

      # Check if we're in a function call
      if not self.local:
        condition = "function_call" in self.messages[-1]
      elif self.local:
        # Since Code-Llama can't call functions, we just check if we're in a code block.
        # This simply returns true if the number of "```" in the message is odd.
        if "content" in self.messages[-1]:
          condition = self.messages[-1]["content"].count("```") % 2 == 1
        else:
          # If it hasn't made "content" yet, we're certainly not in a function call.
          condition = False

      if condition:
        # We are in a function call.

        # Check if we just entered a function call
        if in_function_call == False:

          # If so, end the last block,
          self.end_active_block()

          # Print newline if it was just a code block or user message
          # (this just looks nice)
          last_role = self.messages[-2]["role"]
          if last_role == "user" or last_role == "function":
            print()

          # then create a new code block
          self.active_block = CodeBlock()

        # Remember we're in a function_call
        in_function_call = True

        # Now let's parse the function's arguments:

        if not self.local:
          # gpt-4
          # Parse arguments and save to parsed_arguments, under function_call
          if "arguments" in self.messages[-1]["function_call"]:
            arguments = self.messages[-1]["function_call"]["arguments"]
            new_parsed_arguments = parse_partial_json(arguments)
            if new_parsed_arguments:
              # Only overwrite what we have if it's not None (which means it failed to parse)
              self.messages[-1]["function_call"][
                "parsed_arguments"] = new_parsed_arguments

        elif self.local:
          # Code-Llama
          # Parse current code block and save to parsed_arguments, under function_call
          if "content" in self.messages[-1]:

            content = self.messages[-1]["content"]

            if "```" in content:
              # Split by "```" to get the last open code block
              blocks = content.split("```")

              current_code_block = blocks[-1]

              lines = current_code_block.split("\n")

              if content.strip() == "```": # Hasn't outputted a language yet
                language = None
              else:
                if lines[0] != "":
                  language = lines[0].strip()
                else:
                  language = "python"
                  # In anticipation of its dumbassery let's check if "pip" is in there
                  if len(lines) > 1:
                    if lines[1].startswith("pip"):
                      language = "shell"

              # Join all lines except for the language line
              code = '\n'.join(lines[1:]).strip("` \n")

              arguments = {"code": code}
              if language: # We only add this if we have it-- the second we have it, an interpreter gets fired up (I think? maybe I'm wrong)
                if language == "bash":
                  language = "shell"
                arguments["language"] = language

            # Code-Llama won't make a "function_call" property for us to store this under, so:
            if "function_call" not in self.messages[-1]:
              self.messages[-1]["function_call"] = {}

            self.messages[-1]["function_call"]["parsed_arguments"] = arguments

      else:
        # We are not in a function call.

        # Check if we just left a function call
        if in_function_call == True:

          if self.local:
            # This is the same as when gpt-4 gives finish_reason as function_call.
            # We have just finished a code block, so now we should run it.
            llama_function_call_finished = True

        # Remember we're not in a function_call
        in_function_call = False

        # If there's no active block,
        if self.active_block == None:

          # Create a message block
          self.active_block = MessageBlock()

      # Update active_block
      self.active_block.update_from_message(self.messages[-1])

      # Check if we're finished
      if chunk["choices"][0]["finish_reason"] or llama_function_call_finished:
        if chunk["choices"][
            0]["finish_reason"] == "function_call" or llama_function_call_finished:
          # Time to call the function!
          # (Because this is Open Interpreter, we only have one function.)

          if self.debug_mode:
            print("Running function:")
            print(self.messages[-1])
            print("---")

          # Ask for user confirmation to run code
          if self.auto_run == False:

            # End the active block so you can run input() below it
            # Save language and code so we can create a new block in a moment
            self.active_block.end()
            language = self.active_block.language
            code = self.active_block.code

            # Prompt user
            response = input("  您想运行这段代码吗？(y/n)\n\n  ")
            print("")  # <- Aesthetic choice

            if response.strip().lower() == "y":
              # Create a new, identical block where the code will actually be run
              self.active_block = CodeBlock()
              self.active_block.language = language
              self.active_block.code = code

            else:
              # User declined to run code.
              self.active_block.end()
              self.messages.append({
                "role":
                "function",
                "name":
                "run_code",
                "content":
                "用户决定不运行此代码。"
              })
              return

          # If we couldn't parse its arguments, we need to try again.
          if not self.local and "parsed_arguments" not in self.messages[-1]["function_call"]:

            # After collecting some data via the below instruction to users,
            # This is the most common failure pattern: https://github.com/KillianLucas/open-interpreter/issues/41

            # print("> Function call could not be parsed.\n\nPlease open an issue on Github (openinterpreter.com, click Github) and paste the following:")
            # print("\n", self.messages[-1]["function_call"], "\n")
            # time.sleep(2)
            # print("Informing the language model and continuing...")

            # Since it can't really be fixed without something complex,
            # let's just berate the LLM then go around again.

            self.messages.append({
              "role": "function",
              "name": "run_code",
              "content": """无法解析您的函数调用。请仅使用“run_code”函数，该函数采用两个参数：“code”和“language”。您的响应应采用 JSON 格式。"""
            })

            self.respond()
            return

          # Create or retrieve a Code Interpreter for this language
          language = self.messages[-1]["function_call"]["parsed_arguments"][
            "language"]
          if language not in self.code_interpreters:
            self.code_interpreters[language] = CodeInterpreter(language, self.debug_mode)
          code_interpreter = self.code_interpreters[language]

          # Let this Code Interpreter control the active_block
          code_interpreter.active_block = self.active_block
          code_interpreter.run()

          # End the active_block
          self.active_block.end()

          # Append the output to messages
          # Explicitly tell it if there was no output (sometimes "" = hallucinates output)
          self.messages.append({
            "role": "function",
            "name": "run_code",
            "content": self.active_block.output if self.active_block.output else "No output"
          })

          # Go around again
          self.respond()

        if chunk["choices"][0]["finish_reason"] != "function_call":
          # Done!

          # Code Llama likes to output "###" at the end of every message for some reason
          if self.local and "content" in self.messages[-1]:
            self.messages[-1]["content"] = self.messages[-1]["content"].strip().rstrip("#")
            self.active_block.update_from_message(self.messages[-1])
            time.sleep(0.1)

          self.active_block.end()
          return

  def _print_welcome_message(self):
    print("", Markdown("●"), "", Markdown(f"\n欢迎来到**My Interpreter**.\n"), "")
