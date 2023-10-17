# Provides TeLLMgramBot a way to store and retrieve conversation messages by the OpenAI model
import os, re
from .tokenGPT import TokenGPT
from .utils import get_safe_username, generate_filename, read_reverse_order

class Conversation:
    def __init__(self, user_name: str, assist_name: str, system_content: str, system_model="gpt-3.5-turbo"):
        # Define who's talking for the two-way conversation
        self.user_name = get_safe_username(user_name)
        self.assist_name = assist_name

        # System defines how the assistant will respond to the user by prompt and GPT model
        self.system_content = system_content
        self.system_model = TokenGPT(system_model)
        self.messages = [{"role": "system", "content": system_content}]

        # Orient to the base app path for TellMgramBot no matter what sub folder I'm coming from
        if not os.environ.get('TELLMGRAMBOT_APP_PATH'):
            current_path = os.getcwd()
            app_index = current_path.find("TeLLMgramBot")
            base_path = current_path[:app_index + len("TeLLMgramBot")]
            os.environ['TELLMGRAMBOT_APP_PATH'] = base_path

        # Define the directory where to store this conversation with the log file name
        self.interaction_dir = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], 'sessionlogs')
        self.interaction_log = generate_filename(self.assist_name, self.user_name)

        # Private boolean determines if conversation includes past messages
        # This will be true if user calls out function get_past_interaction()
        self._has_past_interaction = False

    # Replace the system content as the first message of the conversation
    def set_system_content(self, new_content: str):
        self.system_content = new_content
        self.messages[0] = {"role": "system", "content": new_content}

    # Add user message and write to this conversation's log file
    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
        self.write_interaction(role="user", content=content)

    # Add assistant message and write to this conversation's log file
    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})
        self.write_interaction(role="assistant", content=content)

    # Clear out current conversation by:
    def clear_messages(self):
        # Any user-assistant messages even from past, except system message
        self.messages = [self.messages[0]]
        self._has_past_interaction = False

        # Log file storing the messages 
        log_path = os.path.join(self.interaction_dir, self.interaction_log)
        if os.path.isfile(log_path):
            with open(log_path, 'w'): pass

    # Each message size is determined by the number of tokens via OpenAI's tiktoken library
    # Another way would be to use bytes, but not as accurate since it depends on GPT model
    def get_message_token_count(self):
        return self.system_model.num_tokens_from_messages(self.messages)

    # Write to a new log file the conversation message by role
    # This addresses UTF-8 characters, especially other symbols like integrals
    def write_interaction(self, role: str, content: str):
        log_path = os.path.join(self.interaction_dir, self.interaction_log)
        mode = 'w' if not os.path.exists(log_path) else 'a'
        with open(log_path, mode, encoding='utf-8') as file:
            file.write(f'<{role}>: {content}\n')

    # Pop messages off the stack until the token size is below threshold
    def prune_conversation(self, token_limit: int):
        popped_message = self.messages.pop()
        if self.get_message_token_count() > token_limit:
            self.prune_conversation(token_limit)

    # Get all conversation log files of the same user and assistant
    def get_interaction_files(self):
        # Start looping each log file sorted by timestamp
        files = []
        for file in sorted(os.listdir(self.interaction_dir)):
            # Check if full names of user and assistant are in the log name
            if file.startswith(f"{self.assist_name}-{self.user_name}-"):
                files.append(file)
        return files

    # Read logs to store past conversation messages up to a token limit
    def get_past_interaction(self, token_limit: int):
        # First check if the conversation does not have past user-assistant messages
        names = f"User {self.user_name} & Assistant {self.assist_name}"
        if self._has_past_interaction == False:
            # Set initial variables if token limit has reached and initial number of messages
            limit_reached = 0
            message_count = len(self.messages)
            token_count = 0

            # Start looping each log file with timestamp in descending order
            for log_file in sorted(self.get_interaction_files(), reverse=True):
                # Skip if the log file is the current conversation log
                if log_file == self.interaction_log: continue

                # Iterate through the log file backwards by line and populate content for each role
                role    = '' # Set role blank, user should start off before assistant
                content = '' # Set content blank to start off
                for line in read_reverse_order(os.path.join(self.interaction_dir, log_file)):
                    # Remove leading and trailing spaces
                    line = line.strip()

                    # Append content after the stripped line by scenario:
                    # 1.) A new line if there is an empty line with actual content in between.
                    if line == '' and content != '': content = '\n' + content
                    # 2.) The right poriton of the line if the role name by format
                    #     ('<user>: ...', '<assistant>: ...') is defined.
                    result = re.search(r'^\<(user|assistant)\>: (.*)', line)
                    if result is not None:
                        role = result.group(1)
                        content = result.group(2) + content
                    # 3.) The whole line if the role name by format is not defined.
                    else: content = line + content

                    # If the role and content are defined, add both as one message
                    # Otherwise keep adding the content until the role is defined
                    if result is not None:
                        # Since we are going backwards, put it after the first and only system message
                        self.messages.insert(1, {"role": role, "content": content})
                        content = '' # Reset content for next round

                        # See if the series of messages does actually fit by token limit
                        token_count = self.get_message_token_count()
                        if token_count > token_limit:
                            self.messages.pop(1) # Remove message inserted recently
                            token_count = self.get_message_token_count()
                            limit_reached = 1
                            break

                # Stop going through logs if the token limit has reached
                if limit_reached: break

            # Print in terminal if there were conversations via session logs
            self._has_past_interaction = True
            if message_count != len(self.messages):
                print(f"{names} had past conversations {'above' if limit_reached else 'within'}"
                      f" the token limit {token_limit}, storing {token_count} token(s)")
            else:
                print(f"{names} are in their first conversation")  
        else:
            print(f"{names} had their past conversations defined")

    # Erase every message and log of the user-assistant conversation
    def clear_interaction(self):
        self.clear_messages()        
        for file in self.get_interaction_files():
            log_path = os.path.join(self.interaction_dir, file)
            if os.path.isfile(log_path):
                os.remove(log_path)
            else:
                print(f"Error: File '{log_path}' not found to delete")
