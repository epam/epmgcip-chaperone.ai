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

# GPT-4o mini is our most cost-efficient small model that’s smarter and cheaper than GPT-3.5 Turbo, 
# and has vision capabilities. The model has 128K context and an October 2023 knowledge cutoff.
model_to_use="gpt-4o-mini"

class CustomOutputParser(BaseOutputParser):
    def parse(self, text: str):
        return text

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

def generate_description(category: str, keyWords: list[str]) -> str:
    param_provider = lambda: {"category": category, "keyWords": ", ".join(keyWords)}
    return llm_call(
        model=model_to_use,
        system_template = (
            "You're a helpful assistant who generates 1-2 paragraph description on the {category}. Also, ensure mentioned keywords are also used."
            "A user will pass in a {category} and {keywords}, and you should generate 1-2 paragraphs of the text in that {category} "
            "Return this text in form useful for museums brochures."
        ),
        human_template="Category: {category}\nKeyWords: {keyWords}",
        param_provider=param_provider,
        custom_output_parser= CustomOutputParser())

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

# Example of usage
if __name__ == "__main__":

    language = "Belarussian"
    text = ("Художественное образование Уфимцев получил на курсах рисования и живописи при Омском рабочем институте практических знаний (1917-1918).Посещение творческого вечера Д.Бурлюка в 1918 году, произошедшее в Омске, послужило началом его увлечения футуризмом и стало основой для его дальнейших творческих поисков, которыми характеризуется его работы 1920-х -1930-х годов."
"В своей жизни сибиряк Уфимцев оказался тесно связан со Средней Азией. Первый раз он приехал сюда в 1923 году и через два года вернулся к себе в Омск. В конце 1920-х годов он неоднократно посещал Среднюю Азию, а в 1933 переехал в Ташкент на постоянное место жительства."
"Картина «Чаепитие» это яркий пример модернистских исканий художника: она выполнена в стиле неопримитивизма с использованием техники аппликации (войлок, ткань, дерево)."
"В передаче образа «Автопортрет» представляет редкое сочетание стилистики модерна и иконографии иконописи. Именно о такой манере письма говорил близкий друг художника отец Павел Флоренский, как о «реализме сущностном, избегающим натурализма, реализме с превалированием духовного начала»."
"Комаровский, хорошо знакомый с технологией написания икон, в данном автопортрете сумел воспроизвести характеристики иконописной доски (в частности, вертикальная полоса на портрет изображает трещину на доске иконы)."
"В 1937 году В. А.Комаровский, не скрывавший своих религиозных взглядов, был обвинен в монархическом заговоре и расстрелян."
"Не закончив юридическое образование в Петербургском университете, Василий Комаровский заинтересовался изобразительным искусством. В 1910 году он впервые близко познакомился с русской иконописью и стал подробно изучать технологию и иконографию иконописи. Уже с 1912 года он стал самостоятельно писать иконы и оформлять храмы. После революции 1917 года Василий Алексеевич продолжал работать как иконописец, постоянно подвергаясь различным преследованиям и арестам со стороны советской власти.")

    result = translate_text(text, language)
    print(result)