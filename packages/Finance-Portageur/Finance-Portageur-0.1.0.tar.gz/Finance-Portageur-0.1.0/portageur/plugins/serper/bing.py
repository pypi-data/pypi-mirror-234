import io, string, datetime, json, pdb
from contextlib import redirect_stderr
from requests_html import HTMLSession
from boilerpy3 import extractors
from htmldate import find_date
from langchain.utilities import BingSearchAPIWrapper
from portageur.plugins.serper.base import Base
from portageur.plugins.serper.bing_custom_wrapper import BingCustomSearchAPIWrapper


class Bing(Base):
    name = 'bing'

    def run(self, query: str) -> str:
        """Run query through BingSearch and parse result."""
        results = self._value_serper_search_results(query)

        return self._parse_results(results)

    def run_urls_long(self, query: str, article_cutoff=2000) -> str:
        """Run query through BingSearch and parse result."""
        results = self._value_serper_search_results(query)

        urls = self._parse_results_for_urls(results)
        if len(urls) == 0:
            return "No good Bing Search urls was found"

        session = HTMLSession()
        extractor = extractors.ArticleExtractor(raise_on_failure=False)
        # encoding = tiktoken.get_encoding("cl100k_base")

        articles = []

        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            with redirect_stderr(f):
                for url in urls:
                    try:
                        r = session.get(url)
                        article = extractor.get_doc(r.text)
                        article = article.title + " " + article.content
                        article = article[:article_cutoff]
                        articles.append(article)
                    except:
                        pass
        session.close()

        full_text = "||".join(articles)

        while self._num_tokens_from_string(full_text) > 7000:
            full_text = full_text[:-50]

        return full_text

    def _remove_non_ascii(self, a_str):
        ascii_chars = set(string.printable)

        return ''.join(filter(lambda x: x in ascii_chars, a_str))

    def run_urls_long_json(self,
                           query: str,
                           total_token_limit=6050,
                           article_cutoff=2500,
                           citation_start=1):
        """Run query through BingSearch and parse result."""
        results = self._value_serper_search_results(query)
        urls = self._parse_results_for_urls(results)
        if len(urls) == 0:
            print("No Good Bing Search urls was found")
            return None, {}

        session = HTMLSession()
        extractor = extractors.ArticleExtractor(raise_on_failure=False)
        # encoding = tiktoken.get_encoding("cl100k_base")

        articles = []
        citation_map = {}

        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            with redirect_stderr(f):
                citation_num = citation_start
                total_tokens = 0
                for url in urls:
                    try:
                        if total_tokens > total_token_limit:
                            break
                        r = session.get(url)
                        article = {'citation_number': citation_num}
                        publish_date = find_date(r.text,
                                                 original_date=True,
                                                 outputformat='%b %Y')
                        article[
                            'date'] = publish_date if publish_date else "Jan 2019"
                        article_text = extractor.get_doc(r.text)
                        article_text = article_text.title + " " + article_text.content
                        article_text = self._remove_non_ascii(article_text)
                        article_text = article_text[:article_cutoff]
                        article['text'] = article_text
                        articles.append(article)
                        citation_map[citation_num] = url
                        citation_num += 1
                        total_tokens += self._num_tokens_from_string(
                            article_text)
                    except:
                        pass
        session.close()

        sorted_articles = sorted(
            articles,
            key=lambda x: datetime.datetime.strptime(x['date'], '%b %Y'),
            reverse=True)

        citation_map_new = {}
        for i, article in enumerate(sorted_articles):
            old_citation_num = article['citation_number']
            url = citation_map[old_citation_num]
            article['citation_number'] = i + citation_start
            citation_map_new[str(i + citation_start)] = url

        return json.dumps(sorted_articles, indent=2), citation_map_new

    def run_urls_long_json_multi(self,
                                 queries,
                                 total_token_limit=6200,
                                 article_cutoff=2500):
        article_jsons = []
        citation_maps = []
        for query in queries:
            results = self._value_serper_search_results(query)
            urls = self._parse_results_for_urls(results)

    def _parse_results_for_urls(self, results: dict) -> list:
        urls = []
        for result in results:
            if result.get("link"):
                urls.append(result["link"])

        if len(urls) == 0:
            print("No good Google Search Result was found")
            return []

        # if len(urls) == 0:
        #     return "No good Google Search urls was found"

        return urls

    def _parse_results(self, results: dict) -> str:
        snippets = []
        for result in results:
            if result.get("title"):
                snippets.append(result["title"])
            if result.get("snippet"):
                snippets.append(result["snippet"])

        if len(snippets) == 0:
            return "No good Google Search Result was found"

        return " ".join(snippets)

    def _value_serper_search_results(self,
                                     search_term: str,
                                     custom=False,
                                     num_results=15):
        search = BingSearchAPIWrapper(
        ) if not custom else BingCustomSearchAPIWrapper()
        search_results = search.results(search_term, num_results)
        return search_results
