# -*- coding: utf-8 -*-
from portageur.plugins.models.base import create_model_base
from langchain.llms import OpenAI as OpenAIImpl
from langchain.llms import AzureOpenAI as AzureOpenAIImpl
from langchain.llms import OpenAIChat as OpenAIChatImpl
from langchain.llms import GPT4All as GPT4AllImpl
from langchain.llms import HuggingFacePipeline as HuggingFacePipelineImpl


class OpenAI(create_model_base('llms')):

    def __init__(self, **kwargs):
        super().__init__()
        self.impl = OpenAIImpl(**kwargs)

    def save(self):
        return super().save()


class OpenAIChat(create_model_base('llms')):

    def __init__(self, **kwargs):
        super().__init__()
        self.impl = OpenAIChatImpl(**kwargs)

    def save(self):
        return super().save()


class AzureOpenAI(create_model_base('llms')):

    def __init__(self, **kwargs):
        super().__init__()
        self.impl = AzureOpenAIImpl(**kwargs)

    def save(self):
        return super().save()


class HuggingFacePipeline(create_model_base('llms')):

    def __init__(self, **kwargs):
        super().__init__()
        self.impl = HuggingFacePipelineImpl(**kwargs)

    def save(self):
        return super().save()


class GPT4All(create_model_base('llm')):

    def __init__(self, **kwargs):
        super().__init__()
        self.impl = GPT4AllImpl(**kwargs)

    def save(self):
        return super().save()
