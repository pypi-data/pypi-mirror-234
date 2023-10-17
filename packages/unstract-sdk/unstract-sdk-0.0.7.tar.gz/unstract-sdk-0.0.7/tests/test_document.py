import unittest

from sdks.unstract_sdk.documents import UnstractToolDocs
from sdks.unstract_sdk.tools import UnstractToolUtils


class UnstractToolDocsTest(unittest.TestCase):
    @unittest.skip("Skipping")
    def test_insert_get_delete(self) -> None:
        utils = UnstractToolUtils()
        docs = UnstractToolDocs(
            utils=utils, platform_host="http://localhost", platform_port=3001
        )
        result = docs.insert(
            project_id="test",
            unique_file_id="test_unique_file_id2",
            filename="test_filename",
            filetype="test_filetype",
            summary="test_summary",
            embedding_tokens=0,
            llm_tokens=0,
            vector_db="Postgres pg_vector",
        )
        self.assertTrue(result)
        result = docs.get(project_id="test", unique_file_id="test_unique_file_id2")
        print(result)
        self.assertIsNotNone(result)
        result = docs.delete(project_id="test", unique_file_id="test_unique_file_id2")
        self.assertTrue(result)
        result = docs.get(project_id="test", unique_file_id="test_unique_file_id2")
        self.assertIsNone(result)

    def test_indexer(self) -> None:
        utils = UnstractToolUtils()
        docs = UnstractToolDocs(
            utils=utils, platform_host="http://localhost", platform_port=3001
        )
        result = docs.index_file(
            project_id="test2",
            embedding_type="Azure OpenAI",
            vector_db="Postgres pg_vector",
            file_path="/mnt/unstract/fs_input/files/Suriya cv.pdf",
            overwrite=True,
        )
        print(result)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
