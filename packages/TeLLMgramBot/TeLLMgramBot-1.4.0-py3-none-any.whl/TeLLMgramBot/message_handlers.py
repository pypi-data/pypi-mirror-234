# Handles incoming messages and URLs unique for TeLLMgramBot
import os, re
import openai
import validators

from typing import Optional
from .initialize import init_url_prompt
from .tokenGPT import TokenGPT
from .web_utils import fetch_url, strip_html_markup, InvalidURLException, InsecureURLException, SusURLException

# Respond quickly with single word greetings
# Example: Typing ' hello ...? ' makes bot respond 'Hello!'
def handle_greetings(text: str) -> Optional[str]:
    greetings = {'Hello', 'Hi', 'Hey', 'Heya', 'Sup', 'Yo'}
    word = re.sub(r'[^\w]', '', text.title().strip())
    if word in greetings:
        return f'{word}!'
    return None

# Respond quickly with certain phrases
# Example: Typing 'What's up!' makes bot respond 'Wassup?'
def handle_common_queries(text: str) -> Optional[str]:
    phrase = re.sub(r'[^\w]', '', text.lower().strip())
    if phrase.startswith('howyoudoin'):
        return 'How YOU doin?'
    elif phrase == 'wassup' or phrase == 'whatup' or phrase == 'whatsup':
        return 'Wassup?'
    return None

# Process URL content in another OpenAI model to provide a summary
async def handle_url_ask(text: str, model='gpt-4') -> Optional[str]:
    # Check if the message contains a URL wrapped in square brackets [] only
    # Note URLs may be case-sensitive especially with subdirectories
    url_match = re.search(r'\[http(s)?://\S+]', text.strip())

    if url_match:
        # Extract the URL from the message, but not the square brackets
        url = url_match.group()[1:-1]

        # Fetch the URL content
        try:
            # The function strips the HTML markup and ensures the URL is valid and safe
            url_content = strip_html_markup(await fetch_url(url))

            # Check if the URL is valid real quick
            if not validators.url(url):
                raise InvalidURLException(f'Invalid URL parsed by message_handlers.handle_url_ask(): {url}')

            # Let's begin by building the OpenAI messages to set:
            # 1. URL content to be added into the system prompt template
            # 2. User message requesting URL in [square brackets]
            messages = [
                {"role": "system", "content": url_content},
                {"role": "user",   "content": text}
            ]

            # Consider the maximum amount of tokens a ChatGPT model can support:
            #  > GPT-4:         8,192 or 32,768 for 32k version
            #  > GPT-3-5-turbo: 4,097 or 16,385 for 16k version
            # If the URL content is too big, we need to prune it down to a reasonable size the
            # model used can support. Let's also reserve 500 tokens for prompt and response. 
            lengthy_url = False
            pruned_tail = ''
            token_model = TokenGPT(model)
            token_count = token_model.num_tokens_from_messages(messages)
            token_limit = token_model.max_tokens() - 500
            if token_count > token_limit:
                lengthy_url = True
                while token_count > token_limit:
                    # Remove every last word until the token limit is satisfied
                    messages[0]["content"] = messages[0]["content"].rsplit(' ', 1)[0] 
                    token_count = token_model.num_tokens_from_messages(messages)
                # Show the last 50 characters of the pruned URL content
                pruned_tail = messages[0]["content"][-50:]

            # Load system prompt template to insert URL content
            with open(init_url_prompt('url_analysis.prmpt'), 'r') as f:
                template = f.read()
            messages[0]["content"] = template.format(url_content=messages[0]["content"])

            # Call OpenAI API for the response that summarizes URL content
            openai.api_key = os.environ['TELLMGRAMBOT_OPENAI_API_KEY']
            try:
                ask_results = openai.ChatCompletion.create(
                    model       = model,
                    messages    = messages,
                    temperature = 0.9
                )
                response = ask_results['choices'][0]['message']['content'].strip()
            except Exception as e:
                print(f"Error in calling OpenAI API: {e}")
                return "Something went wrong while fetching the URL. Please try again later."

            # If the URL content was too long, let the user know
            if lengthy_url:
                response += ("\n\n"
                    f"*NOTE: The URL content was too long and needed to be pruned for its `{model}` model."
                    f" If the content after \"{pruned_tail}\" is crucial, let me know by pasting it here.*"
                )
            return response

        except InvalidURLException:
            return "The URL you provided appears to be invalid. Could you please check it and try again?"
        except InsecureURLException:
            return "The URL you provided is not secure. Could you please try another URL, or just pasting the relevant content here?"
        except SusURLException:
            return "The URL you provided is potentially unsafe, based on my internal scans. You can check the safety of URLS using this site: https://www.virustotal.com/gui/home/url"
        except Exception as e:
            return f"Something went wrong while fetching the URL: {e}"

    return None
