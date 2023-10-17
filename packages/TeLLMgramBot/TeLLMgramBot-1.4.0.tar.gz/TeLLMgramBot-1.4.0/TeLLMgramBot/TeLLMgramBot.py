#!/usr/bin/env python
import os, re, json
import openai
from math import floor
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from .initialize import INIT_BOT_CONFIG, init_structure, init_bot_config, init_bot_prompt, init_bot_commands
from .conversation import Conversation
from .tokenGPT import TokenGPT
from .message_handlers import handle_greetings, handle_common_queries, handle_url_ask
from .utils import read_yaml, read_text, log_error

class TelegramBot:
    # Show all the commands available by the bot using the TelegramCommands.txt file
    async def tele_commands(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply = ''
        with open(init_bot_commands('commands.txt'), "r", encoding="utf-8") as file:
            for line in file: reply += line
        await update.message.reply_text(reply)

    # Start command only runs by the 'bot_owner' specified in configuration file 
    async def tele_start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        current_uname = update.message.chat.username.lstrip("@")
        if current_uname == self.telegram['owner']:
            greeting_text = f"Oh, hello {update.message.from_user.first_name}! Let me get to work!"
            await update.message.reply_text(greeting_text)
            self.started = True
            self.GPTOnline = True
        else:
            await update.message.reply_text("Sorry, but I'm off the clock at the moment.")

    # Stop command formally closes out the polling loop
    async def tele_stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        current_uname = update.message.chat.username.lstrip("@")
        if current_uname == self.telegram['owner']:
            self.GPTOnline = False
            await update.message.reply_text("Sure thing boss, cutting out!")
        else:
            await update.message.reply_text("Sorry, I can't do that for you.")

    # Let bot know to call the user by a different name other than the Telegram user name
    async def tele_nick_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Must follow the format of "/nick <nickname>" using regular expression
        result = re.search(r'^\/nick[ \n]+([ \S]+)', update.message.text)
        if result is not None:
            prompt = f"Please refer to me by my nickname, {result.group(1).strip()}, rather than my user name."
            await update.message.reply_text( await self.tele_handle_response(text=prompt, update=update) )
        else:
            await update.message.reply_text("Please provide a valid nickname after the command like \"/nick B0b #2\".")

    # Remove the whole conversation including past session logs for peace of mind
    async def tele_forget_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        uname = update.message.from_user.username
        if uname in self.conversations:
            self.conversations[uname].clear_interaction()
            del self.conversations[uname] # Delete object as well
            await update.message.reply_text("My memories of all our conversations are wiped!")
        else:
            await update.message.reply_text(
                "My apologies, but I don't recall any conversations with you," +
                " or you previously asked me to forget about you. Either way, nice to meet you!"
            )

    # Responses
    async def tele_handle_response(self, text: str, update: Update) -> str:
        # Before we handle messages, ensure a user has /started us
        # Starting ensures we get some kind of user account details for logging
        not_started_reply = "I'd love to chat, but please wait as I haven't started up yet!"
        if not self.started:
            return not_started_reply

        # See if this is a new conversation we need to track by user ID
        # Bot user name is more consistent across restarts and different conversation instances
        uname = update.message.from_user.username
        if uname not in self.conversations:
            self.conversations[uname] = Conversation(
                uname,
                self.telegram['username'],
                self.chatgpt['prompt'],
                self.chatgpt['chat_model']
            )
            # If there are past conversations via logs, load 50% by the token limit
            self.conversations[uname].get_past_interaction(floor(self.chatgpt['token_limit'] / 2))

        # Add the user's message to our conversation
        self.conversations[uname].add_user_message(text)

        # Check if the user is asking about a [URL]
        url_match = re.search(r'\[http(s)?://\S+]', text)

        # Form the assistant's message based on low level easy stuff or send to GPT
        # OpenAI relies on the maximum amount of tokens a ChatGPT model can support
        reply = not_started_reply
        if handle_greetings(text):
            reply = handle_greetings(text)
        elif handle_common_queries(text):
            reply = handle_common_queries(text)
        elif url_match:
            # URL content is passed into another model to summarize (GPT-4 preferred)
            await update.message.reply_text("Sure, give me a moment to look at that URL...")
            reply = await handle_url_ask(text, self.chatgpt['url_model'])
        elif self.GPTOnline:
            # This is essentially the transition point between quick Telegram replies and GPT
            reply = self.gpt_completion(uname)['choices'][0]['message']['content'].strip()

        # Add assistant's message to the user's conversation
        self.conversations[uname].add_assistant_message(reply)

        # Calculate the total token count of our conversation messages via tiktoken
        token_count = self.conversations[uname].get_message_token_count()

        # Ensure our conversation token limit is NOT overloaded by rolling thresholds:
        token_prune_upper = floor(self.chatgpt['token_limit'] * self.chatgpt['prune_threshold'])
        token_prune_lower = floor(self.chatgpt['token_limit'] * self.chatgpt['prune_back_to'])
        if token_count > token_prune_upper:
            # Start pruning if we hit our upper threshold (still warned well below it)
            self.conversations[uname].prune_conversation(token_prune_lower)
        elif token_count > token_prune_lower and uname not in self.token_warning:
            # Warn user if getting close to the conversation limit
            reply += ("\n\nBy the way, we're getting close to my current conversation length limits,"
                      " so I may start forgetting some of our older exchanges. Would you like me to"
                      " summarize our conversation so far to keep the main points alive?")
            self.token_warning[uname] = True

        return reply

    # Handles the Telegram side of the message, discerning between Private and Group conversation
    async def tele_handle_message(self, update: Update, context=ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type # PM or Group Chat
        message_text: str = update.message.text
        print(f'User {update.message.from_user.username} in {message_type} chat ID {update.message.chat.id}')

        # If it's a group text, only reply if the bot is named
        # The real magic of how the bot behaves is in tele_handle_response()
        if message_type == 'supergroup' or message_type == 'group':
            if self.telegram['username'] in message_text:
                new_text: str = message_text.replace(self.telegram['username'], '').strip()
                response: str = await self.tele_handle_response(text=new_text, update=update)
            elif self.telegram['nickname'].lower() in message_text.lower() or self.telegram['initials'] in message_text:
                response: str = await self.tele_handle_response(text=message_text, update=update)
            else:
                return
        elif message_type == 'private':
            response: str = await self.tele_handle_response(text=message_text, update=update)
        else:
            return
        await update.message.reply_text(response)

    # Handle errors caused on the Telegram side
    async def tele_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.from_user.username is None:
            # If the user doesn't have a Telegram username, we can't really do anything
            await update.message.reply_text('Add a username to your Telegram account so that I can talk to you!')
        else:
            log_error(context.error, 'Telegram', self.ErrorLog)
            await update.message.reply_text("Sorry, I ran into an error! Please contact my creator.")

    # Read the GPT Conversation so far
    @staticmethod
    def gpt_read_interactions(file_path: str):
        with open(file_path, 'r') as interaction_log:
            lines = interaction_log.readlines()
        formatted_messages = [json.loads(line) for line in lines]
        return formatted_messages

    # Get the OpenAI Chat Completion response based on bot configuration
    def gpt_completion(self, uname: str):
        try:
            response = openai.ChatCompletion.create(
                model       = self.chatgpt['chat_model'],
                messages    = self.conversations[uname].messages,
                temperature = self.chatgpt['temperature'],
                top_p       = self.chatgpt['top_p']
            )
            return response
        except openai.error.AuthenticationError as e:
            # Handle authentication error
            log_error(e, error_type='OpenAI-Authentication', error_filename=self.ErrorLog)
        except openai.error.InvalidRequestError as e:
            # Handle invalid request error
            log_error(e, error_type='OpenAI-InvalidRequest', error_filename=self.ErrorLog)
        except openai.error.APIConnectionError as e:
            # Handle API connection error
            log_error(e, error_type='OpenAI-APIConnection', error_filename=self.ErrorLog)
        except openai.error.OpenAIError as e:
            # Handle other OpenAI-related errors
            log_error(e, error_type='OpenAI-Other', error_filename=self.ErrorLog)
        except Exception as e:
            # Catch any other unexpected exceptions
            log_error(e, error_type='Other', error_filename=self.ErrorLog)

    # The main polling "loop" the user interacts with via Telegram
    def start_polling(self):
        print(f"TeLLMgramBot {self.telegram['username']} polling...")
        self.telegram['app'].run_polling(poll_interval=self.telegram['pollinterval'])
        print(f"TeLLMgramBot {self.telegram['username']} polling ended.")

    # Initialization
    def __init__(self,
        bot_username   = INIT_BOT_CONFIG['bot_username'],
        bot_owner      = INIT_BOT_CONFIG['bot_owner'],
        bot_name       = INIT_BOT_CONFIG['bot_name'],
        bot_nickname   = INIT_BOT_CONFIG['bot_nickname'],
        bot_initials   = INIT_BOT_CONFIG['bot_initials'],
        chat_model     = INIT_BOT_CONFIG['chat_model'],
        url_model      = INIT_BOT_CONFIG['url_model'],
        token_limit    = INIT_BOT_CONFIG['token_limit'],
        persona_temp   = INIT_BOT_CONFIG['persona_temp'],
        persona_prompt = INIT_BOT_CONFIG['persona_prompt']
    ):
        # First provide the main structure if not already there
        init_structure()

        # Set up our variables
        self.ErrorLog = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], 'errorlogs', 'error.log')
        self.started = False
        self.GPTOnline = False
        self.token_warning = {} # Determines whether user has reached token limit by OpenAI model
        self.conversations = {} # Provides Conversation class per user based on bot response

        # Get Telegram Spun Up
        self.telegram = {
            'owner'        : bot_owner,
            'username'     : bot_username,
            'nickname'     : bot_nickname,
            'initials'     : bot_initials,
            'pollinterval' : 3
        }
        self.telegram['app'] = Application.builder().token(os.environ['TELLMGRAMBOT_TELEGRAM_API_KEY']).build()

        # Add our handlers for Commands, Messages, and Errors
        self.telegram['app'].add_handler(CommandHandler('help', self.tele_commands))
        self.telegram['app'].add_handler(CommandHandler('start', self.tele_start_command))
        self.telegram['app'].add_handler(CommandHandler('stop', self.tele_stop_command))
        self.telegram['app'].add_handler(CommandHandler('nick', self.tele_nick_command))
        self.telegram['app'].add_handler(CommandHandler('forget', self.tele_forget_command))
        self.telegram['app'].add_handler(MessageHandler(filters.TEXT, self.tele_handle_message))
        self.telegram['app'].add_error_handler(self.tele_error)

        # Get our LLM Spun Up with defaults if not defined by user input
        # Token limit not defined uses maximum tokens by conversation GPT model
        self.chatgpt = {
            'name'            : bot_name,
            'prompt'          : persona_prompt,
            'chat_model'      : chat_model,
            'url_model'       : url_model,
            'token_limit'     : token_limit or TokenGPT(chat_model).max_tokens(),
            'temperature'     : persona_temp or 1.0,
            'top_p'           : 0.9,
            'prune_threshold' : 0.95,
            'prune_back_to'   : 0.75
        }
        openai.api_key = os.environ['TELLMGRAMBOT_OPENAI_API_KEY']

    # Sets TeLLMgramBot object based on its YAML configuration and prompt files
    def set(config_file='config.yaml', prompt_file='test_personality.prmpt'):
        # First provide the main structure if not already there
        init_structure()

        # Ensure both bot configuration and prompt files are defined and readable
        config = read_yaml(init_bot_config(config_file))
        prompt = read_text(init_bot_prompt(prompt_file))

        # Check any configuration values missing and apply default values:
        for parameter, value in INIT_BOT_CONFIG.items():
            if parameter == 'persona_prompt':
                # Apply initial prompt if not defined
                if not prompt:
                    prompt = value
                    print(f"File '{prompt_file}' is empty, set default prompt '{prompt}'")
            elif parameter not in config:
                # Apply initial configuration paramter with default if not defined
                config[parameter] = value
                if value: print(f"Configuration '{parameter}' not defined, set to '{value}'")

        # Apply parameters to bot:
        return TelegramBot(
            bot_username   = config['bot_username'],
            bot_owner      = config['bot_owner'],
            bot_name       = config['bot_name'],
            bot_nickname   = config['bot_nickname'],
            bot_initials   = config['bot_initials'],
            chat_model     = config['chat_model'],
            url_model      = config['url_model'],
            token_limit    = config['token_limit'],
            persona_temp   = config['persona_temp'],
            persona_prompt = prompt
        )
