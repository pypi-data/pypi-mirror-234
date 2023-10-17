import asyncio, json, pdb, string, datetime, tiktoken
from boilerpy3 import extractors
from htmldate import find_date
from requests_html import AsyncHTMLSession
from portageur.plugins.serper.delayed.bing import BingSearchAPIWrapper


class AsyncSearch(object):
    name = 'async_bing'

    def __init__(self):
        self.extractor = extractors.ArticleExtractor(raise_on_failure=False)
        self._search = BingSearchAPIWrapper()
        self._loop = asyncio.get_event_loop()

    def _num_tokens_from_string(self, string, encoding_name='cl100k_base'):
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def remove_non_ascii(self, a_str):
        ascii_chars = set(string.printable)

        return ''.join(filter(lambda x: x in ascii_chars, a_str))

    async def _async_html(self, query, url):
        asession = AsyncHTMLSession()
        try:
            response = await asession.get(url, timeout=2.0)
            response.raise_for_status()
            content = response.text
            return {'query': query, 'content': content, 'url': url}
        except Exception as e:
            return {'query': query, 'content': "", 'url': url}

    async def async_search(self, search_terms, article_numbers):
        search = BingSearchAPIWrapper()
        tasks = [
            search.results(query, article_numbers) for query in search_terms
        ]
        results = await asyncio.gather(*tasks)
        results = [{
            'query':
            item['query'],
            'meta': [
                sub_dict['link'] for sub_dict in item['meta']
                if 'link' in sub_dict
            ]
        } for item in results]
        return results

    async def async_content(self, urls):
        tasks = [
            self._async_html(query=item['query'], url=url) for item in urls
            for url in item['meta']
        ]
        #tasks = [self._async_html(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

    def transfromer(self, contents):
        result = {}
        for item in contents:
            query = item['query']
            content = item['content']
            url = item['url']
            if query not in result:
                result[query] = {
                    'query': query,
                    'article': [{
                        'content': content,
                        'url': url
                    }]
                }
            else:
                result[query]['article'].append({
                    'content': content,
                    'url': url
                })
        return result

    def parser_boilerpy(self, content, citation_num, article_cutoff):
        article = {'citation_number': citation_num}
        if len(content) == 0:
            return None
        publish_date = find_date(content,
                                 original_date=True,
                                 outputformat='%b %Y')
        article['date'] = publish_date if publish_date else "Jan 2019"
        try:
            article_text = self.extractor.get_doc(content)
            article_text = article_text.title + " " + article_text.content
            article_text = self.remove_non_ascii(article_text)
            article_text = article_text[:article_cutoff]
            article['text'] = article_text
        except Exception as e:
            article = None
        return article

    def analyze_article(self,
                        search_term,
                        contents,
                        total_token_limit=6050,
                        article_cutoff=2500,
                        citation_start=1):
        articles = []
        citation_map = {}
        total_tokens = 0
        citation_num = citation_start
        for content in contents:
            article = self.parser_boilerpy(content=content['content'],
                                           citation_num=citation_num,
                                           article_cutoff=article_cutoff)
            if article is None:
                continue

            article_tokens = self._num_tokens_from_string(article['text'])
            total_tokens += article_tokens
            # if adding the new article would exceed the token limit, stop
            if total_tokens > total_token_limit:
                break

            articles.append(article)
            citation_map[citation_num] = content['url']
            citation_num += 1

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

    def run_urls_long_json(self,
                           search_terms,
                           article_numbers=15,
                           total_token_limit=6050,
                           article_cutoff=2500):
        controversy_dict = {}
        citationmap_dict = {}
        urls = self._loop.run_until_complete(
            self.async_search(search_terms=search_terms,
                              article_numbers=article_numbers))
        contents = self._loop.run_until_complete(self.async_content(urls=urls))
        contents = self.transfromer(contents)
        key = 'Microsoft Controversies or Investor concerns'
        for idx, key in enumerate(contents):
            controv, citation_map = self.analyze_article(
                search_term=key,
                contents=contents[key]['article'],
                total_token_limit=total_token_limit,
                article_cutoff=article_cutoff,
                citation_start=(idx * article_numbers + 1))
            controversy_dict[key] = controv
            citationmap_dict[key] = citation_map
        return controversy_dict, citationmap_dict
