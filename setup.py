from distutils.core import setup

setup(
    name="django-fetchstatic",
    version="0.1",
    description="Fetcher for Django static files",
    author="KACAH",
    author_email="kacah222@gmail.com",
    url="https://github.com/KACAH/django-fetchstatic",
    packages=[
        "fetchstatic", 
        "fetchstatic.management",
        "fetchstatic.management.commands",
        "fetchstatic.templatetags",
    ],
)
