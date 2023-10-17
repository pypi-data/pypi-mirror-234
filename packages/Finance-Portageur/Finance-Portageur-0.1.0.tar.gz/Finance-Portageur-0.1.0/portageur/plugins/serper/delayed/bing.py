from pydantic import BaseModel, Extra, root_validator
from langchain.utils import get_from_dict_or_env
from typing import Dict, List
import aiohttp
import asyncio


class BingSearchAPIWrapper(BaseModel):
    # 其余部分不变，只修改了以下内容：
    bing_subscription_key: str
    bing_search_url: str
    k: int = 10

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and endpoint exists in environment."""
        bing_subscription_key = get_from_dict_or_env(values,
                                                     "bing_subscription_key",
                                                     "BING_SUBSCRIPTION_KEY")
        values["bing_subscription_key"] = bing_subscription_key

        bing_search_url = get_from_dict_or_env(
            values,
            "bing_search_url",
            "BING_SEARCH_URL",
            # default="https://api.bing.microsoft.com/v7.0/search",
        )

        values["bing_search_url"] = bing_search_url

        return values

    async def _bing_search_results(self, search_term: str,
                                   count: int) -> List[dict]:
        headers = {"Ocp-Apim-Subscription-Key": self.bing_subscription_key}
        params = {
            "q": search_term,
            "count": count,
            "textDecorations": "true",
            "textFormat": "HTML",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.bing_search_url,
                                   headers=headers,
                                   params=params) as response:
                response.raise_for_status()
                search_results = await response.json()
                return search_results["webPages"]["value"]

    async def run(self, query: str) -> str:
        snippets = []
        results = await self._bing_search_results(query, count=self.k)
        if len(results) == 0:
            return "No good Bing Search Result was found"
        for result in results:
            snippets.append(result["snippet"])

        return " ".join(snippets)

    async def results(self, query: str, num_results: int) -> List[Dict]:
        metadata_results = []
        results = await self._bing_search_results(query, count=num_results)
        if len(results) == 0:
            return [{"Result": "No good Bing Search Result was found"}]
        for result in results:
            metadata_result = {
                "snippet": result["snippet"],
                "title": result["name"],
                "link": result["url"],
            }
            metadata_results.append(metadata_result)

        return {'query': query, 'meta': metadata_results}
