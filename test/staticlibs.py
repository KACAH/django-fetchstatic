__all__ = ["STATIC_LIBS"]

jquery = {
    "name": "jQuery",
    "files": [("http://code.jquery.com/jquery-1.8.2.min.js", ".")],
}

jquery_ui = {
    "name": "jQuery.ui",
    "files": [("http://code.jquery.com/ui/1.9.0/jquery-ui.js", ".")],
    "zips": [
        {"url": "https://github.com/downloads/jquery/jquery-ui/jquery-ui-themes-1.9.0.zip",
        "unpack": [("jquery-ui-themes-1.9.0/themes/cupertino", "theme/")],
        "only_min": False}
    ]
}

jquery_json = {
    "name": "jQuery.json",
    "files": [("http://jquery-json.googlecode.com/files/jquery.json-2.3.min.js", ".")],
}

bootstrap = {
    "name": "bootstrap",
    "zips": [
        {"url": "http://twitter.github.com/bootstrap/assets/bootstrap.zip",
        "unpack": [
            ("bootstrap/css", "css/"),
            ("bootstrap/js", "js/"),
            ("bootstrap/img", "img/")
        ],
        "only_min": True}
    ]
}

qtip = {
    "name": "jQuery.qtip",
    "files": [
        ("http://craigsworks.com/projects/qtip2/packages/latest/jquery.qtip.min.js", "."),
        ("http://craigsworks.com/projects/qtip2/packages/latest/jquery.qtip.min.css", "."),
    ]
}

STATIC_LIBS = [jquery, jquery_ui, jquery_json, qtip, bootstrap]
