import copy
import openai
from openai import error
import math
import time
from openai.error import RateLimitError
import tiktoken
import time
from logutils import get_logger
from chatgpt_klient.consts import MAX_TOKENS, LEGACY_ENGINES, CHAT_ENGINES, MAX_DELAY
from chatgpt_klient.exceptions import (
    InvalidAPIKeyError,
    InvalidModelError,
    InvalidResponseError,
)
from rich.console import Console

logger = get_logger("chatgpt_client")
console = Console()


class ChatGPTPrompt:
    def __init__(self, api_key, engine="gpt-3.5-turbo-16k", cap_tokens=math.inf):
        self.api_key = api_key
        self.openai = openai
        self.openai.api_key = self.api_key
        self.check_api_key_validity()
        self.msg_history = {"messages": [], "tokens": []}
        self.last_prompt_tokens = 0
        self.cap_tokens = cap_tokens
        self.set_engine(engine)

    def list_models(self):
        return LEGACY_ENGINES + CHAT_ENGINES

    def check_api_key_validity(self):
        try:
            r = self.openai.Completion.create(
                model="davinci",
                prompt="Hi",
                max_tokens=5,
            )
            r = self.check_response_validity(r, "davinci")
        except Exception:
            logger.error("Invalid API key.")
            raise InvalidAPIKeyError(
                "Your API key does not seem to be valid. Please check it."
            )
        else:
            logger.info("API key seems valid and working.")

    def check_model_validity(self):
        if self.engine not in self.list_models():
            logger.error(f"Engine {self.engine} is not supported")
            raise InvalidModelError(f"Engine {self.engine} not supported")
        try:
            if self.engine in LEGACY_ENGINES:
                r = self.openai.Completion.create(
                    model=self.engine,
                    prompt="Hi",
                    max_tokens=5,
                )
                if type(r) is not dict:
                    raise Exception
                else:
                    logger.debug(f'Model validity test: {r["choices"][0]["text"]}')
            elif self.engine in CHAT_ENGINES:
                r = self.openai.ChatCompletion.create(
                    model=self.engine,
                    messages=[{"role": "user", "content": "Hi"}],
                    max_tokens=5,
                )
                r = self.check_response_validity(r)
                logger.debug(
                    f'Model validity test: {r["choices"][0]["message"]["content"]}'
                )
            else:
                raise InvalidModelError(f"Engine {self.engine} not supported")
        except Exception:
            logger.info(f"Invalid model ({self.engine}) for your API key")
            raise InvalidModelError(f"Engine {self.engine} not supported")
        else:
            logger.info(f"Model ({self.engine}) seems to be valid.")

    def check_response_validity(self, r, engine=None) -> dict:
        if engine is None:
            engine = self.engine
        try:
            if engine in LEGACY_ENGINES:
                content = r["choices"][0]["text"]
            elif engine in CHAT_ENGINES:
                content = r["choices"][0]["message"]["content"]
            else:
                raise InvalidModelError
        except Exception:
            raise InvalidResponseError(f"Response is not well formed: {r}")
        else:
            logger.debug("Response seems to be well formed")
            return r

    def set_engine(self, engine: str):
        self.engine = engine
        self.check_model_validity()
        self.encoding = tiktoken.encoding_for_model(self.engine)
        self.max_tokens = int(MAX_TOKENS[self.engine] / 2)

    def set_system_directive(self, directive: str):
        self.clean_history(keep_sysdir=False)
        self.msg_history["messages"].append(
            {
                "role": "system",
                "content": directive,
            }
        )
        self.msg_history["tokens"].append(len(self.encoding.encode(directive)))

    def clean_history(self, keep_sysdir=True):
        new_history = {"messages": [], "tokens": []}
        if keep_sysdir:
            for i, m in enumerate(self.msg_history["messages"]):
                if m["role"] == "system":
                    new_history["messages"].append(
                        {"role": m["role"], "content": m["content"]}
                    )
                    new_history["tokens"].append(self.msg_history["tokens"][i])
            self.msg_history = new_history
        self.last_prompt_tokens = 0

    def get_max_tokens_allowed(self):
        return min([self.max_tokens, MAX_TOKENS[self.engine], self.cap_tokens]) - 10

    def calculate_prompt_tokens(self, text, no_history=True, keep_sysdir=False):
        aux_history = copy.deepcopy(self.msg_history)
        aux_last_prompt = self.last_prompt_tokens
        if no_history:
            self.clean_history(keep_sysdir=keep_sysdir)
        self.msg_history["messages"].append(
            {
                "role": "user",
                "content": text,
            }
        )
        self.msg_history["tokens"].append(len(self.encoding.encode(text)))
        potential_tokens = self.msg_history["tokens"][-1] + self.last_prompt_tokens
        if no_history:
            self.msg_history = aux_history
            self.last_prompt_tokens = aux_last_prompt
        return potential_tokens

    def send_prompt(self, text=None, no_history=False, delay=5):
        response = "No response"
        if self.engine in LEGACY_ENGINES:
            r = self.openai.Completion.create(
                engine=self.engine,
                prompt=text,
                max_tokens=self.get_max_tokens_allowed(),
            )
            r = self.check_response_validity(r)
            response = r["choices"][0]["text"]
        elif self.engine in CHAT_ENGINES:
            if text:
                if no_history:
                    self.clean_history()
                self.msg_history["messages"].append(
                    {
                        "role": "user",
                        "content": text,
                    }
                )
                self.msg_history["tokens"].append(len(self.encoding.encode(text)))
            potential_tokens = self.msg_history["tokens"][-1] + self.last_prompt_tokens
            logger.debug(f"Potential tokens: {potential_tokens}")
            while potential_tokens > self.get_max_tokens_allowed():
                logger.warning("Too many tokens. Reducing history size")
                aux = {"messages": [], "tokens": []}
                first_user = True
                first_assistant = True
                for i in range(len(self.msg_history["messages"])):
                    if self.msg_history["messages"][i]["role"] == "user" and first_user:
                        first_user = False
                        potential_tokens -= self.msg_history["tokens"][i]
                    elif (
                        self.msg_history["messages"][i]["role"] == "assistant"
                        and first_assistant
                    ):
                        first_assistant = False
                        potential_tokens -= self.msg_history["tokens"][i]
                    else:
                        aux["messages"].append(self.msg_history["messages"][i])
                        aux["tokens"].append(self.msg_history["tokens"][i])
                self.msg_history = aux
            if text not in [m["content"] for m in self.msg_history["messages"]]:
                raise TooManyTokensError(
                    f"The maximum accepted tokens ({self.get_max_tokens_allowed()}) is not big enough to process your prompt"
                )

            try:
                r = self.openai.ChatCompletion.create(
                    model=self.engine,
                    messages=self.msg_history["messages"],
                    max_tokens=self.get_max_tokens_allowed(),
                    request_timeout=300,
                )
                logger.debug(r)
                r = self.check_response_validity(r)
                self.last_prompt_tokens = r["usage"]["total_tokens"]
                response = r["choices"][0].message.content
                if response:
                    self.msg_history["messages"].append(
                        {
                            "role": "assistant",
                            "content": response,
                        }
                    )
                    self.msg_history["tokens"].append(
                        len(self.encoding.encode(response))
                    )
            except RateLimitError:
                logger.warning(f"Rate limit reached, delaying request {delay} seconds")
                if delay > MAX_DELAY:
                    raise Exception(
                        "Recurring RateLimitError and delaying requests not working"
                    )
                time.sleep(delay)
                response = self.send_prompt(
                    text, no_history=no_history, delay=delay * 2
                )
            except openai.InvalidRequestError as e:
                if "maximum context length" in str(e):
                    self.clean_history(keep_sysdir=True)
                    response = self.send_prompt(text, delay=delay * 2)
                else:
                    logger.warning("We shouldn't be getting here!")
                    raise e
            except error.Timeout:
                logger.warning("Request failed with timeout, retrying")
                if delay > MAX_DELAY:
                    raise Exception("Getting timeouts to all requests")
                time.sleep(delay)
                response = self.send_prompt(
                    text, no_history=no_history, delay=delay * 2
                )

        else:
            logger.warning(f"Engine {self.engine} not supported")
        return response

    def interactive_prompt(self, system_directive: str | None = None, max_tokens=None):
        if system_directive:
            self.set_system_directive(system_directive)
        console.print("###########", style="bold")
        console.print("# ChatGPT #", style="bold")
        console.print("###########", style="bold")
        console.print(
            f"[bold yellow]Engine:[/bold yellow] {self.engine}", highlight=False
        )
        console.print("[bold cyan]Enter 'q'/'quit' to exit the chat[/]")
        console.print("[bold cyan]Enter anything to start chatting.[/]")
        console.print()
        while True:
            input_text = input("$ ")
            if input_text in ("q", "quit"):
                print("ChatGPT> Sayonara, baby!")
                break
            try:
                r = self.send_prompt(text=input_text, max_tokens=max_tokens)
            except RateLimitError:
                logger.warning("You are sending requests too fast. Delaying 20s...")
                time.sleep(20)
                r = self.send_prompt(text=input_text, max_tokens=max_tokens)

            console.print(f"[bold green]ChatGPT>[/] [green]{r}[/]")
            self.msg_history["messages"].append(
                {
                    "role": "assistant",
                    "content": r,
                }
            )
            self.msg_history["tokens"].append(len(self.encoding.encode(r)))


class TooManyTokensError(Exception):
    pass
