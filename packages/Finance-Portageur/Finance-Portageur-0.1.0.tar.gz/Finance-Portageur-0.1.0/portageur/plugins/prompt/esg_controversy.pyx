# -*- coding: utf-8 -*
import pdb
import re

from portageur.kdutils.division.lazy import LazyFunc
from portageur.plugins.prompt.base import transformer, PromptsMessage

class ESGControversy(object):

    @classmethod
    def research(cls, company):
        return company.esg_controversy

    @classmethod
    def research_assistant(self):
        prompt = """You are a research assistant that helps with analyzing information about companies.
                    Please focus your research on issues and events that can be of concern to investors.
                    Please be objective and critical of the research subject.
                    Please exclude stale events that occurred before 2010.
                    Please refrain from including information that are overly positive about the subject, e.g., puff pieces and company affiliated websites.
                    If you cannot find any relevant information, please respond with "No information found." """
        return transformer(query=prompt, method=PromptsMessage.System)

    @classmethod
    def query_level2(cls, company_name, controv, search_term, method):
        question = f'what are the controversies and events of concern related to {search_term} ' \
                   f'surrounding {company_name} and its significant subsidiaries?'
        overall_query = f"""
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
        return transformer(overall_query, method=method)

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
    def match_sources(cls, results, citation_map):
        """
        parse the source citations in the answer, and return it in markdown format
        """
        pattern = r"\[\^(\d+)\^\]"
        matches = re.findall(pattern, results)
        matches = [int(match) for match in matches]
        matches = list(sorted(set(matches)))
        md_str = ""
        for match in matches:
            try:
                md_str += f"[Document {match}]({citation_map[str(match)]}) "
                # md_str += f"<a href='{citation_map[match]}' target='_blank'> [Document{match}] </a>"
            except KeyError:
                pass
        return md_str

    @classmethod
    def match_sources_and_format(cls, results, citation_map):
        """
        parse the source citations in the answer, rerank the answers, and return it in markdown format
        """
        pattern = r"\[\^(\d+)\^\]"
        matches = re.findall(pattern, results)
        matches = [int(match) for match in matches]
        # deduplicate matches, while maintaining sequence
        # matches = list(set(matches)) # this will change the sequence, so cannot use
        matches_dedup = [i for n, i in enumerate(matches) if i not in matches[:n]]
        # reassign citation numbers
        new_citation_map = {}
        # url to number map
        inverse_citation_map = {}
        formatted_results = results
        # for display, the citation starts at 1
        new_idx = 1
        # record the last cited number, so we wont repeat the same citation consecutively
        last_cited = -1
        for citation_idx, match in enumerate(matches_dedup):
            try:
                source_link = citation_map[str(match)]
                # citation_md = f"<sup>[[{citation_idx}]]({source_link})</sup>" # disable superscript for now
                # new url that has not been cited before
                if source_link not in inverse_citation_map.keys():
                    inverse_citation_map[source_link] = new_idx
                    # citation_md = f"[[{new_idx}]]({source_link})"
                    # use {} instead of [] to avoid conflict with reformatting
                    citation_md = f"{{{new_idx}}}"
                    formatted_results = formatted_results.replace(f"[^{match}^]", citation_md)
                    new_citation_map[str(new_idx)] = source_link
                    # the next reference will be the next number
                    last_cited = new_idx
                    new_idx += 1
                # the url has already been cited
                else:
                    # get the existing citation number
                    cite_idx = inverse_citation_map[source_link]
                    if cite_idx == last_cited:
                        # if the article is the same one as the last cited one, we remove the citation
                        formatted_results = formatted_results.replace(f"[^{match}^]", '')
                    else:
                        # if the article is different from the last cited one, we cite it again
                        # citation_md = f"[[{cite_idx}]]({source_link})"
                        citation_md = f"{{{cite_idx}}}"
                        formatted_results = formatted_results.replace(f"[^{match}^]", citation_md)
                        # update the last cited number
                        last_cited = cite_idx
            except KeyError:
                pass
        citations = re.findall(r'\{[0-9\{\}]*\}', formatted_results)
        # process the citations in descending order of length
        citations = sorted(citations, key=lambda k: len(k), reverse=True)
        for cite_str in citations:
            # get the citation numbers in a consecutive list
            cite_list = re.split(r'[{\}]', cite_str)
            cite_list = [int(x) for x in cite_list if x != '']
            cite_list = list(sorted(list(set(cite_list))))
            # if there is only one citation number, we need to reorganize the citation
            if len(cite_list) > 1:
                # if there are more than one citation number, we combine them
                citation_md = [f"[[{x}]]({new_citation_map[str(x)]})" for x in cite_list]
                citation_md = ''.join(citation_md)
                formatted_results = formatted_results.replace(cite_str, citation_md)
            elif len(cite_list) == 1:
                source_link = new_citation_map[str(cite_list[0])]
                citation_md = f"[[{cite_list[0]}]]({source_link})"
                formatted_results = formatted_results.replace(cite_str, citation_md)
            else:
                pass

        return formatted_results, new_citation_map

    # @classmethod
    # def scrap_wab(cls, bing_serper, search_term: str, company_name: str, retry=2, citation_start=1, num_result=15):
    #     while retry >= 0:
    #         try:
    #             controv, citation_map = bing_serper.run_urls_long_json(
    #                 f'{company_name} {search_term}',
    #                 citation_start=citation_start, num_results=num_results)
    #             return search_term, controv, citation_map
    #             break
    #         except Exception as e:
    #             retry -= 1
    #     return "", "", {}

    @classmethod
    def query_recent(cls, company_name: str, seleya_headlines: str, method):
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