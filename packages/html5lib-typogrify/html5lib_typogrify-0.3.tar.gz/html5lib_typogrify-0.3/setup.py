from setuptools import setup


setup(
    name="html5lib_typogrify",
    version="0.3",
    author="Alexandre Leray",
    author_email="alexandre@stdin.fr",
    description=("Corrects common typographical mistakes."),
    url="https://github.com/aleray/html5lib_typogrify",
    packages=[
        "html5lib_typogrify",
        "html5lib_typogrify.french",
        "html5lib_typogrify.french.filters",
    ],
    include_package_data=True,
    install_requires=["html5lib>=1.0.1,<1.2", "Pyphen>=0.9.5,<1.15"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
)
