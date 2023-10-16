from functools import lru_cache
from pathlib import Path

import requests
from markupsafe import Markup


class CDNHTMLHelper:
    """
    A class for generating HTML tags for files hosted on jsDelivr CDN.
    """

    CDN_URL = "https://cdn.jsdelivr.net"

    DATA_URL = "https://data.jsdelivr.com"
    FILE_PATH = "/{repo}/{package}@{version}{name}"
    API_RESOLVED_VERSION = "/v1/packages/npm/{package}/resolved"
    API_VERSION_METADATA = "/v1/packages/npm/{package}@{version}"
    API_ENTRYPOINTS = "/v1/packages/npm/{package}@{version}/entrypoints"
    TEMPLATE_STRINGS = {
        ".css": (
            '<link rel="stylesheet"'
            ' href="{file_url}"'
            ' integrity="sha256-{hash}" crossorigin="anonymous"/>'
        ),
        ".js": (
            '<script src="{file_url}"'
            ' integrity="sha256-{hash}"'
            ' crossorigin="anonymous"></script>'
        ),
        # Add more template strings for other file types if needed
    }

    def __init__(self, app=None, local=False, local_url=None):
        """
        Initializes a new instance of the CDNHTMLHelper class.

        Args:
            app: An optional Flask application instance.
        """
        self.data = {}
        self.app_name = type(app).__name__
        self.local = local
        self.local_url = local_url

        if self.app_name == "Flask":
            self.app = app

            @app.context_processor
            def _():
                return dict(cdn_html_helper=self)

        self._handle_local()

    def _handle_local(self):
        """
        Configures local resource paths and URLs based on app settings.

        Handles the local resource path and URL configuration,
        taking into account various conditions such as app and local setting.

        Returns:
            None
        """
        if self.local == True and self.app_name == "Flask":
            self.local = Path(self.app.static_folder, "resources")
            if self.local_url == None:
                self.local_url = f"{self.app.static_url_path}/resources"
        elif self.local == True:
            self.local = Path("resources")
        elif type(self.local) == str:
            self.local = Path(self.local)
        elif type(self.local) == Path:
            self.local = self.local

        if self.local and not self.local_url:
            self.local_url = self.local

    def _get_hash_and_name(self, package, version, filename):
        """
        Gets the hash and name of a file in a package.

        Args:
            package: The name of the package.
            version: The version of the package.
            filename: The name of the file.

        Returns:
            A tuple containing the name and hash of the file.
        """
        r = requests.get(
            self.DATA_URL + self.API_VERSION_METADATA.format(package=package, version=version),
            params={"structure": "flat"},
        )

        for file in r.json().get("files", []):
            if file["name"].endswith(filename):
                return file["name"], file["hash"]

    def _get_default_files(self, package, version):
        """
        Gets the default files for a package version.

        Args:
            package: The name of the package.
            version: The version of the package.

        Returns:
            A dictionary containing the default files for the package version.
        """
        files = {}
        r = requests.get(
            self.DATA_URL + self.API_ENTRYPOINTS.format(package=package, version=version)
        )
        entrypoints = r.json().get("entrypoints", {})
        for key, value in entrypoints.items():
            if "file" in value:
                files[key] = value["file"]
        return files

    def use(self, package, version="latest", files={}):
        """
        Adds a package to the data dictionary.

        Args:
            package: The name of the package.
            version: The version of the package.
            files: A dictionary containing the files to be added to the package.

        Raises:
            Exception: If the package is not found.
        """
        self.data[package] = {"requested_version": version, "files": {}}

        r = requests.get(
            self.DATA_URL + self.API_RESOLVED_VERSION.format(package=package),
            params={"specifier": version},
        )
        data = r.json()
        if not data.get("version"):
            raise Exception(f"Package {package} not found")
        if not files:
            files = self._get_default_files(package, data["version"])
        for alias, filename in files.items():
            name, hash = self._get_hash_and_name(package, data["version"], filename)
            self.data[package]["files"][alias] = {
                "name": name,
                "package": package,
                "version": data["version"],
                "repo": "npm",
                "hash": hash,
            }
            if self.local:
                self._download(package, data["version"], name)

    def _download(self, package, version, name):
        """
        Downloads a file from a CDN and saves it to the local file system.

        Args:
            package (str): The name of the package to download.
            version (str): The version of the package to download.
            name (str): The name of the file to download.

        Raises:
            Exception: If the resulting file path is not relative to the current directory.

        Returns:
            None
        """
        file_path = self.FILE_PATH.format(
            cdn_url=self.CDN_URL, repo="npm", package=package, version=version, name=name
        )
        _path = Path(self.local, file_path.lstrip("/"))
        if not _path.is_relative_to(self.local):
            raise Exception("Path leaves current dir")

        _path.parent.mkdir(parents=True, exist_ok=True)
        with open(_path, "wb") as f:
            f.write(requests.get(self.CDN_URL + file_path).content)

    def _find_matching_extension(self, filename):
        """
        Finds the matching extension for a filename.

        Args:
            filename: The name of the file.

        Returns:
            The matching extension for the file.
        """
        matching_extension = None
        for extension in self.TEMPLATE_STRINGS.keys():
            if filename.endswith(extension) and (
                matching_extension is None or len(extension) > len(matching_extension)
            ):
                matching_extension = extension
        return matching_extension

    @lru_cache(maxsize=None)
    def _get_string(self, package, alias):
        """
        Gets the HTML tag string for a file in a package.

        Args:
            package: The name of the package.
            alias: The alias of the file.

        Returns:
            The HTML tag string for the file.
        """
        file = self.data.get(package, {}).get("files", {}).get(alias)
        if not file:
            return f"<!-- File not found -->"

        filetype = self._find_matching_extension(file.get("name"))

        if filetype:
            template_string = self.TEMPLATE_STRINGS[filetype]
        else:
            return f"<!-- Template string not found for file type [{file['name']}] -->"

        file_path = self.FILE_PATH.format(
            repo=file.get("repo"),
            package=file.get("package"),
            version=file.get("version"),
            name=file.get("name"),
        )
        file_url = f"{self.CDN_URL if not self.local else self.local_url}{file_path}"
        return template_string.format(
            file_url=file_url,
            hash=file.get("hash"),
        )

    def get(self, package=None, alias=None):
        """
        Generates HTML tags for the specified package and alias, or for all packages and aliases if none are specified.

        Args:
            package (str, optional): The name of the package to generate HTML tags for.
            alias (str, optional): The alias of the package file to generate HTML tags for.

        Returns:
            str or Markup: The generated HTML tags.
        """
        html = ""
        if not package and not alias:
            for package in self.data.keys():
                for alias in self.data.get(package, {}).get("files", {}).keys():
                    html += self._get_string(package, alias)
        elif not package and alias:
            for package in self.data.keys():
                html += self._get_string(package, alias)
        elif package and not alias:
            for alias in self.data.get(package, {}).get("files", {}).keys():
                html += self._get_string(package, alias)
        elif package and alias:
            html = self._get_string(package, alias)

        return Markup(html)
