import os, asyncio

os.environ['PB_SERVER_URL'] = 'app.portageb.com'
os.environ['seleya_username'] = 'flaght@gmail.com'
os.environ['seleya_password'] = '123456@'

os.environ['SYL_DB'] = \
    'mysql+mysqlconnector://molecule:tr7XKeNmmzjdxfY2@10.0.0.4:12306/portagebay'
os.environ['SELEYAWARNINGS'] = '1'

#os.environ['OPENAI_API_TYPE'] = 'azure'
#os.environ['OPENAI_API_KEY'] = '6c5231138be14017ac2a06bb27ccb4cd'
#os.environ['OPENAI_API_BASE'] = 'https://seleyaopenai.openai.azure.com/'
#os.environ['OPENAI_API_VERSION'] = '2023-05-15'
os.environ['SERPER_API_KEY'] = '8097262ac2c7440ea4f7a694abf5af7dc40cf05e'
os.environ['VALUE_SERPER_API_KEY'] = 'CD1E74E442294421A0B31F31A5E39B5B'
os.environ["BING_SUBSCRIPTION_KEY"] = "6080aec710e44c939b8c833fcc15a451"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
os.environ['USER_FILE'] = '/workspace/molecule/config.yml'

import time, pdb
from enum import Enum
import pandas as pd
#from portageur.plugins.models.chat_models import AzureChatOpenAI
from portageur.plugins.auth.azure import AzureChatOpenAI
from portageur.plugins.serper import serper_bing
from portageur.plugins.prompt.esg_hint import ESGHint
from portageur.plugins.prompt.esg_controversy import ESGControversy
from portageur.kdutils.logger import kd_logger


class Method(Enum):
    SYNC = 0
    AYSN = 1


class Concerns(object):

    def __init__(self, search_terms, method=0):
        self._search_terms = search_terms
        self._method = method
        self._model = AzureChatOpenAI(temperature=0,
                                      max_tokens=800,
                                      deployment_name="gpt-4",
                                      model_name="gpt-4",
                                      request_timeout=60,
                                      max_retries=2)

    def _serper_data(self, name, controversy_dict, citationmap_dict):
        for search_term in self._search_terms:
            query = f'{name} {search_term}'
            try:
                controv, citation_map = serper_bing(query=query,
                                                    citation_start=0 + 1)
                controversy_dict[search_term] = controv
                citationmap_dict[search_term] = citation_map
            except Exception as e:
                kd_logger.error(e)

    '''
    def _predict_summary(self, name, controversy_dict):
        results_map = {}
        for search_term in controversy_dict.keys():
            message = ESGHint.research_assistant_summary(
                company_name=name,
                controv=controversy_dict[search_term],
                search_term=search_term)
            results = self._model.predict(messages=message)
            print(results)
            results_map[search_term] = results.content
        return results_map
    '''

    async def task(self, search_term, controv):
        print("++++{0}".format(search_term))
        message = ESGHint.research_assistant_summary(company_name=name,
                                                     controv=controv,
                                                     search_term=search_term)
        await asyncio.sleep(1)
        results = self._model.predict(messages=message)
        print("===>{0}\n".format(results))
        return results

    async def _pred_summary(self, controversy_dict):
        await asyncio.gather(
            self.task('Controversies or Investor concerns',
                      controversy_dict['Controversies or Investor concerns']),
            self.task('Social concerns', controversy_dict['Social concerns']))

    def _predict_summary(self, name, controversy_dict):
        pdb.set_trace()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._pred_summary(controversy_dict))
        print('-->')

    def _summary_match_sources(self, name, results_map, citationmap_dict,
                               controversy_dict):
        sources_res = []
        for search_term in controversy_dict.keys():
            kd_logger.info("start {0} match search term: {1}".format(
                name, search_term))
            answer = results_map[search_term]
            citation_map = citationmap_dict[search_term]
            controversy = controversy_dict[search_term]
            # md_str = ESGControversy.match_sources(answer, citation_map)
            answer_new, citation_map_new = ESGControversy.match_sources_and_format(
                answer, citation_map)
            # if len(md_str) > 0:
            #     answer += f"\nSources: \n{md_str}"
            cache_data = {
                'task': 'controversy',
                'tag': search_term,
                'answer': answer_new,
                'controversy': controversy,
                'citation_map': citation_map_new,
                'latest_time': int(time.time())
            }
            sources_res.append(cache_data)
        return sources_res

    def predict_content(self, name, controversy_dict, citationmap_dict):
        kd_logger.info("start {0} serper data ".format(name))
        self._serper_data(name=name,
                          controversy_dict=controversy_dict,
                          citationmap_dict=citationmap_dict)

        kd_logger.info("start {0} predict summary".format(name))
        results_map = self._predict_summary(name=name,
                                            controversy_dict=controversy_dict)
        return results_map

    def _predict_overall(self, name, results_map):
        research_md = ""
        for search_term in results_map.keys():
            current_md = results_map[search_term]
            research_md += current_md + "\n\n"
        message = ESGHint.research_esg_overall(company_name=name,
                                               research_md=research_md)
        kd_logger.info("start {0} predict overall".format(name))
        results = self._model.predict(messages=message)
        return results.content

    def _overall_match_sources(self, name, overall, controversy_dict,
                               citationmap_dict):
        flat_citemap = {
            k: v
            for d in citationmap_dict.values()
            for k, v in d.items()
        }
        kd_logger.info("start {0} match overall".format(name))
        # md_str = ESGControversy.match_sources(overall, flat_citemap)
        answer_new, citation_map_new = ESGControversy.match_sources_and_format(
            overall, flat_citemap)
        # if len(md_str) > 0:
        #     overall += f"\n\nSources: \n{md_str}"
        cache_data = {
            'task': 'controversy',
            'tag': 'overall',
            'answer': answer_new,
            'citation_map': citation_map_new,
            'controversy': controversy_dict,
            'latest_time': int(time.time())
        }
        return cache_data

    def run(self, code, name):
        controversy_dict = {}
        citationmap_dict = {}

        results_map = self.predict_content(name=name,
                                           controversy_dict=controversy_dict,
                                           citationmap_dict=citationmap_dict)
        '''
        summary = self._summary_match_sources(
            name=name,
            results_map=results_map,
            citationmap_dict=citationmap_dict,
            controversy_dict=controversy_dict)

        results = self._predict_overall(name=name, results_map=results_map)

        overall = self._overall_match_sources(
            name=name,
            overall=results,
            controversy_dict=controversy_dict,
            citationmap_dict=citationmap_dict)

        summary = pd.DataFrame(summary)
        overall = pd.DataFrame([overall])
        return pd.concat([summary, overall], axis=0)
        '''


search_terms = ['Controversies or Investor concerns', 'Social concerns']
name = 'Microsoft'
code = 'MSFT.OQ'
en = Concerns(search_terms=search_terms)
results = en.run(name=name, code=code)

print(results)