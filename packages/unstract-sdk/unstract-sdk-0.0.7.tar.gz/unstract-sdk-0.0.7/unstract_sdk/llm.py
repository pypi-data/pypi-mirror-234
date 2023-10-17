from typing import Optional

import openai
import tiktoken
from llama_index.callbacks import CallbackManager, TokenCountingHandler
from llama_index.llms import AzureOpenAI
from llama_index.llms.base import LLM
from unstract_sdk.tools import UnstractToolUtils


class UnstractToolLLM:
    """Class to handle LLMs for Unstract Tools."""

    def __init__(self, utils: UnstractToolUtils, llm_id: str):
        """

        Notes:
            - "Azure OpenAI" : Environment variables required OPENAI_API_KEY,
            OPENAI_API_BASE, OPENAI_API_VERSION, OPENAI_API_ENGINE, OPENAI_API_MODEL

        Args:
            utils (UnstractToolUtils): The utils object for the tool.
            llm_id (str): The id of the LLM to use.
                Supported values:
                    - "Azure OpenAI"
        """
        self.utils = utils
        self.llm_id = llm_id
        self.max_tokens = 1024 * 4

    def get_llm(self) -> Optional[LLM]:
        """Returns the LLM object for the tool.

        Returns:
            Optional[LLM]: The LLM object for the tool. (llama_index.llms.base.LLM)
        """
        if self.llm_id == "Azure OpenAI":
            # We are using the 16k context. Change if required
            self.max_tokens = 1024 * 16
            openai.api_type = "azure"
            llm = AzureOpenAI(
                engine=self.utils.get_env_or_die("OPENAI_API_ENGINE"),
                model=self.utils.get_env_or_die("OPENAI_API_MODEL"),
                temperature=0.0,
            )
            return llm
        else:
            self.utils.stream_log(f"LLM not found for id: {self.llm_id}", level="ERROR")
            return None

    def get_callback_manager(self) -> Optional[CallbackManager]:
        """Returns the Callback Manager object for the tool.

        Returns:
            Optional[CallbackManager]: The Callback Manager object for the tool.
                (llama_index.callbacks.CallbackManager)
        """
        if self.llm_id == "Azure OpenAI":
            self.token_counter = TokenCountingHandler(
                tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
            )
            callback_manager = CallbackManager([self.token_counter])
            return callback_manager
        else:
            self.utils.stream_log(
                f"LLM/Callback Manager not found for id: {self.llm_id}", level="ERROR"
            )
            return None

    def get_usage_counts(self) -> dict[str, int]:
        """Returns the usage counts for the tool.

        Returns:
            dict: The usage counts for the tool.
                - embedding_tokens: The number of tokens used for the embedding.
                - llm_prompt_tokens: The number of tokens used for the LLM prompt.
                - llm_completion_tokens:
                    The number of tokens used for the LLM completion.
                - total_llm_tokens: The total number of tokens used for the LLM.
        """

        return {
            "embedding_tokens": self.token_counter.total_embedding_token_count,
            "llm_prompt_tokens": self.token_counter.prompt_llm_token_count,
            "llm_completion_tokens": self.token_counter.completion_llm_token_count,
            "total_llm_tokens": self.token_counter.total_llm_token_count,
        }

    def stream_usage_counts(self) -> None:
        """Stream all usage costs.

        This function retrieves the usage counts and
        stream the costs associated with it.

        Returns:
            None
        """
        usage_counts = self.get_usage_counts()
        for unit, cost in usage_counts.items():
            self.utils.stream_cost(cost=cost, cost_units=unit)

    def reset_usage_counts(self) -> None:
        """Resets the usage counts for the tool.

        Returns:
            None
        """
        self.token_counter.reset_counts()

    def get_max_tokens(self, reserved_for_output: int = 0) -> int:
        """Returns the maximum number of tokens that can be used for the LLM.

        Args:
            reserved_for_output (int): The number of tokens reserved for the output.
                The default is 0.

        Returns:
            int: The maximum number of tokens that can be used for the LLM.
        """
        return self.max_tokens - reserved_for_output
