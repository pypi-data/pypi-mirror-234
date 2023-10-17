import tiktoken, os, pdb
import pandas as pd
from sqlalchemy import create_engine
#from portageur.plugins.models.chat_models import AzureChatOpenAI
from portageur.plugins.auth.azure import AzureChatOpenAI
from portageur.plugins.prompt.esg_hint import ESGHint
from portageur.kdutils.logger import kd_logger


class News(object):

    def __init__(self):
        self._engine = create_engine(os.environ['SYL_DB'], echo=False)
        self._model = AzureChatOpenAI(temperature=0,
                                      max_tokens=800,
                                      deployment_name="gpt-4",
                                      model_name="gpt-4",
                                      request_timeout=60,
                                      max_retries=2)

    def _num_tokens_from_string(self, string, encoding_name='cl100k_base'):
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def fetch_news(self, code, limit):
        #table = self._base.classes['esg_feed']
        '''
        query = select([
            table.title, table.origin_id, table.url, table.publish_time
        ]).where(
            and_(table.code == code, table.flag == 1, table.effective == 1,
                 table.language.in_(['ENGLISH',
                                     'English']))).order_by(table.publish_time)
        '''
        query = "SELECT title,origin_id, url,publish_time  FROM esg_feed WHERE code='{0}' and flag=1 and effective=1 and language='ENGLISH' ORDER BY publish_time DESC limit {1}".format(
            code, limit)
        result = pd.read_sql(query, self._engine)
        result = result.drop_duplicates(subset=['title'])
        result = result.drop_duplicates(subset=['origin_id'])
        result = result.drop_duplicates(subset=['url'])
        result['publish_time'] = pd.to_datetime(result['publish_time'])
        result['publish_month'] = result['publish_time'].dt.strftime('%b %Y')
        return result

    def _transform_format(self, news_data):
        news_data[
            'text'] = news_data['title'] + ' ' + news_data['publish_month']
        snippets = news_data['text'].dropna().tolist()
        snippets = '|'.join(snippets)
        while self._num_tokens_from_string(snippets) > 2000:
            snippets = snippets[:-50]
        return snippets

    def run(self, code, name, limit):
        kd_logger.info("{0}:fetch {1} news".format(code, limit))
        news_data = self.fetch_news(code=code, limit=limit)

        kd_logger.info("{0}:transform snippets".format(code))
        snippets = self._transform_format(news_data=news_data)
        message = ESGHint.research_news_recent(company_name=name,
                                               seleya_headlines=snippets)

        kd_logger.info("{0}:predict news recent".format(code))
        results = self._model.predict(messages=message)
        return results.content