# -*- coding: utf-8 -*
import pdb
from portageur.kdutils.division.lazy import LazyFunc
from portageur.plugins.prompt.base import transformer, PromptsMessage


class ESGHint(object):

    @classmethod
    def research_assistant_summary(cls, company_name, controv, search_term):
        human_message = cls.query_summary(company_name=company_name,
                                          controv=controv,
                                          search_term=search_term,
                                          method=PromptsMessage.Human)
        system_message = cls.research_assistant_topic()
        return [system_message, human_message]

    @classmethod
    def research_esg_overall(cls, company_name, research_md):
        human_message = cls.query_overall(company_name=company_name,
                                          research_md=research_md,
                                          method=PromptsMessage.Human)

        system_message = cls.research_assistant_overall()
        return [system_message, human_message]

    @classmethod
    def research_news_recent(cls, company_name, seleya_headlines):
        human_message = cls.query_recent(company_name=company_name, seleya_headlines=seleya_headlines,
                                         method=PromptsMessage.Human)
        system_message = cls.research_assistant()
        return [system_message, human_message]

    @classmethod
    def research_assistant(self):
        query = "You are a research assistant that helps with analyzing information about companies."
        return transformer(query=query, method=PromptsMessage.System)

    @classmethod
    def research_assistant_topic(self):
        query = """You are a research assistant that helps with analyzing information about companies.
                    Please focus your research on issues and events that can be of concern to investors.
                    Please be objective and critical of the research subject.
                    Please exclude stale events that occurred before 2010.
                    Please refrain from reading into any articles that are overly positive about the subject, e.g., puff pieces and company affiliated website.
                    If you cannot find any relevant information, please respond with "No information found." """
        return transformer(query=query, method=PromptsMessage.System)

    @classmethod
    def research_assistant_overall(self):
        query = """You are a research assistant that helps with analyzing information about companies.
                    Please focus your research on issues and events that can be of concern to investors.
                    Please be objective and critical of the research subject.
                    Please exclude stale events that occurred before 2010.
                    Please refrain from including information that are overly positive about the subject, e.g., puff pieces and company affiliated websites.
                    If you cannot find any relevant information, please respond with "No information found." """
        return transformer(query=query, method=PromptsMessage.System)

    @classmethod
    def query_overall(cls, company_name, research_md, method):
        overall_query = f"""
                Your task is to summarize a few research pieces about {company_name} and its subsidiaries, delimited by triple quotes.
                Please extract and summarize at most 5 the MOST important events and controversies mentioned and leave out the trivial ones like company initiatives and commitments.
                Do not include all information from the research pieces.
                Please respond in about 250 words in concise and professional tone in markdown format.
                Please present your findings in one master list with bullet points and sub-bullet points.
                Please highlight item headers and important phrases in bold.
                Please include details like dates, location, fines, key parties if available.
                Please keep each item in the list to be less than 40 words.
                Please keep and consolidate the source citations (e.g. [^12^]) for each item.
                Please do not append a citation list in the end.
                Please rank your findings by the importance / severity of the events.
                Please refrain from including irrelevant information.

                Research pieces: ```{research_md}```
        """
        return transformer(overall_query, method=method)

    @classmethod
    def query_summary(cls, company_name, controv, search_term, method):
        #question = f'what are the controversies and events of concern surrounding {company_name} and its significant subsidiaries?'
        question = f'what are the controversies and events of concern regarding {search_term} surrounding {company_name} and its significant subsidiaries?'
        query = f"""
                    Your task is to answer user's question about the company {company_name} from the articles below in json, delimited by triple quotes.
                    Please extract the relative information, and respond in about 200 words in concise and professional tone in markdown format with bullet points and not json.
                    Please highlight item headers and important phrases in bold.
                    Please include details like dates, location, fines, key persons if available.
                    Please cite your sources with only the given citation_number, e.g., [^12^] and not by the title or link.
                    Please do not append a citation list in the end.
                    Please rank your findings by the importance / severity of the events.
                    Please refrain from including irrelevant information about the question.

                    Articles: ```{controv}```
                    Question: ```{question}```
                                """
        return transformer(query, method=method)

    @classmethod
    def query_recent(cls, company_name, seleya_headlines, method):
        query = f"""
                   Your task is to find additional controversial events from the given headlines about the company {company_name}.
                   The headlines are listed below, delimited by triple quotes.
                   Please only generate an itemized list, not a full report.
                   Please limit your answer in 150 words, and write in concise and professional tone.
                   Please include details like date, location, fines, key persons if available.
                   Please refrain from including irrelevant information.

                   Headlines: ```{seleya_headlines}```
                   """
        return transformer(query, method=method)

    @classmethod
    def query_target_summarize(cls, observation, method):
        query = """
        I want you to help extract key information out of company ghg emissions targets. If you do not know hot to extract certain targets, please return the original text for them.

        Observation:
        BP targets a 20% reduction in our aim 1 operational emissions by 2025 (Scope 1 & 2). We are targeting a 10-15% reduction by 2025 for Scope 3. They will aim for a 50% reduction in our aim 1 operational emissions by 2030 against their 2019 baseline (Scope 1 & 2). We will aim for 20-30% by 2030 against our 2019 baseline for Scope 3. By 2050 or sooner, they aim to be net zero on an absolute basis across our entire operations and in our upstream oil and gas production.
        Extracted Targets:
        |target scope | target year | baseline year | reduction percentage |
        |scope 1 & 2 | 2025 | 2019 | 20% |
        |scope 3 | 2025 | 2019 | 10-15% |
        |scope 1 & 2 | 2030 | 2019 | 50% |
        |scope 3 | 2030 | 2019 | 20-30% |
        |scope 1&2 | 2050 | 2019 | 100% |

        Observation:
        {observation}
        """
        return transformer(query, method=method)