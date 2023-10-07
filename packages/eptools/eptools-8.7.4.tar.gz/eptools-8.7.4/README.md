# EasyPost Tools

## How to deploy to PyPi

Reference: https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56


Manually change with new number in setup.cfg (increment it)

Upload to PyPi
 cd c:\EasypostLibrary\eptools
 python -m build
 python -m twine upload dist/*

Afterwards install it globaly:
> pip install eptools==&lt;version&gt;

E.g. "pip install -U eptools"


add config.py of with following methods!
    - slacktoken