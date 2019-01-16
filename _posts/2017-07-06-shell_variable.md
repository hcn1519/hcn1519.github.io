---
layout: post
comments: true
title:  "Shell에서 변수 사용하기"
excerpt: "예제를 통해 Shell 변수에 대해 알아보겠습니다."
categories: Shell Linux Language
date:   2017-07-06 00:30:00
tags: [Shell, Linux, Language]
image:
  feature: linux.png
---

## Shell 기본 변수

Shell에서 사용되는 변수는 기본적으로 `$`를 앞에 붙여서 사용됩니다.

{% highlight Bash shell scripts %}
$ var=10
$ echo var // 결과: var
$ echo $var // 결과: 10
{% endhighlight %}

위의 예시에서 var에 10을 주고, 접근하기 위해서는 `$var`의 형태를 사용해야 합니다.

## Shell의 지정된 변수들

Shell에는 미리 지정되어 있는 몇 가지 변수들이 있습니다. `$HOME`, `$SHELL`, `$PWD`, `$PATH` 등이 미리 전역으로 지정되어 있는 경로 변수들입니다. 위의 변수들이 하는 역할은 다음과 같습니다.

- $HOME : 홈디렉토리의 경로를 저장합니다.(`/Users/name` 형태)
- $SHELL : 사용하고 있는 배쉬의 경로를 저장합니다.(`/bin/bash` 형태)
- $PWD : 현재 위치한 경로를 저장합니다.(`/Users/name/Desktop` 형태)
- $PATH : 전역에서 접근할 수 있는 디렉토리들의 경로를 저장합니다. 여러 경로들을 `:`을 통해 구분하여 저장합니다.

## Shell의 파라미터 사용

또한 Shell은 스크립트를 실행할 때 파라미터를 전송할 수 있습니다. 그리고 파라미터들은 스크립트 내에서 `$0`, `$1`, `$2`의 형태로 접근할 수 있습니다. 예시를 통해 알아보겠습니다. 먼저 `hello.sh`를 생성하고 다음 내용을 넣어줍니다.

{% highlight Bash shell scripts %}
# hello.sh
#!/bin/Bash
echo "Hello $0"
echo "Hello $1"
echo "Hello $2"
{% endhighlight %}

위와 같이 스크립트를 작성하게 되면 `$0`, `$1`, `$2`에 각각 어떤 내용이 나타나는지 알 수 있습니다. 이제 해당 스크립트를 실행해봅니다.

{% highlight Bash shell scripts %}
$ ./hello.sh Tom Sam
   ^--$0     ^--$1 ^--$2
# 출력 결과
# Hello ./hello.sh
# Hello Tom
# Hello Sam
{% endhighlight %}

파라미터는 계속해서 뒤에 추가적으로 붙여줄 수 있으며 번호가 증가하는 형태로 접근할 수 있습니다.

## 새로운 변수 사용하기(export, source)

위의 예시에서 `var=10`과 같은 명령이 만드는 변수는 **쉘 변수** 라고 부릅니다. 이 **쉘 변수** 는 bash에서 생성했을 때 bash에서만 사용할 수 있습니다. 즉, 다른 `temp.sh`를 만들고 변수 `var`에 접근할 수 없습니다. 이 때, 해당 변수에 접근하도록 만들어주는 명령어가 `export`입니다. `export var=10`으로 명령을 내리면 이는 bash와 그 fork된 자식(이 때, bash는 모든 shell의 최상위에 있으므로 bash상에서 `export var=10`으로 선언하면 `var`는 모든 쉘에서 사용할 수 있습니다.)에서 사용할 수 있는 **환경변수** 가 됩니다. 예를 들면,

{% highlight Bash shell scripts %}
$ export var=10
$ vim hello2.sh
{% endhighlight %}

으로 `hello2.sh`를 생성합니다. 그리고 다음 내용을 작성합니다.

{% highlight Bash shell scripts %}
# hello2.sh
#!/bin/bash
{% endhighlight %}

그 결과는 다음과 같습니다.

{% highlight Bash shell scripts %}
$ echo $var
$ ./hello2.sh #결과: 10
{% endhighlight %}
