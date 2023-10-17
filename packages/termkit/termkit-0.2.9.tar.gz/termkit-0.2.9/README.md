<p align="center">
    <img alt="" title="Termkit" src="docs/images/banner.png#gh-dark-mode-only" width="450">
    <img alt="" title="Termkit" src="https://raw.githubusercontent.com/thmahe/termkit/master/docs/images/banner_light.png#gh-light-mode-only" width="450">
</p>
<p></p>
<div align="center">
  <b><i>Command Line Tools with... ease.</i></b>
<hr>

</div>

## Introduction

Termkit is a Python framework designed for building command line interface applications using functions 
and type hints [[PEP 484]](https://peps.python.org/pep-0484/). 
**Solely written using [Python Standard Library](https://docs.python.org/3/library/)** and will always be to ensure
minimal dependency footprint within your project.

## Features

- Build CLI Tools from functional code
- Create fast prototypes using implicit arguments
- Compatible with [argcomplete](https://pypi.org/project/argcomplete/) for autocompletion

## Usage

To get started, follow these steps:

#### 1. Install Termkit using pip
```shell
$ pip install termkit
```
#### 2. Test it with given example

```python
# app.py
from termkit import Termkit

app = Termkit()

@app.command()
def greet(name, count=2):
    for _ in range(count):
        print(name)

if __name__ == "__main__":
    app()

```
```shell
$ python3 ./app.py "Hello Termkit" --count 3
Hello Termkit
Hello Termkit
Hello Termkit
```


## Work in Progress Disclaimer

🛠️ **Please Note: This documentation is a work in progress.** 🛠️

Termkit is constantly evolving, and we are actively working on expanding and improving this documentation. Some sections may be incomplete or subject to change. We appreciate your patience and understanding as we continue to enhance this resource.

If you have any questions or encounter any issues while using Termkit, please feel free to reach me at [contact@tmahe.dev](mailto:contact@tmahe.dev).

Thank you for being a part of Termkit journey! 🌟
