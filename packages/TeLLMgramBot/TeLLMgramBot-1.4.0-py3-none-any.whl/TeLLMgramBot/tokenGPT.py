# Defines ChatGPT model parameters and token count of messages using OpenAI's tiktoken library
# Sources:
# > https://platform.openai.com/docs/models/overview
# > https://github.com/openai/openai-python/blob/main/chatml.md
# > https://platform.openai.com/docs/guides/fine-tuning
import re, tiktoken
from .utils import read_yaml
from .initialize import init_tokenGPT_config

class TokenGPT:
    def __init__(self, openai_model="gpt-3.5-turbo", yaml_file="tokenGPT.yaml"):
        # The OpenAI model name may also be a fine-tuned model, which has the base ChatGPT 
        # model after "ft:" up to the next colon (:), like "ft:gpt-3.5-turbo-0613:..."
        self.model = re.search("^ft\:([^:]*)", openai_model).group(1) if openai_model.startswith("ft:") else openai_model
        self.config_path = init_tokenGPT_config(yaml_file)

        # Get ChatGPT model parameters by configuration file for the:
        # > Maximum number of tokens
        # > Tokens per message
        # > Tokens per name by ChatGPT model
        self.param = None
        for key, param in read_yaml(self.config_path).items():
            # Set parameters if the configuration key matches either:
            #  > Full OpenAI model name (an exact match to stop searching)
            #  > Base ChatGPT name after "ft:" up to next colon (:), part of the OpenAI model name
            if key == openai_model or key == self.model:
                self.param = param
                if key == openai_model: break

        # If the parameters are not set, the OpenAi model name is invalid or
        # has an undefined ChatGPT model configuration not set in the YAML file
        if self.param is None:
            raise ValueError(f"OpenAI model \"{openai_model}\" is invalid or its base ChatGPT model is not in:\n{self.config_path}")

        # Set token model parameter defaults, unless defined in configuration:
        if 'max_tokens' not in self.param:
            self.param['max_tokens'] = 4097
        if 'tokens_per_message' not in self.param:
            self.param['tokens_per_message'] = 3
        if 'tokens_per_name' not in self.param:
            self.param['tokens_per_name'] = 1

        # Get OpenAI's tiktoken encoding of the base ChatGPT model name
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")
            print(f"Warning: {self.encoding} for an unknown ChatGPT model \"{self.model}\"")

    # Query the maximum amount of tokens possible an OpenAI model can support
    def max_tokens(self) -> int:
        return self.param['max_tokens']

    # Return the number of tokens based on a list of messages
    # Source: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    def num_tokens_from_messages(self, messages: dict[str, str]) -> int:
        num_tokens = 0
        for message in messages:
            num_tokens += self.param['tokens_per_message']
            for key, value in message.items():
                num_tokens += len(self.encoding.encode(value))
                if key == "name":
                    num_tokens += self.param['tokens_per_name']
        num_tokens += 3  # Every reply is primed with <|start|>assistant<|message|>
        return num_tokens
