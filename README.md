# What it does

Simple Python script which converts a zipped SWORD module into [Obsidian](https://obsidian.md/) compatible Bible.
Each chapter is a separate Markdown document.
The structure is a direct copy of https://github.com/selfire1/BibleGateway-to-Obsidian.

# How to use

Download a zipped SWORD Bible module from http://www.crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles.

To run the script `setuptools` and `pysword` must be available in the Python path.
The project ships with a [Poetry](https://python-poetry.org/) setup.
If you have Poetry installed, simply run (example):

```shell
poetry shell
./main.py ~/Downloads/PolUGdanska.zip
```

This will output the structure into the current working directory.
You can then copy it into your Obsidian vault.

Locale translations are provided through a JSON file.
You can specify a different locale using `-l` flag.
Polish is the default for now.
Contributions are welcome to switch it to English as default.

# Acknowledgments

- https://github.com/selfire1/BibleGateway-to-Obsidian
- https://gitlab.com/tgc-dk/pysword
