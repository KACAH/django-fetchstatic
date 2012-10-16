__all__ = ["STATIC_LIBS"]

jquery = {
    "js": ["http://code.jquery.com/jquery-1.8.2.min.js"],
}

jquery_ui = {
    "js": ["http://code.jquery.com/ui/1.9.0/jquery-ui.js"],
    "theme": ["https://github.com/downloads/jquery/jquery-ui/jquery-ui-themes-1.9.0.zip",
              "jquery-ui-themes-1.9.0/themes/cupertino"],
}

jquery_json = {
    "js": ["http://jquery-json.googlecode.com/files/jquery.json-2.3.min.js"],
}

bootstrap = {
    "js": ["https://raw.github.com/twitter/bootstrap/master/docs/assets/js/bootstrap.min.js"],
    "images": ["https://raw.github.com/twitter/bootstrap/master/img/glyphicons-halflings-white.png",
               "https://raw.github.com/twitter/bootstrap/master/img/glyphicons-halflings.png"],
    "css": ["http://twitter.github.com/bootstrap/assets/css/bootstrap-responsive.css",
            "http://twitter.github.com/bootstrap/assets/css/bootstrap.css"],
}

qtip = {
    "js": ["http://craigsworks.com/projects/qtip2/packages/latest/jquery.qtip.min.js"],
    "css": ["http://craigsworks.com/projects/qtip2/packages/latest/jquery.qtip.min.css"],
}

libraries = (jquery, jquery_ui, jquery_json, bootstrap, qtip)

STATIC_LIBS = {
    "libraries" : libraries,
    "fetch_directory" : "./fetched_static/"
}
