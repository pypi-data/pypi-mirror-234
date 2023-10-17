# This script initializes TeLLMgramBot with useful functions
import os, re

INIT_BOT_CONFIG = {
    'bot_username'   : 'test_bot',
    'bot_owner'      : '<YOUR USERNAME>',
    'bot_name'       : 'Test Bot',
    'bot_nickname'   : 'Testy',
    'bot_initials'   : 'TB',
    'chat_model'     : 'gpt-3.5-turbo',
    'url_model'      : 'gpt-4',
    'token_limit'    : None,
    'persona_temp'   : None,
    'persona_prompt' : 'You are a test harness bot.'
}

# Checks for important directories to configure for TeLLMgramBot
def init_directories():
    app_base_path = os.environ.get('TELLMGRAMBOT_APP_PATH', os.getcwd())

    # Update the environment variable with the cleaned-up path
    os.environ['TELLMGRAMBOT_APP_PATH'] = app_base_path

    # Create necessary directories
    directories = [
        os.path.join(app_base_path, 'sessionlogs'),
        os.path.join(app_base_path, 'errorlogs'),
        os.path.join(app_base_path, 'prompts'),
        os.path.join(app_base_path, 'configs'),
        # Add more as needed
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

# Investigates three API keys by file or environment variable
def init_keys():
    # List each key file and URL if it does not exist for more information
    key_files = {
        'openai.key'     : 'https://platform.openai.com/account/api-keys',
        'telegram.key'   : 'https://core.telegram.org/api',
        'virustotal.key' : 'https://developers.virustotal.com/reference/overview'
    }

    # Create key files and environment variables
    for key_file, url in key_files.items():
        path = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], key_file)
        key = re.sub("\..+", "", key_file).upper()  # Uppercase with .key removed
        env_var = f"TELLMGRAMBOT_{key}_API_KEY"

        # Ensures the specified key file is created and populated by user
        if not os.path.exists(path):
            # Create a basic ~.key file
            with open(path, 'w') as f:
                f.write(f"YOUR {key} API KEY HERE - {url}\n")
            print(f"Created new API key file: '{key_file}'")

        # If the environment variable is undefined, set by API key file
        if os.environ.get(env_var) is None:
            try:
                with open(path, 'r') as f:
                    os.environ[env_var] = f.read().strip()
                    print(f"Loaded secret for {env_var}")
            except FileNotFoundError:
                print(f"Key file not found for {env_var}")
            except Exception as e:
                print(f"An error occurred while loading {env_var}: {e}")

# Ensure the list of TeLLMgramBot commands is provided for user by a text file
def init_bot_commands(file='commands.txt') -> str:
    path = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], 'configs', file)
    if not os.path.exists(path):
        # Create a basic commands text file by filename
        with open(path, 'w') as f:
            f.write(
                "TeLLMgramBot commands:\n"
                "/start - Go online (Admin only)\n"
                "/stop - Go offline (Admin only)\n"
                "/nick - Add your nickname to set\n"
                "/forget - Clear your conversations\n"
                "/help - Show this information\n\n"
                "NOTE: Chat history will still show in your Telegram client. You must have a username, which is your default nickname unless specified like \"/nick B0b #2\".\n"
            )
        print(f"Created new Telegram commands file: '{file}'")
    return path

# Ensure bot configuration file is created
def init_bot_config(file='config.yaml') -> str:
    path = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], 'configs', file)
    if not os.path.exists(path):
        # Create a basic TeLLMgramBot configuration by filename
        with open(path, 'w') as f:
            # Add configuration with default values except prompt:
            for parameter, value in INIT_BOT_CONFIG.items():
                if parameter == 'persona_prompt': next
                else: # Write parameter, with optional comment if no value
                    f.write('%s : %s\n' % (
                        parameter.ljust(12),
                        value if value else '# Optional, see README'
                    ))
        print(f"Created new configuration file: '{file}'")
    return path

# Ensures TokenGPT configuration file is created
def init_tokenGPT_config(file='tokenGPT.yaml') -> str:
    path = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], 'configs', file)
    if not os.path.exists(path):
        # Create a basic GPT configuration of token parameters by filename
        with open(path, 'w') as f:
            f.write(
                "# Available parameters per base ChatGPT model with default values:\n"
                "#   max_tokens: 4097\n"
                "#   tokens_per_message: 3\n"
                "#   tokens_per_name: 1\n"
                "# For OpenAI's updated list of additional ChatGPT models, please see:\n"
                "#   https://platform.openai.com/docs/models/overview\n"
                "'gpt-4':\n"
                "  max_tokens: 8192\n"
                "'gpt-3.5-turbo':\n"
                "  max_tokens: 4097\n"
            )
        print(f"Created new TokenGPT configuration file: '{file}'")
    return path

# Ensure prompt file is created that defines bot personality
def init_bot_prompt(file='test_personality.prmpt') -> str:
    path = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], 'prompts', file)
    if not os.path.exists(path):
        # Create a basic TeLLMgramBot prompt by filename
        with open(path, 'w') as f:
            f.write(
                "You are a test harness bot based on a GPT 3.5 Turbo model that can:\n"
                "1. Fetch URLs, provided the user supply a URL in [square brackets].\n"
                "2. Scrub URLs to ensure they are safe for work via the VirusTotal API.\n"
            )
        print(f"Created new bot personality prompt file: '{file}'")
    return path

# Ensure prompt file is created that defines how the bot will analyze URLS via square brackets []
def init_url_prompt(file='url_analysis.prmpt') -> str:
    path = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], 'prompts', file)
    if not os.path.exists(path):
        # Create a basic URL analysis prompt by filename
        with open(path, 'w') as f:
            f.write(
                "The user has provided a URL to perform some level of analysis. You will infer the nature of the analysis from the user's query.\n\n"
                "The contents of the URL mentioned have already been harvested and cleansed. Note the URL contents will likely have sections of text that are less relevant to the user's question (headers, footers, menus, ads, etc.). You will need to ignore those sections of text and focus on the main content of the page.\n\n"
                "The contents of the URL are shown below:\n"
                "BEGIN URL CONTENTS\n"
                "{url_content}\n"
                "END URL CONTENTS\n"
            )
        print(f"Created new URL analysis prompt file: '{file}'")
    return path

# Performs main setup, especially with necessary files
def init_structure():
    init_directories()
    init_keys()
    init_url_prompt()
    init_tokenGPT_config()
    init_bot_commands()

# Run this script if the first time setting up TeLLMgramBot
if __name__ == '__main__':
    init_structure()
    init_bot_config()
    init_bot_prompt()
    print("TeLLMgramBot setup complete!")
