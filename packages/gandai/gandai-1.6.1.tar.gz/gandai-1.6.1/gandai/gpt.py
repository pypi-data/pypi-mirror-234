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


# def get_company_products(domain: str) -> str:
#     domain = ts.helpers.clean_domain(domain)
#     company = ts.query.find_company_by_domain(domain)
#     resp = requests.get(f"http://www.{domain}")
#     soup = BeautifulSoup(resp.text, "html.parser")
#     homepage_text = soup.text.strip()
#     homepage_links = list(set(soup.find_all("a")))
    
#     messages = [
#         {
#             "role": "system",
#             "content": f"You are a helpful assistant evaulating {company.name} for acquisition.",
#         },
#          {
#             "role": "system",
#             "content": f"We need to give the client the products sold by the company.",
#         },
#         {
#             "role": "system",
#             "content": f"Here is homepage text for {homepage_text}",
#         },
#         {
#             "role": "system",
#             "content": f"Here are the links on the homepage: {homepage_links}",
#         },
#         {
#             "role": "user",
#             "content": f"I want to know about the products sold by the company. What are the top 3 links should I visit",
#         },
#         {
#             "role": "user",
#             "content": f"Answer as a Python list of strings. List[str]",
#         },
#     ]
    
    
#     links = ask_gpt4(messages)
#     print(links)
#     for link in links:
#         resp = requests.get(link)
#         soup = BeautifulSoup(resp.text, "html.parser")
#         messages.append({
#             "role": "system",
#             "content": f"Here text for {link}: {soup.text.strip()}",
#         })
#     messages.append({
#             "role": "user",
#             "content": f"What are the products sold by {company.name}?. Answer as a Python list of strings. List[str]",
#         })
#     resp = ask_gpt4(messages)
#     return resp



    

def get_company_products(domain: str) -> str:
    domain = ts.helpers.clean_domain(domain)
    company = ts.query.find_company_by_domain(domain)
    resp = requests.get(f"http://www.{domain}")
    soup = BeautifulSoup(resp.text, "html.parser")
    homepage_text = soup.text.strip()
    
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant evaulating {company.name} for acquisition.",
        },
        {
            "role": "system",
            "content": f"We are need to give our Client the products sold by the company.",
        },
        {
            "role": "system",
            "content": f"Here is homepage text for {homepage_text}",
        },
        {
            "role": "user",
            "content": f"What are the products sold by this company? You will respond with a Python list of strings. List[str]",
        },
    ]
    resp = ask_gpt4(messages)
    return resp


def get_company_services(domain: str) -> str:
    domain = ts.helpers.clean_domain(domain)
    company = ts.query.find_company_by_domain(domain)
    resp = requests.get(f"http://www.{domain}")
    soup = BeautifulSoup(resp.text, "html.parser")
    homepage_text = soup.text.strip()
    print(homepage_text)
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant evaulating {company.name} for acquisition.",
        },
        {
            "role": "system",
            "content": f"We are need to give our Client the services offered by the company.",
        },
        {
            "role": "system",
            "content": f"Here is homepage text from {company.domain}: {homepage_text}",
        },
        {
            "role": "user",
            "content": f"What are the services offered by this company? You will respond with a Python list of strings. List[str]",
        },
    ]
    resp = ask_gpt4(messages)
    return resp

def get_company_customers(domain: str) -> str:
    domain = ts.helpers.clean_domain(domain)
    company = ts.query.find_company_by_domain(domain)
    resp = requests.get(f"http://www.{domain}")
    soup = BeautifulSoup(resp.text, "html.parser")
    homepage_text = soup.text.strip()
    print(homepage_text)
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant evaulating {company.name} located at {company.domain} for acquisition.",
        },
        {
            "role": "system",
            "content": f"We are need to give our Client the type of customers that {company.name} is selling to.",
        },
        {
            "role": "system",
            "content": f"Here is homepage text from {company.domain}: {homepage_text}",
        },
        {
            "role": "user",
            "content": f"What type of customer does this company sell to? You will respond with a Python list of strings. List[str]",
        },
    ]
    resp = ask_gpt4(messages)
    return resp

# def get_suggested_search_phrase(search: models.Search) -> str:
#     # need up update this
#     targets = query.search_targets(search_uid=search.uid).query()
#     resp = ask_gpt(
#         f"What search phrase would you use to search Google Maps to find companies that look like this: {targets['description'].tolist()}",
#         max_tokens=60,
#     )
#     return resp


# def summarize_search_by(targets):
#     px.histogram(targets, x="employees", nbins=20, height=400, width=400).show()

#     print(targets["ownership"].value_counts())

#     GPT_PROMPT = f"""
#     The top three geographic areas, based on the {[desc for desc in targets['description'].dropna().sample(20)]} are:
#     """

#     print(ask_gpt(prompt=GPT_PROMPT))

#     GPT_PROMPT = f"""
#     Give me the company type, products and services, and end markets {[desc for desc in targets['description'].dropna().sample(20)]} are:
#     """

#     print(ask_gpt(prompt=GPT_PROMPT, max_tokens=100))
