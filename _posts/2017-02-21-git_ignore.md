---
layout: post
comments: true
title:  "Git ignore"
excerpt: "github에 프로젝트를 올릴 때 파일을 제외하는 방법을 알아봅니다."
categories: Git Ignore
date:   2017-02-21 00:30:00
tags: [Git, Ignore]
---

git을 사용할 때, github에 올리면 안되는 파일 혹은 폴더들이 있습니다. 이런 파일들이 github에 올라가지 않도록 도와주는 것이 <code>.gitignore</code>입니다. <code>.gitignore</code>을 사용하는 것은 간단합니다. 먼저 프로젝트의 root 폴더에서 <code>.gitignore</code>파일을 생성합니다.

{% highlight shell %}
vim .gitignore
{% endhighlight %}

이렇게 하면 <code>.gitignore</code> 파일이 생성되고, 해당 파일 안에 제외하고자 하는 파일을 넣어주면 됩니다.

{% highlight shell %}
// .gitignore
Info.plist
Pods/
xcuserdata/
*.lock
{% endhighlight %}

특정 파일을 제외시키고자 할 때는 파일명을 그대로 써주면 됩니다. 폴더의 경우에는 <code>Pods/</code>처럼 뒤에 <code>/</code>를 붙여주어야 합니다. 특정 확장자를 가진 모든 파일을 제외하고자 할 경우에는 <code>*.lock</code>처럼 <code>*</code>를 사용하면 됩니다.

<br/>

## 이미 올라간 파일들을 github에서 제외하기

사실 처음에 이렇게 제외할 파일들을 미리 설정하지 않고 <code>commit</code>을 해버리는 경우가 종종 발생합니다. 이 때는 캐시된 파일들을 <code>refresh</code>해주고 새롭게 <code>add</code>를 해야합니다.

{% highlight shell %}
git rm --cached -r .
{% endhighlight %}

이렇게 해주고 나서, 다시 <code>add</code>, <code>commit</code>, <code>push</code>의 단계를 거치면 <code>gitignore</code>가 정상 작동하게 됩니다.
