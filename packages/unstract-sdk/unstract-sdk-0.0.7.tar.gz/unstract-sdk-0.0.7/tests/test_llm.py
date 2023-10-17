import unittest

from llama_index import ServiceContext, set_global_service_context

from sdks.unstract_sdk.llm import UnstractToolLLM
from sdks.unstract_sdk.tools import UnstractToolUtils


class UnstractToolLLMTest(unittest.TestCase):

    def test_azure_openai(self):
        utils = UnstractToolUtils()
        tool_llm = UnstractToolLLM(utils=utils, llm_id='Azure OpenAI')
        llm = tool_llm.get_llm()
        self.assertIsNotNone(llm)
        cb = tool_llm.get_callback_manager()
        service_context = ServiceContext.from_defaults(llm=llm, callback_manager=cb)
        set_global_service_context(service_context)
        response = llm.complete('The capital of Tamilnadu is ', max_tokens=50, temperature=0.0, stop=['.', '\n'])
        self.assertEqual(response.text, 'Chennai')
        print(response)
        print(tool_llm.get_usage_counts())
        tool_llm.reset_usage_counts()
        response = llm.complete('The capital of Karnataka is ', max_tokens=50, temperature=0.0, stop=['.', '\n'])
        print(tool_llm.get_usage_counts())


if __name__ == '__main__':
    unittest.main()
