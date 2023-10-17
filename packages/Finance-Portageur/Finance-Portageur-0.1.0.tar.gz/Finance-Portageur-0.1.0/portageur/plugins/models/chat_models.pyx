# -*- coding: utf-8 -*-
from portageur.plugins.models.base import create_model_base
from langchain.chat_models import AzureChatOpenAI as AzureChatOpenAIImpl
from langchain.chat_models import ChatOpenAI as ChatOpenAIImpl
from langchain.chat_models import ChatGooglePalm as ChatGooglePalmImpl


class AzureChatOpenAI(create_model_base('chat_models')):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.impl = AzureChatOpenAIImpl(**kwargs)

    def save(self):
        return super().save()


class ChatOpenAI(create_model_base('chat_models')):

    def __init__(self, **kwargs):
        super().__init__()
        self.impl = ChatOpenAIImpl(**kwargs)

    def save(self):
        return super().save()


class ChatGooglePalm(create_model_base('chat_models')):

    def __init__(self, **kwargs):
        super().__init__()
        self.impl = ChatGooglePalm(**kwargs)

    def save(self):
        return super().save()
