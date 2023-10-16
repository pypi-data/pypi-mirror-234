import unittest
from unittest.mock import patch

from CDNHTMLHelper import CDNHTMLHelper


class TestCDNHTMLHelper(unittest.TestCase):
    def setUp(self):
        self.cdn_html_helper = CDNHTMLHelper()
        self.maxDiff = None

    def test_get_hash_and_name(self):
        package = "jquery"
        version = "3.6.0"
        filename = "jquery.js"
        expected_output = (
            "/dist/jquery.js",
            "H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=",
        )

        with patch("CDNHTMLHelper.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "type": "npm",
                "name": "jquery",
                "version": "3.6.0",
                "default": "/dist/jquery.min.js",
                "files": [
                    {
                        "name": "/AUTHORS.txt",
                        "hash": "+e+lrsW5i7sKvDmE0SHWJLRgrTlCM8nIiMrhY3p3dQY=",
                        "size": 12448,
                    },
                    {
                        "name": "/bower.json",
                        "hash": "gOOJjukzNHufmoTD2V03ez88xkQj+aVN99PG1FpqrVo=",
                        "size": 190,
                    },
                    {
                        "name": "/dist/jquery.js",
                        "hash": "H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=",
                        "size": 288580,
                    },
                    {
                        "name": "/dist/jquery.min.js",
                        "hash": "/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=",
                        "size": 89501,
                    },
                    {
                        "name": "/dist/jquery.min.map",
                        "hash": "h3kHBWvsN5koZRCQhj58SLMjDtMYV/BDyY03foi8uwM=",
                        "size": 137960,
                    },
                    # ... removed for brevity
                ],
                "links": {
                    "stats": "https://data.jsdelivr.com/v1/stats/packages/npm/jquery@3.6.0",
                    "entrypoints": "https://data.jsdelivr.com/v1/packages/npm/jquery@3.6.0/entrypoints",
                },
            }
            output = self.cdn_html_helper._get_hash_and_name(package, version, filename)
            self.assertEqual(output, expected_output)

    def test_get_default_files(self):
        package = "jquery"
        version = "3.6.0"
        expected_output = {"js": "/dist/jquery.js"}
        with patch("CDNHTMLHelper.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "entrypoints": {"js": {"file": "/dist/jquery.js", "guessed": False}}
            }
            output = self.cdn_html_helper._get_default_files(package, version)
            self.assertEqual(output, expected_output)

    def test_use(self):
        package = "jquery"
        version = "3.6.0"
        files = {"js": "/dist/jquery.js"}
        expected_output = {
            "jquery": {
                "requested_version": "3.6.0",
                "files": {
                    "js": {
                        "name": "/dist/jquery.js",
                        "package": "jquery",
                        "version": "3.6.0",
                        "repo": "npm",
                        "hash": "H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=",
                    }
                },
            }
        }

        with patch("CDNHTMLHelper.requests.get") as mock_get, patch.object(
            self.cdn_html_helper, "_get_default_files", return_value=files
        ), patch.object(
            self.cdn_html_helper,
            "_get_hash_and_name",
            return_value=("/dist/jquery.js", "H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk="),
        ):
            mock_get.return_value.json.return_value = {"version": "3.6.0"}
            self.cdn_html_helper.use(package, version, files)
            self.assertEqual(self.cdn_html_helper.data, expected_output)

    def test_find_matching_extension(self):
        filename = "jquery.min.js"
        expected_output = ".js"
        output = self.cdn_html_helper._find_matching_extension(filename)
        self.assertEqual(output, expected_output)

    def test_get_string(self):
        package = "jquery"
        alias = "js"
        expected_output = '<script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.js" integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=" crossorigin="anonymous"></script>'

        self.cdn_html_helper.data = {
            "jquery": {
                "requested_version": "3.6.0",
                "files": {
                    "js": {
                        "name": "/dist/jquery.js",
                        "package": "jquery",
                        "version": "3.6.0",
                        "repo": "npm",
                        "hash": "H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=",
                    }
                },
            }
        }
        output = self.cdn_html_helper._get_string(package, alias)
        self.assertEqual(output, expected_output)

    def test_get(self):
        package = "jquery"
        alias = "js"
        expected_output = '<script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.js" integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=" crossorigin="anonymous"></script>'
        with patch.object(self.cdn_html_helper, "_get_string", return_value=expected_output):
            output = self.cdn_html_helper.get(package, alias)
            self.assertEqual(output, expected_output)


# if __name__ == "__main__":
#     unittest.main()
