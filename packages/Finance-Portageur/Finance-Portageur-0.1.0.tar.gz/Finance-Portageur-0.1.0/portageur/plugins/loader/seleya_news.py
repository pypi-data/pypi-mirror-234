import datetime
import pandas as pd
import tiktoken
from pydantic.class_validators import root_validator
from pydantic.main import BaseModel

from langchain.utils import get_from_dict_or_env
from seleya import *


class SeleyaControversies(BaseModel):
    """Wrapper aound the seleya controversy api"""

    def __init__(self):
        super().__init__()
        self._sly_engine = DBFetchEngine.create_engine('sly')

    def _num_tokens_from_string(self, string, encoding_name='cl100k_base'):
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def run(self, company_code: str, max_len=2000, date_delta=100) -> str:
        """Run controversies query."""
        results = self._query_controversies(company_code, date_delta)
        results['text'] = results['title'] + ' ' + results['publish_month']
        snippets = results['text'].dropna().tolist()
        snippets = '|'.join(snippets)

        while self._num_tokens_from_string(snippets) > max_len:
            snippets = snippets[:-50]

        return snippets

    def _query_controversies(self, company_code, date_delta) -> str:
        end_date = datetime.date.today().strftime('%Y-%m-%d')
        delta = datetime.timedelta(days=date_delta)
        begin_date = (datetime.date.today() - delta).strftime('%Y-%m-%d')

        result = ESGFeedFactory(self._sly_engine).result(codes=['BP.L'], key='source',
                                                    categories=['gdelt', 'refintiv', 'anrefin'], begin_date=begin_date,
                                                    end_date=end_date,
                                                    columns=['publish_time', 'code', 'title', 'origin_id', 'source'],
                                                    limit=10000)
        if len(result) == 0:
            return 'No controversies found. Please try other tools'
        result = result.drop_duplicates(subset=['title'])
        result = result.drop_duplicates(subset=['origin_id'])
        result = result.drop_duplicates(subset=['url'])
        result['publish_time'] = pd.to_datetime(result['publish_time'])
        result['publish_month'] = result['publish_time'].dt.strftime('%b %Y')
        return result
