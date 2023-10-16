from unittest import mock
import pytest
from tycho.tycho_utils import Resource
import os

class TestResource:

    testdata = [
        ("test.yaml", None, "yaml"),
        ("test.yaml", 'yaml', "yaml"),
        ("test.json", None, "json"),
        ("test.json", 'json', "json"),
        ("test", 'yaml', "yaml"),
        ("test.exe", None, "json"),
    ]

    @pytest.mark.parametrize("resource_name,format,correct_type", testdata)
    def test_get_resource_obj(self, resource_name, format, correct_type, mocker):
        # Set up mocks
        mocker.patch('tycho.tycho_utils.Resource.get_resource_path', return_value="")
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('tycho.tycho_utils.Resource.load_json', return_value="json")
        mocker.patch('tycho.tycho_utils.Resource.load_yaml', return_value="yaml")

        # Test get_resource_obj
        resource = Resource()
        result = resource.get_resource_obj(resource_name, format)
        assert result == correct_type
