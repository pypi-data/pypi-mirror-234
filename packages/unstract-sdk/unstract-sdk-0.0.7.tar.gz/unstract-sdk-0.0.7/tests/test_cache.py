import unittest

from sdks.unstract_sdk.cache import UnstractToolCache
from sdks.unstract_sdk.tools import UnstractToolUtils


class UnstractToolCacheTest(unittest.TestCase):
    def test_set(self):
        utils = UnstractToolUtils()
        cache = UnstractToolCache(utils=utils, platform_host='http://localhost', platform_port=3001)
        result = cache.set(key='test_key', value='test_value')
        self.assertTrue(result)

    def test_get(self):
        utils = UnstractToolUtils()
        cache = UnstractToolCache(utils=utils, platform_host='http://localhost', platform_port=3001)
        cache.set(key='test_key', value='test_value')
        result = cache.get(key='test_key')
        self.assertEqual(result, 'test_value')

    def test_delete(self):
        utils = UnstractToolUtils()
        cache = UnstractToolCache(utils=utils, platform_host='http://localhost', platform_port=3001)
        cache.set(key='test_key', value='test_value')
        result = cache.delete(key='test_key')
        self.assertTrue(result)
        result = cache.get(key='test_key')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
