# CDNHTMLHelper

[![Build and Test and Publish to PyPI](https://github.com/dbautz/CDNHTMLHelper/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/dbautz/CDNHTMLHelper/actions/workflows/publish-to-pypi.yml)

The `CDNHTMLHelper` is a Python utility for generating HTML tags that link to files hosted on the [jsDelivr Content Delivery Network (CDN)](https://www.jsdelivr.com/). This class simplifies the process of including external JavaScript and CSS files in your web application by providing a programmatic way to generate HTML tags for these resources.

## Features

- Generate HTML tags for including JavaScript and CSS files from jsDelivr CDN.
- Fetch package information, including available versions and default files.
- Retrieve Subresource Integrity (SRI) hashes from the jsDelivr API to ensure file integrity and security.
- Optional integration with Flask applications to easily include resources in your templates.
- Optional download of files to local folder, to deliver the files without use of CDN.

## Installation

To use `CDNHTMLHelper`, you can install it via pip:

```bash
pip install CDNHTMLHelper
```

## Usage

### Initialization

You can create an instance of the `CDNHTMLHelper` class by simply instantiating it:

```python
from CDNHTMLHelper import CDNHTMLHelper

cdn_html_helper = CDNHTMLHelper()
```

Optionally, if you are using the Flask web framework, you can pass your Flask application instance to the constructor. This allows you to easily integrate `CDNHTMLHelper` into your Flask templates:

```python
from CDNHTMLHelper import CDNHTMLHelper
from flask import Flask

app = Flask(__name__)
cdn_html_helper = CDNHTMLHelper(app)
```

### Adding a Package

To add a package to the `CDNHTMLHelper` instance, use the `use` method. This method fetches package information from jsDelivr and adds it to the instance's data dictionary. You can specify the package name, version (default is "latest"), and a dictionary of files you want to include:

```python
cdn_html_helper.use("package-name", version="1.0.0", files={"alias1": "file1.js", "alias2": "file2.css"})
```

### Generating HTML Tags

To generate HTML tags for the added packages and their files, you can use the `get` method in different ways:

#### 1. Generate HTML tags for a specific package and alias:

```python
html_tag = cdn_html_helper.get(package="package-name", alias="alias1")
```

This will generate an HTML tag for the specified package and alias.

#### 2. Generate HTML tags for all aliases of a specific package:

```python
html_tags = cdn_html_helper.get(package="package-name")
```

This will generate HTML tags for all the files associated with the specified package.

#### 3. Generate HTML tags for all packages and aliases:

```python
html_tags = cdn_html_helper.get()
```

This will generate HTML tags for all the packages and their files that have been added using the `use` method.

You can choose the method that best suits your needs for including resources in your web pages.

### Flask Integration (Optional)

If you are using Flask and passed your Flask application instance to the `CDNHTMLHelper` constructor, you can use the `cdn_html_helper` variable directly in your Flask templates to generate HTML tags. Example usage in a Flask template:

```html
<!DOCTYPE html>
<html>
  <head>
    {{ cdn_html_helper.get("package-name", "alias1") }}
  </head>
  <body>
    <!-- Your web content here -->
  </body>
</html>
```

In this example, `{{ cdn_html_helper.get("package-name", "alias1") }}` generates and safely renders the HTML tag for the specified package file.

### Configuration

CDNHTMLHelper supports various configuration options, including specifying local resources for addressing GDPR concerns and data privacy. You can configure local resources by providing the `local` and `local_url` parameters during initialization. You can set the local parameter to either True or provide a custom path to specify where the files will be stored locally. If True is used without specifying a path, a default storage location will be employed.

Here's an example of configuring local resources:

```python
from cdnhtmlhelper import CDNHTMLHelper

# Initialize CDNHTMLHelper with local resources to address GDPR concerns
cdn_helper = CDNHTMLHelper(local=True)

# Add packages and generate HTML tags as needed
cdn_helper.use("package-name", version="1.2.3", files={"file-alias": "file-name.css"})

# When using local resources, files will be downloaded to the static files folder
# and served from there to address GDPR compliance and data privacy concerns.
```

In this example, `local=True` indicates that local resources are enabled to address GDPR concerns and data privacy requirements. When using local resources, files will be automatically downloaded to the static files folder and served from there, ensuring GDPR compliance and data privacy protection.

## Dependencies

The `CDNHTMLHelper` relies on the following external Python packages:

- `requests`: Used for making HTTP requests to jsDelivr's API to fetch package information.
- `markupsafe`: Used for safely rendering HTML tags when integrated with Flask applications.

The required dependencies are included in the `requirements.txt` file, which is shipped with this repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contribution

Contributions and bug reports are welcome! Please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/dbautz/CDNHTMLHelper).

Enjoy using the `CDNHTMLHelper` class to simplify the process of including external JavaScript and CSS files in your web applications!

## Release History

- **0.1.4** (2023-10-08)

  - Fixed an issue where get would not return the proper values on omitted parameters

- **0.1.3** (2023-10-08)

  - Adding release to Github

- **0.1.2** (2023-10-08)

  - Added description to project

- **0.1.1** (2023-10-08)

  - Fixes to Documentation
  - Minor Formatting adjustments

- **0.1.0** (2023-10-07)

  - Initial release
