import openai
import plotly.express as px
import requests
from bs4 import BeautifulSoup

import gandai as ts

openai.api_key = ts.secrets.access_secret_version("OPENAI_KEY")

## gpt4


def ask_gpt4(messages: list):
    response = openai.ChatCompletion.create(
        model="gpt-4", messages=messages, temperature=0.0
    )
    return response.choices[0]["message"]["content"]


def ask_gpt35(messages: list):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", messages=messages, temperature=0.0
    )
    print(response['usage'])
    return response.choices[0]["message"]["content"]


## gpt3


def ask_gpt(prompt: str, max_tokens: int = 60):
    response = openai.Completion.create(
        engine="text-davinci-003",  # or "text-curie-003" for a less expensive engine
        prompt=prompt,
        max_tokens=max_tokens,
    )

    return response.choices[0].text.strip()


def get_top_zip_codes(area: str, top_n: int = 25) -> list:
    resp = ask_gpt(
        f"As a python array List[str], the top {top_n} zip codes in {area} are:",
        max_tokens=1000,
    )
    return eval(resp)[0:top_n]  # top_n of 1 was giving me a ton of results


