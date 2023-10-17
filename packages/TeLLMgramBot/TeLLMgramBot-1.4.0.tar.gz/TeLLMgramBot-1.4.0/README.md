# TeLLMgramBot
The basic goal of this project is to create a bridge between a Telegram Bot and a Large Langage Model (LLM), like ChatGPT.

<img src="assets/TeLLMgramBot_Logo.png" width=200 align=center />

**Disclaimer**: In order to use this library, you must have a Telegram account **with a user name**, not just a phone number. If you don't have one, [create one online](https://telegram.org/).

## Telegram Bot + LLM Encapsulation
* The Telegram interface handles special commands, especially on some basic "chatty" prompts and responses that don't require LLM, like "Hello".
* The more dynamic conversation gets handed off to the LLM to manage prompts and responses, and Telegram acts as the interaction broker.
* Pass the URL in [square brackets] and mention how the bot should interpret it.
  * Example: "What do you think of this article? [https://some_site/article]"
  * This uses another ChatGPT model, preferrably GPT-4, to support more URL content by OpenAI tokens.
* Tokens are used to measure the length of all conversation messages between the Telegram bot assistant and the user. This is useful to:
  * Ensure the length does not go over the ChatGPT model limit. If it does, prune oldest messages to fit within the limit.
  * Remember 50% of the past conversations when starting up TeLLMgramBot again.
* Users can also clear their conversation history for privacy.

## Why Telegram?
Using Telegram as the interface not only solves "exposing" the interface, but gives you boadloads of interactivity over a standard Command Line interface, or trying to create a website with input boxes and submit buttons to try to handle everything:
1. Telegram already lets you paste in verbose, multiline messages.
2. Telegram already lets you paste in pictures, videos, links, etc.
3. Telegram already lets you react with emojis, stickers, etc.

## Directories
When initializing TeLLMgramBot, the following directories get created:
* `configs` - Contains bot conifguration files.
  * `commands.txt`
    * Users can type `/help` interacting with the to see this file's text get displayed in Telegram.
  * `config.yaml` (can be a different name)
    * This file sets main OpenAI parameters like naming and ChatGPT models to process.
    * The parameter `url_model` is to read URL content, different than `chat_model` that the bot normally uses to interact with the user.
    * An empty `token_limit` would do the maximum amount of tokens supported by the `chat_model` (e.g. 4097 for `gpt-3.5-turbo`).
  * `tokenGPT.yaml`
    * This important YAML file contains token size parameters for every ChatGPT model possible supported by OpenAI.
    * If the first time, only `gpt-3.5-turbo` and `gpt-4` get populated, but the user can specify more models with token size parameters as needed.
* `prompts` - Contains prompt files for how the bot interacts with any user.
    * `test_personality.prmpt`
      * This is a sample prompt file as a basis to test this library.
      * The user can create more prompt files as needed for different personalities. See [OpenAI Playground](https://platform.openai.com/playground) to test some ideas.
    * `url_analysis.prmpt`
      * This is a crucial prompt file to analysis URL content in brackets `[]` in a different ChatGPT model (likely `gpt-4` or higher).
* `errorlogs`
   * Contains error log files to investigate if there are problems during the interaction.
   * User will also get notified to contact the owner.
* `sessionlogs`
  * Every conversation is stored between the Telegram bot assistant and each user.
  * If a user types `/forget`, any session log files between the bot and the user will all be removed.

## API Keys
To operate TeLLMgramBot, three API keys are required:
* [OpenAI](https://platform.openai.com/overview) - Drives the actual GPT AI.
* [BotFather](https://t.me/BotFather) - Helps create a new Telegram bot and provide its API.
* [VirusTotal](https://www.virustotal.com/gui/home/) - Performs safety checks on URLs.

There are two ways to populate each API key: environment variables or `.key` files.

### Environment Variables
TeLLMgramBot uses the following environment variables that can be pre-loaded with the three API keys respectively:
1. `TELLMGRAMBOT_OPENAI_API_KEY`
2. `TELLMGRAMBOT_TELEGRAM_API_KEY`
3. `TELLMGRAMBOT_VIRUSTOTAL_API_KEY`

During spin-up time, a user can call out `os.environ[env_var]` to set those variables, like the following example:
```
my_keys = Some_Vault_Fetch_Function()

os.environ['TELLMGRAMBOT_OPENAI_API_KEY']     = my_keys['GPTKey']
os.environ['TELLMGRAMBOT_TELEGRAM_API_KEY']   = my_keys['BotFatherToken']
os.environ['TELLMGRAMBOT_VIRUSTOTAL_API_KEY'] = my_keys['VirusTotalToken']
```

This means the user can implement whatever key vault they want to fetch the keys at runtime, without needing files stored in the directory.

### API Key Files
By default, three files are created for the user to input each API key:
1. `openai.key`
2. `telegram.key`
3. `virustotal.key`

Setting each file also updates its respective environment variable as discussed before, if not defined.

## Bot Setup
This library includes an example script `test_local.py`, which uses files from the folders `configs` and `prompts` for TeLLMgramBot to process.
1. Ensure the previous sections are followed with the proper API keys and your Telegram bot set.
2. Install this library via PIP (`pip install TeLLMgramBot`) and then import into your project.
3. Instantiate the bot by passing in various configuration pieces needed below:
   ```
   telegram_bot = TeLLMgramBot.TelegramBot(
       bot_username   = <Bot username like 'friendly_bot'>,
       bot_owner      = <Bot owner's Telegram username>,
       bot_name       = <Bot name like 'Friendly Bot'>,
       bot_nickname   = <Bot nickname like 'Botty'>,
       bot_initials   = <Bot initials like 'FB'>,
       chat_model     = <Conversation ChatGPT model like 'gpt-3.5-turbo'>,
       url_model      = <URL contents ChatGPT model like 'gpt-4'>,
       token_limit    = <Maximum token count set, by default chat_model max>,
       persona_temp   = <LLM factual to creative value [0-2], by default 1.0>,
       persona_prompt = <System prompt summarizing bot personality>
   )
   ```
4. Turn on TeLLMgramBot by calling:
   ```
   telegram_bot.start_polling()
   ```
   Once you see `TeLLMgramBot polling...`, the bot is online in Telegram.
5. Typing `/help` shows all available commands reported by the `configs/commands.txt` file.
6. Only by the bot owner, type `/start` to initiate user conversations.

## Resources
* GitHub repository [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) has guides to create a Telegram bot.
* For more information on ChatGPT models like `gpt-3.5-turbo` and tokens, see the following:
  * [OpenAI model overview and maximum tokens](https://platform.openai.com/docs/models/overview).
  * [OpenAI message conversion to tokens](https://github.com/openai/openai-python/blob/main/chatml.md).
  * [OpenAI custom fine-tuning](https://platform.openai.com/docs/guides/fine-tuning).
  * [OpenAI's tiktoken library, including some helpful guides](https://github.com/openai/tiktoken/tree/main).
* [OpenAI Playground](https://platform.openai.com/playground) is a great place to test out prompts and responses.
