from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='TeLLMgramBot',
    version='1.4.0',
    packages=find_packages(),
    license='MIT',
    author='Digital Heresy',
    author_email='ronin.atx@gmail.com',
    description='OpenAI GPT, driven by Telegram',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Digital-Heresy/TeLLMgramBot',
    install_requires=[
        'openai',
        'PyYAML',
        'httpx',
        'beautifulsoup4',
        'typing',
        'validators',
        'python-telegram-bot',
        'tiktoken'
    ],
    python_requires='>=3.10',
)
