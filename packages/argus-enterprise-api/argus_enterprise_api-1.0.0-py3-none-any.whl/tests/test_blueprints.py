import unittest
from unittest.mock import patch, Mock
from api.blueprints import Blueprint


class TestBlueprints(unittest.TestCase):
    @patch("api.blueprints.json.load")
    @patch("builtins.open")
    def test_initialization(self, mock_open, mock_json_load):
        mock_client = Mock()
        mock_json = {"servers": [{"url": "http://example.com"}], "paths": {}}
        mock_json_load.return_value = mock_json

        blueprint = Blueprint(mock_client)

        self.assertEqual(blueprint._client, mock_client)
        self.assertEqual(blueprint._spec_path.endswith("-swagger.json"), True)
        mock_open.assert_called_once()
        mock_json_load.assert_called_once()
