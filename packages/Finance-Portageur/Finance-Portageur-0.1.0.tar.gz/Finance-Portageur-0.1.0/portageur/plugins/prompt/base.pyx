from enum import Enum
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain import PromptTemplate

class PromptsMessage(Enum):
    Template = 0
    HumanTemplate = 1
    ChatTemplate = 2
    System = 3
    Human = 4
    Function = 5


def transformer(query, method, **kwargs):
    if method == PromptsMessage.Template:
        return PromptTemplate(template=query, input_variables=kwargs["variables"])
    elif method == PromptsMessage.HumanTemplate:
        return HumanMessagePromptTemplate.from_template(query)
    elif method == PromptsMessage.ChatTemplate:
        return ChatPromptTemplate.from_messages(query)
    elif method == PromptsMessage.Human:
        return HumanMessage(content=query)
    elif method == PromptsMessage.System:
        return SystemMessage(content=query)
