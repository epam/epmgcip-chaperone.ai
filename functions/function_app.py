from langchain.chat_models import AzureChatOpenAI
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

import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="translate_http_trigger", methods=["POST"])
def translate_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    language = req.params.get('language')
    if not language:
        return func.HttpResponse(
             "Language parameter must be specified.",
             status_code=400
        )
    text = req.get_body()
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
        # ranges from 0 to 2, with lower values indicating greater determinism and higher values indicating more randomness.
        temperature=0.7
        # default value is bigger and dependent on model
        max_tokens=2048
        logging.info('Starting LLM call')
        logging.info('MODEL type %s', os.getenv('MODEL'))
        logging.info('api type %s', os.getenv('OPENAI_API_TYPE'))
        logging.info('key %s', os.getenv('OPENAI_API_KEY'))
        logging.info('url %s', os.getenv('OPENAI_API_BASE'))
        
        chat_model = AzureChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        logging.info('model %s', chat_model)
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        logging.info('Creating LLM chain')
        # Create the LLM chain
        chain = LLMChain(
            llm=chat_model,
            prompt=chat_prompt,
            output_parser=custom_output_parser
        )

        params = param_provider()
        logging.info('Running LLM chain')
        # Run the chain and return the result
        return chain.run(**params)
    except Exception as e:
        # Handle any exceptions that occur during the LLM call
        logging.info('An error occurred while calling the LLM %s', e)
        print(f"An error occurred while calling the LLM: {e}")
        raise e

class CustomOutputParser(BaseOutputParser):
    def parse(self, text: str):
        return text

def translate_text(text: str, language: str) -> str:
    param_provider = lambda: {"text": text, "language": language}
    model_to_use = os.environ['MODEL']

    return llm_call(
        model=model_to_use,
        system_template = (
            "You're a helpful translator assistant who translates the provided {text} into specified {language}."
            "A user will pass in a text in HTML format and language that this text should be translated to. Make sure that the meaning of the translated text is as closer as possible to the original text and preserve HTML structure"
            "Return this text in HTML format in form useful for museums brochures."
        ),
        human_template="Text: {text}\nLanguage: {language}",
        param_provider=param_provider,
        custom_output_parser= CustomOutputParser())    