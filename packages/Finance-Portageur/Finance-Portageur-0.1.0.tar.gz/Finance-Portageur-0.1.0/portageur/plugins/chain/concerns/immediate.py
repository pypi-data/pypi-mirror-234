import time, pdb
import pandas as pd
#from portageur.plugins.models.chat_models import AzureChatOpenAI
from portageur.plugins.auth.azure import AzureChatOpenAI
from portageur.plugins.serper import serper_bing
from portageur.plugins.prompt.esg_hint import ESGHint
from portageur.plugins.prompt.esg_controversy import ESGControversy
from portageur.kdutils.logger import kd_logger


class Immediate(object):

    def __init__(self, search_terms):
        self._search_terms = search_terms
        self._model = AzureChatOpenAI(temperature=0,
                                      max_tokens=800,
                                      deployment_name="gpt-4",
                                      model_name="gpt-4",
                                      request_timeout=60,
                                      max_retries=2)

    def _serper_data(self, name, controversy_dict, citationmap_dict):
        for search_idx, search_term in enumerate(self._search_terms):
            query = f'{name} {search_term}'
            try:
                # start scrapping controversies,
                # the default offset 15 articles is applied to ensure unique citation number
                controv, citation_map = serper_bing(query=query,
                                                    citation_start=(1+15*search_idx))
                controversy_dict[search_term] = controv
                citationmap_dict[search_term] = citation_map
            except Exception as e:
                kd_logger.error(e)

    def _predict_summary(self, name, controversy_dict):
        results_map = {}
        for search_term in controversy_dict.keys():
            message = ESGHint.research_assistant_summary(
                company_name=name,
                controv=controversy_dict[search_term],
                search_term=search_term)
            results = self._model.predict(messages=message)
            results_map[search_term] = results.content
        return results_map

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
        # consolidate all the citation map together, there should not be duplicates
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
