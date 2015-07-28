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
    "files": [("http://jquery-json.googlecode.com/files/jquery.json-2.4.min.js", ".")],
}

jquery_validate = {
    "name": "jQuery.validate",
    "zips": [
        {"url": "http://jqueryvalidation.org/files/jquery-validation-1.13.1.zip",
        "unpack": [
            ("dist/jquery.validate.min.js", "./jquery.validate.min.js"),
        ]}
    ],
}

STATIC_LIBS = [jquery, jquery_ui, jquery_json, jquery_validate]
