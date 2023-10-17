# Fetches the content of a URL and returns the HTML as a string
# If a specific <div> tag ID is provided, extracts only that content
import os
import re
import asyncio
from typing import Optional
from urllib.parse import urlparse

import httpx
import validators
from bs4 import BeautifulSoup


class InvalidURLException(Exception):
    """Exception raised for invalid URLs."""
    pass


class InsecureURLException(Exception):
    """Exception raised for insecure URLs."""
    pass


class SusURLException(Exception):
    """Exception raised for insecure URLs."""
    pass


class FetchingError(Exception):
    """Exception raised for errors during fetching."""
    pass


async def check_url_safety(url: str, max_retries=5, retry_delay=5) -> Optional[bool]:
    headers = {'x-apikey': os.environ['TELLMGRAMBOT_VIRUSTOTAL_API_KEY']}
    data = {'url': url}

    async with httpx.AsyncClient() as client:
        response = await client.post(url='https://www.virustotal.com/api/v3/urls', headers=headers, data=data)

        if response.status_code == 200:  # OK
            json_response = response.json()
            analysis_id = json_response.get("data", {}).get("id", None)  # Extract the analysis ID from the response
            if analysis_id:
                retries = 0  # Initialize retry counter
                while retries <= max_retries:  # While we haven't exceeded max retries
                    # Now check the analysis results
                    response = await client.get(
                        url=f'https://www.virustotal.com/api/v3/analyses/{analysis_id}',
                        headers=headers
                    )
                    if response.status_code == 200:  # OK
                        json_response = response.json()
                        attributes = json_response.get("data", {}).get("attributes", None)
                        if attributes:
                            status = attributes.get("status", None)
                            if status == "completed":
                                malicious = attributes.get("stats", {}).get("malicious", None)
                                suspicious = attributes.get("stats", {}).get("suspicious", None)
                                if malicious == 0 and suspicious < 3:
                                    return True  # URL is safe
                                else:
                                    print(f"URL is not safe. Malicious: {malicious}, "
                                          f"Suspicious: {suspicious}, Status: {status}")
                                    return False  # URL is not safe
                            elif status == "queued":
                                retries += 1  # Increment retry counter
                                await asyncio.sleep(retry_delay)  # Wait before retrying
                            else:
                                print(f"Unexpected status: {status}")
                                return None
                        else:
                            print("Attributes not found in the response.")
                            return None
                    else:
                        print("Error in fetching analysis results.")
                        return None
            else:
                print("Analysis ID not found in the response.")
                return None
        else:
            print(f"An error occurred: {response.status_code}")
            return None


async def fetch_url(url: str, div_id: Optional[str] = None, div_class: Optional[str] = None) -> Optional[str]:
    try:
        async with httpx.AsyncClient() as client:
            # Validate the URL
            if not validators.url(url):
                print(f"Invalid URL: {url}")
                raise InvalidURLException(f'Invalid URL: {url}')
            elif not urlparse(url).scheme.startswith('https'):
                print(f"URL is not secure: {url}")
                raise InsecureURLException(f'URL is not secure: {url}')
            elif not await check_url_safety(url):
                print(f"URL is not safe: {url}")
                raise SusURLException('URL is not safe or is non-existent!')

            # Fetch the URL if everything is OK
            response = await client.get(url)
            response.raise_for_status()  # Raises an exception for 4xx and 5xx responses

            # Parse the HTML content
            soup = BeautifulSoup(response.text, features='html.parser')

            # If a specific <div> tag ID or class is provided, extract only that content
            specific_div = None
            if div_id:
                specific_div = soup.find(name='div', id=div_id)
            elif div_class:
                specific_div = soup.find(name='div', class_=div_class)

            if specific_div:
                return str(specific_div)  # Returns the HTML of the specified <div> tag
            elif div_id or div_class:
                print(f"Specified <div> tag with ID {div_id} or class {div_class} not found")
                return None  # Returns none but they were expecting to find something
            else:
                return response.text  # Returns the entire HTML content as they didn't specify a <div> tag

    except httpx.HTTPError as err:
        print(f"An unhandled HTTP error occurred while fetching the content from the URL provided: {err}")
        raise FetchingError(
            f'An unhandled HTTP error occurred while fetching the content from  the URL provided: {err}')

# Strips the HTML markup from a string
def strip_html_markup(html_content: str) -> str:
    # Parse the HTML content
    soup = BeautifulSoup(html_content, features='html.parser')

    # Extract the plain text content
    text_content = soup.get_text()

    # Remove excessive blank lines
    cleaned_text = re.sub('\n+', '\n', text_content).strip()

    return cleaned_text
