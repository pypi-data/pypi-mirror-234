SmartDance

SmartDance is a Python package that brings the power of template languages to Python. Inspired by Handlebars and similar languages, SmartDance allows you to embed Python function calls and variables directly into your strings, which are then executed and replaced with their results when the string is processed.

> Designed specifically to work as a Prompt Engineering tool, SmartDance is a simple, flexible, and powerful way to generate strings from Python code.

## Features

- Simple Syntax: Use double curly braces {{}} to embed Python function calls and variables into your strings.
- Flexible: SmartDance can handle any function or variable that's in scope when the string is processed.
- Error Handling: Function execution is wrapped in a try/except block. If an exception is raised, a custom error message is returned.
Installation

You can install SmartDance with pip:

```
pip install smartdance
```

## Usage

```py
from smartdance import dance

def hello(name):
    return f"Hello, {name}!"

print(dance("{{hello('World')}}", locals()))
```

```
Output: Hello, World!
```

## Future Plans

- Complex Data Types: We plan to add support for complex data types like lists, dictionaries, and objects in the future.
- Debugging and Testing: We plan to add built-in functionality for debugging and testing in the future.
