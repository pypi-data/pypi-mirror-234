# pyright: reportMissingImports=false, reportUnusedVariable=warning
from CDNHTMLHelper import CDNHTMLHelper

cdn_html_helper = CDNHTMLHelper(local=True)

cdn_html_helper.use("jquery", version="3.7.1")
cdn_html_helper.use(
    "bootstrap", files={"bundle": "bootstrap.bundle.min.js", "css": "bootstrap.min.css"}
)
cdn_html_helper.use("bootstrap-icons")

print(cdn_html_helper.get())

# <script
#   src="resources/npm/jquery@3.7.1/dist/jquery.min.js"
#   integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" crossorigin="anonymous"
# ></script>
# <script
#   src="resources/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
#   integrity="sha256-gvZPYrsDwbwYJLD5yeBfcNujPhRoGOY831wwbIzz3t0="
#   crossorigin="anonymous"
# ></script>
# <link
#   rel="stylesheet"
#   href="resources/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
#   integrity="sha256-MBffSnbbXwHCuZtgPYiwMQbfE7z+GOZ7fBPCNB06Z98=""
#   crossorigin="anonymous"
# />
# <link
#   rel="stylesheet"
#   href="resources/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.min.css"
#   integrity="sha256-6MNujrdbV0Z7S927PzUMXOmMLwkKdsdD7XIl/w89HMQ="
#   crossorigin="anonymous"
# />
