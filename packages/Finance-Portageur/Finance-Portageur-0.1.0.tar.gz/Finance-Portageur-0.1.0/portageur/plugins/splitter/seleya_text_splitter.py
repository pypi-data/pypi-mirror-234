from langchain.text_splitter import TextSplitter
from typing import (
    AbstractSet,
    Any,
    Collection,
    List,
    Literal,
    Optional,
    Union,
)


class SeleyaTextSplitter(TextSplitter):
    """Implementation of splitting text that looks at tokens."""

    def __init__(
            self,
            encoding_name: str = "cl100k_base",
            model_name: Optional[str] = None,
            allowed_special: Union[Literal["all"], AbstractSet[str]] = set(),
            disallowed_special: Union[Literal["all"], Collection[str]] = "all",
            **kwargs: Any,
    ):
        """Create a new TextSplitter."""
        super().__init__(**kwargs)
        try:
            import tiktoken
        except ImportError:
            raise ImportError(
                "Could not import tiktoken python package. "
                "This is needed in order to for TokenTextSplitter. "
                "Please install it with `pip install tiktoken`."
            )

        if model_name is not None:
            enc = tiktoken.encoding_for_model(model_name)
        else:
            enc = tiktoken.get_encoding(encoding_name)
        self._tokenizer = enc
        self._allowed_special = allowed_special
        self._disallowed_special = disallowed_special

    def _num_tokens_from_string(self, string):
        """Returns the number of tokens in a text string."""
        num_tokens = len(self._tokenizer.encode(string))
        return num_tokens

    def split_text(self, texts: List[str]) -> List[str]:
        """Split incoming text and return chunks."""

        accumulated_len = self._num_tokens_from_string(f"|{texts[0]}")
        accumulated_text = texts[0]
        splits = []
        for text in texts[1:]:
            text_len = self._num_tokens_from_string(f"|{text}")
            if accumulated_len + text_len <= self._chunk_size:
                accumulated_text += f"|{text}"
                accumulated_len += text_len
            else:
                splits.append(accumulated_text)
                accumulated_text = text
                accumulated_len = text_len
        splits.append(accumulated_text)
        return splits
