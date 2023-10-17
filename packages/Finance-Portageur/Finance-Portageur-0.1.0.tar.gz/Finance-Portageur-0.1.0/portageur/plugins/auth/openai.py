import yaml
from dataclasses import dataclass
from plugins.auth.base import BaseAuth, ChatModelManager


@dataclass
class OpenAIAuth(BaseAuth):
    auth_index: int
    api_key: str


class OpenAIChatManager(ChatModelManager):
    endpoints = {
        'completions': 'https://api.openai.com/v1/completions',
        'embeddings': 'https://api.openai.com/v1/embeddings',
        'chat_completions': 'https://api.openai.com/v1/chat/completions'
    }
    name = 'openai'

    def __init__(self, config_path):
        self.auth_config(config_path=config_path)

    def auth_config(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        openai_config = config.get('openai', {})
        self.auths = super(OpenAIChatManager,
                           self).auth_config(openai_config, OpenAIAuth)
