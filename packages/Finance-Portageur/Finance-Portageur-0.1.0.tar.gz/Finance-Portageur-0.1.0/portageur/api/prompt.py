# -*- coding: utf-8 -*
from portageur.plugins.prompt.esg_hint import ESGHint
from portageur.plugins.prompt.employee_hint import EmployeesHint
from portageur.plugins.prompt.esg_controversy import ESGControversy
from portageur.plugins.prompt.base import PromptsMessage


def prompts_summary(company_name, controv, search_term):
    return ESGHint.research_assistant_summary(company_name=company_name,
                                              controv=controv,
                                              search_term=search_term)


def prompts_overall(company_name, research_md):
    return ESGHint.research_esg_overall(company_name=company_name,
                                        research_md=research_md)


def prompts_news(company_name, seleya_headlines):
    return ESGHint.research_news_recent(company_name=company_name,
                                        seleya_headlines=seleya_headlines)


def prompts_single_reviews():
    return EmployeesHint.employess_single_reviews()


def match_sources(results, citation_map):
    return ESGControversy.match_sources(results=results,
                                        citation_map=citation_map)


def match_sources_and_format(results, citation_map):
    return ESGControversy.match_sources_and_format(results=results,
                                                   citation_map=citation_map)
