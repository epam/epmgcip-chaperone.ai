from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

# ensure that env

def generate_description(category: str, keyWords: list[str]) -> str:
    try:
        chat_model = ChatOpenAI()

        system_template = (
            "You're a helpful assistant who generates 1-2 paragraph description on the category. Also, ensure mentioned keywords are also used."
            "A user will pass in a category and keywords, and you should generate 1-2 paragraphs of the text in that category "
            "Return this text in form useful for museums brochures."
        )
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

        # Define the human message template
        human_template = "Category: {category}\nKeyWords: {keyWords}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # Create the chat prompt template
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        # Define the output parser
        class CommaSeparatedListOutputParser(BaseOutputParser):
            def parse(self, text: str):
                return text # format/validate output?

        # Create the LLM chain
        chain = LLMChain(
            llm=chat_model,
            prompt=chat_prompt,
            output_parser=CommaSeparatedListOutputParser()
        )

        # Run the chain and return the result
        return chain.run(category=category, keyWords=keyWords)
    except Exception as e:
        # Handle any exceptions that occur during the LLM call
        print(f"An error occurred while calling the LLM: {e}")
        return []

# Example usage
if __name__ == "__main__":
    result = generate_description("Ancient Rome", ["Caesar", "Legion", "Coliseum"])
    print(result)