---
layout: post
comments: true
title:  "Java파일 컴파일해서 실행하기"
excerpt: "콘솔에서 java 파일을 컴파일해서 실행하는 방법을 알아봅니다."
categories: Java Language
date:   2016-12-21 00:30:00
tags: [Java, Language]
---

<p>&nbsp;자바를 처음 배우게 되면, 대부분 eclipse(처음에 거의 안 쓰지만, Intellij)같은 IDE를 설치해서 자바 파일을 실행합니다. 하지만, 이런 IDE 없이 openjdk(그냥 jdk를 설치하면 됩니다.)만 설치되어 있다면, 자바로 짠 코드를 컴파일하고 실행할 수 있습니다. 순서는 다음과 같습니다.</p>

<h4>1. jdk가 설치되어 있는지 먼저 확인합니다.</h4>
{% highlight html %}
javac -version
{% endhighlight %}

<h4>2. javac "java파일 이름"을 실행합니다.</h4>
<p>&nbsp;여기서는 <code>APlusB.java</code>라는 파일을 컴파일해보겠습니다.</p>
{% highlight html %}
javac  APlusB.java
{% endhighlight %}

<h4>3. java "java클래스 이름"을 하면 컴파일된 프로그램이 실행됩니다.</h4>
{% highlight html %}
java APlusB
{% endhighlight %}

<p>&nbsp;결과는 다음과 같습니다.</p>
<img src="https://dl.dropbox.com/s/zce4iel68dbk91d/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202016-12-21%20%EC%98%A4%ED%9B%84%203.45.17.png">
