import io
from pydantic.main import BaseModel
from contextlib import redirect_stderr
import tiktoken
from requests_html import HTMLSession
from boilerpy3 import extractors


class Base(BaseModel):

    def _num_tokens_from_string(self, string, encoding_name='cl100k_base'):
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def run_urls(self, query: str) -> str:
        """Run query through GoogleSearch and parse result."""
        results = self._value_serper_search_results(query,
                                                    gl=self.gl,
                                                    hl=self.hl)

        urls = self._parse_results_for_urls(results)
        if len(urls) == 0:
            return "No good Google Search urls was found"

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
                        article = extractor.get_content(r.text)
                        article = article[:750]
                        articles.append(article)
                    except:
                        pass
        session.close()

        full_text = "||".join(articles)

        while self._num_tokens_from_string(full_text) > 1250:
            full_text = full_text[:-100]

        return full_text