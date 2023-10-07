# AutoRunX-Python
AutoRunX is an open source low code framework. The user only needs to run the script by entering the program flowchart configuration file.

If you are a company or organization, you can extend your code base based on this framework with your own products or use cases.


## Usage
1. Install
```sh
pip install autorunx
```

2. Used in Python
```python
import autorunx as arx
arx.run("config.json")
```

2. Used in Linux Command
```sh
autorunx -c "config.json"
```
or
```sh
arx -c "config.json"
```


## Build Release File

1. Build source distribution packages

Used to distribute a 'Python' module or project, packaging the source code into a 'tar.gz' or 'zip' package

```sh
python setup.py sdist # package, default tar.gz
python setup.py sdist --formats=gztar,zip # package, specifying the compression format
```

2. Build a binary distribution package

Multi-platform packaging

If your project needs to install multiple platforms, both Windows and Linux, according to the above method, a variety of formats we have to execute multiple commands, for convenience, you can step in place, execute the following command, you can generate multiple formats of the system

```sh
python setup.py bdist
```

Build wheel package

```sh
# pip install wheel
python setup.py sdist bdist_wheel
```

## Install By Setup.py

Use setup.py to install the package

```sh
python setup.py install
```

If your project is still in development and needs frequent updates, you can use the following command to install it. This method does not actually install the package, but creates a soft link in the system environment to the actual directory where the package is located. After modifying the package, it can take effect without installing it again, which is easy to debug.

```sh
python setup.py develop
```


## Release To PyPi

1. Register PyPi account and get the api token.
2. Create `~/.pypirc` (or `C:/User/${yourname}/.pypirc`) file and edit:
```ini
[distutils]
index-servers=pypi

[pypi]
username=__token__
password=your_token_input_here
```

3. Upload

Before uploading, you need to biuld first.

```
twine upload dist/*   # upload all files under dist folder
```








