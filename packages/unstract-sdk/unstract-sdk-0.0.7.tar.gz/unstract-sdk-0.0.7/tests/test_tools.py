import unittest
from io import StringIO
from unittest.mock import patch

from sdks.unstract import tools as unstract_tools


class UnstractSDKToolsTest(unittest.TestCase):
    def test_spec(self):
        spec = unstract_tools.spec(spec_file='config/tool_json_schema.json')
        self.assertIsNotNone(spec)

    def test_stream_spec(self):
        spec = unstract_tools.spec(spec_file='config/tool_json_schema.json')
        captured_output = StringIO()
        with patch('sys.stdout', new=captured_output):
            unstract_tools.stream_spec(spec)
        captured_output_str = captured_output.getvalue()
        print(captured_output_str)
        self.assertIn("SPEC", captured_output_str)

    def test_properties(self):
        properties = unstract_tools.properties(properties_file='config/tool_properties.json')
        self.assertIsNotNone(properties)

    def test_stream_properties(self):
        properties = unstract_tools.properties(properties_file='config/tool_properties.json')
        captured_output = StringIO()
        with patch('sys.stdout', new=captured_output):
            unstract_tools.stream_properties(properties)
        captured_output_str = captured_output.getvalue()
        print(captured_output_str)
        self.assertIn("PROPERTIES", captured_output_str)

    def test_icon(self):
        icon = unstract_tools.icon(icon_file='config/icon.svg')
        self.assertIsNotNone(icon)

    def test_stream_icon(self):
        icon = unstract_tools.icon(icon_file='config/icon.svg')
        captured_output = StringIO()
        with patch('sys.stdout', new=captured_output):
            unstract_tools.stream_icon(icon)
        captured_output_str = captured_output.getvalue()
        print(captured_output_str)
        self.assertIn("ICON", captured_output_str)


if __name__ == '__main__':
    unittest.main()
