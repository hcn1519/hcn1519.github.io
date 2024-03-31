---
layout: post
title: "Python Import Mechanism"
date: "2024-03-25 00:53:17 +0900"
excerpt: "Exploring Python Module Import System"
categories: Python Module Package
tags: [Python, Module, Package]
table-of-contents: |
  ### Table of Contents
    1. [Reasons for frequent errors when importing other files in Python](./python_import_mechanism#reasons-for-frequent-errors-when-importing-other-files-in-python)
    2. [Importing other files into Python files](./python_import_mechanism#importing-other-files-into-python-files)
        1. [Placing all modules in the same directory](./python_import_mechanism#1-placing-all-modules-in-the-same-directory)
        2. [Using packages to resolve dependencies](./python_import_mechanism#2-using-packages-to-resolve-dependencies)
        3. [Modifying Module Search Paths](./python_import_mechanism#3-modifying-module-search-paths)
    3. [Best Practices](./python_import_mechanism#best-practices)
translate: true
---

Encountering frequent errors while importing functionalities from other source code in a Python project is common. Developers unfamiliar with Python's import system may mitigate these errors by either consolidating all source code into one file or placing all scripts in a single directory.

This article is written to aid developers with such experiences in understanding Python's import system better.

## Reasons for frequent errors when importing other files in Python

When using Python, developers can execute scripts **without path constraints**. While this is a significant advantage, it also means that the script execution path, which serves as a key reference point when organizing references across multiple files, can easily change. For example, consider the project structure below:

```
foo
├── bar
│   └── sample2.py
└── sample.py
```

Here, executing `python3 sample.py` from the `foo` directory and `python3 ../sample.py` from the `bar` directory both run the same script file. However, their script execution paths differ, `/foo` and `/foo/bar`, respectively, which can lead to significant differences. Therefore, when working on projects where multiple source files are divided into various subdirectories, it is generally assumed that the project is executed from the project root, and the project code is organized accordingly.

## Importing other files into Python files

Python allows importing functionalities from other scripts using the `import` statement. Since Python scripts are not compiled simultaneously with multiple scripts, the interpreter relies on the directory structure when locating imported definitions or functions.

This part aims to cover various methods of defining import statements.

### 1. Placing all modules in the same directory

The easiest way to import different definitions is to place all script files in the same directory. For example, let's consider a project structure like the following:

```
directory
├── message.py
└── sender.py
```

Each script contains the following code:

```python
# message.py
class Message:
    def foo(self):
        print("Message from script1")
```
```python
# sender.py
from message import Message

class Sender:
    def send(self):
        msg = Message()
        msg.foo()
        print("Send from script2")

if __name__ == "__main__":
    sender = Sender()
    sender.send()
```

```
$ python3 sender.py
Message from script1
Send from script2
```

In this example, `sender.py` imports the `Message` class from `message` using the `from message import Message` statement. As shown above, we can simply add definitions or statements from other scripts using the `from module import name` format. Here, [module](https://docs.python.org/3/tutorial/modules.html) refers to a file without an extension (`.py`) containing the functionalities we want to import.

You might wonder why we don't define import statements using the `import [name]` format. While this is possible, the `[name]` following the `import` must be a module or package (a collection of modules). Therefore, when using the `import [name]` form, you need to write the full namespace for each function or class when accessing them within the module (e.g., `msg = message.Message()`). On the other hand, the `from message import Message` statement allows access to functionalities within the module without a separate namespace.

### 2. Using packages to resolve dependencies

As projects grow, putting all script files into a single directory becomes impractical. Let's consider the directory structure below:

```
directory
├── msgs
│   └── message.py
└── sender.py
```

In this example, `sender.py` and `message.py` are in different directories. Therefore, running `sender.py` from the example files above results in a `ModuleNotFoundError`:

```
$ python3 sender.py
Traceback (most recent call last):
  File "path/sender.py", line 2, in <module>
    from message import Message
ModuleNotFoundError: No module named 'message'
```

There are several ways to solve this problem. The simplest way is to change the import statement to `from msgs.message import Message`. This treats the `msgs` directory as a package and accesses the module inside it. [Packages](https://docs.python.org/3/tutorial/modules.html#packages) are a structured way in Python that supports module namespaces, allowing access to modules within subdirectories by using dots (`package.sub_package.module`). Python recognizes a directory as a package when it contains Python source code files. This can be explicitly indicated by adding an `__init__.py` file to the directory:

```
directory
├── msgs
│   ├── __init__.py
│   └── message.py
└── sender.py
```

```python
# sender.py
from msgs.message import Message # changed

class Sender:
    def send(self):
        msg = Message()
        msg.foo()
        print("Send from script2")

if __name__ == "__main__":
    sender = Sender()
    sender.send()
```

> `__init__.py` is also used to define various syntax sugars that simplify import statements. For example, adding `from message import Message` to `__init__.py` allows writing the statement in `sender.py` as `from msgs import Message`.
### 3. Modifying Module Search Paths

Another way to import modules is by modifying the module search paths. When the Python interpreter encounters an import statement in a script, it searches for the module the user wants to import in three locations: the current script's directory, `PYTHONPATH`, and the paths in `sys.path`. Therefore, by modifying any of these, you can add the path where the module exists and make the module accessible.

1. Current Script's Directory: By default, the directory where the script is executed is included in the module search path. So, if you place the module in the same directory as the script you're running, the module will be accessible.

2. `PYTHONPATH`: `PYTHONPATH` is an environment variable that stores the module search paths when the Python interpreter is invoked. Like other environment variables, you can update it to apply changes for the current session. Alternatively, if you want changes to be permanent, you can add a statement to export the path to `./zshrc` or `./bashrc`.

    ```shell
    export PYTHONPATH=/path/to/msgs:$PYTHONPATH
    ```

3. Modifying `sys.path` at Runtime

    Python searches for modules in the paths added to `sys.path`. Therefore, by adding the path where the module is defined to `sys.path`, Python can access that module.

    ```python
    import sys
    sys.path.append("path/of/msgs")

    from msgs import Message

    class Sender:
        def send(self):
            msg = Message()
            msg.foo()
            print("Send from script2")

    if __name__ == "__main__":
        sender = Sender()
        sender.send()
    ```

These methods allow you to customize the module search paths according to your project structure and make the required modules accessible to your scripts.

## Best Practices

If you intend to introduce subdirectories into your project, the recommended approach is to use modules and packages. However, if your project is small and does not require subdirectories, placing all Python source code in a single directory is the simplest and most desirable method. If your project has only a few modules, providing the module path as an argument using the [-m](https://docs.python.org/3/using/cmdline.html#cmdoption-m) option when executing scripts can also be a viable approach.

Personally, I believe that modifying the module search path to resolve module import issues becomes less favorable as the project scales. The reason is that environment variables are shared across projects, so modifying them can lead to side effects in other projects. Additionally, using `sys.path` requires developers to manage `sys.path.append()` calls at runtime, leading to inconsistent module reference environments. While creating a file where `sys.path.append()` calls are centralized and ensuring it is always executed can mitigate this issue, it introduces unnecessary dependencies to all source code and requires updating the file every time a new directory is added to the project.

In conclusion, while modifying the module search path can be a temporary solution for small projects, it is not recommended for larger projects due to potential side effects and maintenance overhead. Instead, leveraging modules and packages is a more robust and scalable approach for organizing Python projects with subdirectories.

# References
- [Module](https://docs.python.org/3/tutorial/modules.html)
- [Package](https://docs.python.org/3/tutorial/modules.html#packages)
- [Python import system](https://docs.python.org/3/reference/import.html#importsystem)
- [Command line and environment](https://docs.python.org/3/using/cmdline.html#cmdoption-m)
