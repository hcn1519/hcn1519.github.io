---
layout: post
comments: true
title:  "Git ignore"
excerpt: "github에 프로젝트를 올릴 때 파일을 제외하는 방법을 알아봅니다."
categories: Git Github Ignore
date:   2017-02-21 00:30:00
tags: [Git]
translate: false
---

git을 사용할 때, github에 올리면 안되는 파일 혹은 폴더들이 있습니다. 이런 파일들이 github에 올라가지 않도록 도와주는 것이 <code>.gitignore</code>입니다. <code>.gitignore</code>을 사용하는 것은 간단합니다. 먼저 프로젝트의 root 폴더에서 <code>.gitignore</code>파일을 생성합니다.

{% highlight shell %}
vim .gitignore
{% endhighlight %}

이렇게 하면 <code>.gitignore</code> 파일이 생성되고, 해당 파일 안에 제외하고자 하는 파일을 넣어주면 됩니다.

{% highlight shell %}
# .gitignore
Info.plist
Pods/
xcuserdata/
*.lock
{% endhighlight %}

특정 파일을 제외시키고자 할 때는 파일명을 그대로 써주면 됩니다. 폴더의 경우에는 <code>Pods/</code>처럼 뒤에 <code>/</code>를 붙여주어야 합니다. 특정 확장자를 가진 모든 파일을 제외하고자 할 경우에는 <code>*.lock</code>처럼 <code>*</code>를 사용하면 됩니다.

<br/>

## 이미 올라간 파일들을 github에서 제외하기

처음부터 <code>.gitignore</code>을 생성하고 작업을 진행한 경우 위의 작업만 하면 되지만, 이미 프로젝트를 <code>commit</code>했을 경우에는 위의 작업을 진행해도 올바르게 <code>.gitignore</code>이 작동하지 않습니다. 이 때는 캐시된 파일들을 <code>refresh</code>(github에서 파일을 삭제)해주고 새롭게 <code>add</code>를 해야합니다. 이 때 이미 올라간 파일을 지우는 명령어는 다음과 같습니다.

{% highlight shell %}
git rm --cached -r .
{% endhighlight %}

위 명령어를 치면 다음과 같이 변경된 파일들의 목록들이 쭉 나타납니다.

<img src="https://dl.dropbox.com/s/p41b9a8qdk6jiby/ignore.png">

이 후 다시 <code>add</code>, <code>commit</code>, <code>push</code>의 단계를 거치면 <code>gitignore</code>가 정상 작동하게 됩니다.
