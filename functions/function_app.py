from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)
from typing import Callable
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
import os
import json  # Import json module to convert dictionary to JSON string

# GPT-4o mini is our most cost-efficient small model that’s smarter and cheaper than GPT-3.5 Turbo, 
# and has vision capabilities. The model has 128K context and an October 2023 knowledge cutoff.
model_to_use="gpt-4o-mini"

import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="translate_http_trigger", methods=["POST"]
def translate_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    language = req.params.get('language')
    if not language:
        return func.HttpResponse(
             "Language parameter must be specified.",
             status_code=400
        )
    text = req.params.get('text')
    if not text:
        return func.HttpResponse(
             "Text parameter must be specified.",
             status_code=400
        )    

    translated = translate_text(text=text, language=language)

    return func.HttpResponse(
        json.dumps({ "LLM Response" : translated }),
        mimetype="application/json")

def llm_call(model, system_template, human_template, param_provider: Callable[[], dict], custom_output_parser) -> str:
    try:
        api_key = os.environ['OPENAI_API_KEY']
        # ranges from 0 to 2, with lower values indicating greater determinism and higher values indicating more randomness.
        temperature=0.7
        # default value is bigger and dependent on model
        max_tokens=2048
        chat_model = ChatOpenAI(model=model, api_key=api_key, temperature=temperature, max_tokens=max_tokens)
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        # Create the LLM chain
        chain = LLMChain(
            llm=chat_model,
            prompt=chat_prompt,
            output_parser=custom_output_parser
        )

        params = param_provider()
        # Run the chain and return the result
        return chain.run(**params)
    except Exception as e:
        # Handle any exceptions that occur during the LLM call
        print(f"An error occurred while calling the LLM: {e}")
        raise e

class CustomOutputParser(BaseOutputParser):
    def parse(self, text: str):
        return text

def translate_text(text: str, language: str) -> str:
    param_provider = lambda: {"text": text, "language": language}
    return llm_call(
        model=model_to_use,
        system_template = (
            "You're a helpful translator assistant who translates the provided {text} into specified {language}."
            "A user will pass in a text and language that this text should be translated to. Make sure that the meaning of the translated text is as closer as possible to the original text"
            "Return this text in form useful for museums brochures."
        ),
        human_template="Text: {text}\nLanguage: {language}",
        param_provider=param_provider,
        custom_output_parser= CustomOutputParser())    