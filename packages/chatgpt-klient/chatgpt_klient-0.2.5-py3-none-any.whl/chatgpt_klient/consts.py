NO_AUTH_MSG = """
For this script to work, authentication to OpenAI is needed. This should be provided in one of the following 3 ways:
    1. Pass valid authentication data via the --key option.
    2. Use the --config option to point to a valid JSON with the "api_key" field.
    3. Set the environment variable OPENAI_CONFIGFILE pointing to a valid JSON file with the "api_key" field.
"""

INVALID_JSON_MSG = """
The config file should be in a valid JSON format like the following:
{
    "api_key": "dk39??!meerLq"
}
"""

LEGACY_ENGINES = [
    "davinci",
    "text-davinci-003",
    "text-davinci-002",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]

CHAT_ENGINES = [
    "gpt-4",
    "gpt-4-32k",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k"
]

MAX_TOKENS = {
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "text-davinci-003": 4096,
    "text-davinci-002": 4096,
    "davinci": 4096,
    "text-curie-001": 2048,
    "text-babbage-001": 2048,
    "text-ada-001": 2048,
}

MAX_DELAY = 500
