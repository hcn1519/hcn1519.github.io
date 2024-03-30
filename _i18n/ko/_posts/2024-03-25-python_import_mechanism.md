---
layout: post
title: "Python Import Mechanism"
date: "2024-03-25 00:53:17 +0900"
excerpt: "Python의 Module Import에 대해 살펴봅니다."
categories: Python Module Package
tags: [Python, Module, Package]
table-of-contents: |
  ### Table of Contents
    1. [Python에서 다른 파일 import시 오류가 많은 이유](./python_import_mechanism#python에서-다른-파일-import시-오류가-많은-이유)
    2. [Python 파일에 다른 파일 import하여 사용하기](./python_import_mechanism#python-파일에-다른-파일-import하여-사용하기)
        1. [모든 module을 동일한 디렉토리에 두기](./python_import_mechanism#1-모든-module을-동일한-디렉토리에-두기)
        2. [의존성 해결을 위해 package 사용](./python_import_mechanism#2-의존성-해결을-위해-package-사용)
        3. [모듈 검색 경로 수정](./python_import_mechanism#3-모듈-검색-경로-수정)
    3. [Best Practices](./python_import_mechanism#best-practices)
translate: true
---


Python 프로젝트에서 다른 소스코드의 기능을 import하는 과정에서 잦은 에러를 마주치는 것은 흔한 일입니다. Python import system에 익숙하지 않은 개발자들은 이러한 에러를 피하기 위해, 모든 소스코드를 하나의 파일에 넣거나, 스크립트를 모두 하나의 디렉토리에 넣는 작업을 했을 수도 있습니다. 

이 글은 위와 같은 경험이 있는 개발자들의 Python의 import system에 대한 이해를 돕기 위해 작성되었습니다.

## Python에서 다른 파일 import시 오류가 많은 이유

파이썬을 사용할 때 개발자는 **경로 제약 없이** 스크립트를 실행할 수 있습니다. 이는 큰 장점이지만, 한편으로는 여러 파일의 참조를 구성할 때 주요한 기준점인 스크립트 수행 경로가 쉽게 바뀔 수 있다는 것을 의미하기도 합니다. 예를 들어서, 아래와 같은 프로젝트 구조를 생각해보겠습니다.

```
foo
├── bar
│   └── sample2.py
└── sample.py
```

여기에서 `foo`에서 `python3 sample.py`를 수행하는 것과 `bar` 디렉토리 안에서 `python3 ../sample.py`는 동일한 스크립트 파일을 실행합니다. 하지만, 둘의 스크립트 수행 경로는 `/foo`와 `/foo/bar`로 다르고 이는 큰 차이를 야기합니다. 그렇기 때문에 우리는 여러 소스 파일이 다양한 하위 디렉토리에 나누어진 프로젝트를 진행하고 있다면, 일반적으로 프로젝트 루트에서 프로젝트를 실행하는 것을 전제하고 프로젝트 코드를 구성합니다.


## Python 파일에 다른 파일 import하여 사용하기

Python은 `import` 문을 통해 다른 스크립트의 기능을 가져올 수 있습니다. Python 스크립트는 동시에 여러 스크립트와 컴파일되지 않기 때문에, 인터프리터는 가져온 정의나 함수를 찾을 때 디렉토리 구조에 의존합니다.

이 글에서는 import 문을 정의하는 다양한 방법을 다루고자 합니다.

### 1. 모든 module을 동일한 디렉토리에 두기

다른 정의를 가져오는 가장 쉬운 방법은 모든 스크립트 파일을 동일한 디렉토리에 두는 것입니다. 예를 들어, 아래와 같은 프로젝트가 있다고 가정해보겠습니다.

```
directory
├── message.py
└── sender.py
```

각 스크립트는 아래 코드를 포함합니다.

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
$ python3 script2.py
Message from script1
Send from script2
```

이 예제에서 `sender.py`는 `message`에서 `Message` 클래스를 `from message import Message` 문을 사용하여 가져옵니다. 위의 예제와 같이, 우리는 간단히 `from module import name` 형식으로 다른 스크립트의 정의나 문을 추가할 수 있습니다. 여기서 [module](https://docs.python.org/3/tutorial/modules.html)은 우리가 가져오고자 하는 기능을 갖춘 확장자(`.py`)가 없는 파일입니다.

왜 `import name` 형식으로 import 문을 정의하지 않는지 궁금할 수 있습니다. 이는 사용 가능하지만, `import` 후에 오는 `[name]` 부분은 모듈 또는 패키지(모듈의 모음)이어야 합니다. 그렇기 때문에 `module.name`(예: `msg = message.Message()`)과 같이 모듈 내의 기능을 사용할 때, 각 함수 또는 클래스의 전체 네임스페이스를 작성해야 접근이 가능합니다. 반면 `from message import Message` 형태의 statement는 별도의 네임스페이스 없이 모듈 내 기능에 접근할 수 있게 합니다.

### 2. 의존성 해결을 위해 package 사용

프로젝트가 커지면 모든 스크립트 파일을 하나의 디렉토리에 넣는 것이 어려워집니다. 아래 디렉토리 구조를 생각해보겠습니다.

```
directory
├── msgs
│   └── message.py
└── sender.py
```

이 예에서 `sender.py`와 `message.py`는 서로 다른 디렉토리에 있습니다. 그래서 위의 예시 파일의 `sender.py`를 실행하면 `ModuleNotFoundError`가 발생합니다.

```
$ python3 sender.py
Traceback (most recent call last):
  File "path/sender.py", line 2, in <module>
    from message import Message
ModuleNotFoundError: No module named 'message'
```

이 문제를 해결하는 몇 가지 방법이 있습니다. 가장 간단한 방법은 import 문을 `from msgs.message import Message`로 변경하면 됩니다. 이는 msgs 디렉토리를 package로 간주하여 내부의 모듈을 접근하는 방식입니다. [Package](https://docs.python.org/3/tutorial/modules.html#packages)는 모듈 네임스페이스를 지원하는 Python의 구조적인 방식으로 `.`을 연결하는 방식(`package.sub_package.module`)으로 서브 디렉토리 내부 모듈 접근을 지원합니다. Python은 디렉토리가 Python 소스코드 파일을 가지고 있을 때 이를 package로 인식합니다. 이는 `__init__.py` 파일을 디렉토리에 추가하여 명시적으로 이를 보여줄 수 있습니다.

```
directory
├── msgs
│   ├── __init__.py
│   └── message.py
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

> `__init__.py`는 import statement를 단순화하는 다양한 syntax sugar를 정의하는 데에 사용되기도 합니다. 예를 들어서, `__init__.py`에 `from message import Message`를 추가할 경우, `from msgs import Message` 형태로 `sender.py`에 statement를 작성할 수 있습니다.

### 3. 모듈 검색 경로 수정

모듈을 가져오는 또 다른 방법은 모듈 검색 경로를 수정하는 것입니다. Python 인터프리터가 스크립트에서 import 문을 감지할 때, 사용자가 가져오려는 모듈을 찾을 때 세 가지 경로를 검색합니다: 현재 실행 중인 스크립트 경로, `PYTHONPATH`, 그리고 `sys.path`의 경로입니다. 따라서 이 중 하나를 수정하여 모듈이 있는 경로를 추가하면 해당 모듈을 사용할 수 있습니다.

1. 현재 실행 중인 스크립트 경로: 스크립트를 실행하는 경로는 기본적으로 모듈 검색 경로에 포함됩니다. 그렇기 때문에 모듈을 실행하려는 스크립트와 동일한 디렉토리에 넣으면 해당 모듈은 접근 가능합니다.
1. `PYTHONPATH`: `PYTHONPATH`는 Python 인터프리터가 실행될 때 모듈을 검색 경로를 저장하는 환경 변수입니다. 다른 환경 변수와 마찬가지로 경로를 갱신하여 현재 세션에 적용할 수 있습니다. 또는 변경 사항을 영구적으로 적용하려면 `./zshrc` 또는 `./bashrc`에 해당 경로를 export하는 statement를 추가하면 됩니다.

    ```shell
    export PYTHONPATH=/path/to/msgs:$PYTHONPATH
    ```

1. 런타임에서 `sys.path` 수정

Python은 `sys.path`에 추가된 경로의 모듈들을 검색합니다. 따라서 모듈이 정의된 경로를 `sys.path`에 추가하면 Python이 해당 모듈을 사용할 수 있습니다.

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

## Best Practices

만약 프로젝트에 하위 디렉터리를 도입하고 싶다면, 권장하는 방법은 모듈과 패키지를 사용하는 것입니다. 프로젝트가 작고 하위 디렉터리가 필요하지 않다면, 모든 파이썬 소스 코드를 하나의 디렉터리에 두는 것이 가장 간단하고 바람직한 방법입니다. 프로젝트에 모듈이 많지 않다면 스크립트 실행시 [-m](https://docs.python.org/3/using/cmdline.html#cmdoption-m) 인자로 모듈 경로를 제공하는 것도 하나의 방법이 될 수 있습니다.

개인적으로 모듈 import 문제를 해결하는 데 module search path를 수정하는 것은 프로젝트의 규모가 커질 수록 피해야 하는 방법이라고 생각합니다.그 이유는 환경 변수는 해당 프로젝트 뿐만 아니라 다른 프로젝트도 사용하는 변수이기 때문에 이를 변경하면 다른 프로젝트에 side-effect이 발생할 수 있기 때문입니다. 또한, `sys.path`를 활용하는 방식은 개발자가 직접 런타임에 `sys.path.append()` 의 실행을 관리해야 합니다. 이는 일관적이지 않은 모듈 참조 환경을 쉽게 만들어 낼 수 있습니다. 단일 파일에서 `sys.path.append()`를 모아둔 파일을 항상 실행하도록 하는 것이 이 문제를 해결할 수 있지만, 이는 모든 소스 코드에 불필요한 의존성을 도입하고, 프로젝트에서 새 디렉토리를 만들고 싶을 때마다 해당 파일을 업데이트해야 합니다.

# 참고자료
- [Module](https://docs.python.org/3/tutorial/modules.html)
- [Package](https://docs.python.org/3/tutorial/modules.html#packages)
- [Python import system](https://docs.python.org/3/reference/import.html#importsystem)
- [Command line and environment](https://docs.python.org/3/using/cmdline.html#cmdoption-m)
