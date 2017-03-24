---
layout: post
comments: true
title:  "다중 Thread 프로그래밍"
excerpt: "Operating System Concepts에 기반한 정리입니다."
categories: OS Thread Java
date:   2017-03-20 00:30:00
tags: [OS, Thread, Java]
image:
  feature: thread.png
---

## 여러 작업을 하는 운영체제

코어가 1개인 CPU는 본질적으로 한 순간에 1개의 일밖에 할 수 없습니다. 그런데 현대의 컴퓨터는 컴퓨터를 킨 순간부터 여러 개의 작업을 수행합니다. 물론, 현대의 컴퓨터는 1 코어보다는 멀티 코어가 대중화되어 있습니다. 다만 그 코어의 개수도 개인 컴퓨터 수준에서는 4~8개 수준이므로, 하나의 컴퓨터는 한 순간에 4~8개의 작업만 수행할 수 있습니다. 하지만, 개인 컴퓨터들은 이보다 더 많은 일을 수행합니다. 이것이 어떻게 가능할까요?

<!-- process 이미지 -->
<img src="https://dl.dropbox.com/s/sud3gn15aa6xvf9/process.png">

많은 작업을 동시다발적으로 가능하게 하는 것은 바로 **Process** 입니다. 하나하나 켜진 프로그램들은 운영체제에서 **Process** 라고 부릅니다. 엄밀한 의미에서 "**Process** = 프로그램"은 아니지만, 이렇게 이해해도 크게 문제는 없습니다.

이제 우리가 이해한 컴퓨터들은 300여 개의 일을 **Process** 를 통해 가능하게 해줍니다. 하지만, 이것만으로 충분하지는 않습니다. 예를 들어 1개의 웹 서버가 300명의 클라이언트밖에 수용할 수 없다면, 하루 방문자 수(클라이언트)가 수천 만에 달하는 곳들은 운영을 할 수 없을 것입니다.(소위 말해 서버가 계속 터질 것입니다.) 즉, **Process** 안의 세분화된 또 다른 개념의 도입이 필요해진 것입니다.

## Thread 개념

여기서 도입되는 것이 **Thread** 입니다. 먼저 **Thread** 의 기본 개념 및 구성에 대해 살펴보면 다음과 같습니다.

<div class="message">
Thread는 <span style="font-weight: bold">CPU 이용의 기본 단위</span> 입니다. Thread는 스레드 ID, 프로그램 카운터, 레지스터 집합, 스택으로 구성되며, 같은 프로세스에 속한 다른 스레드와 코드, 데이터 섹션 외 운영체제 자원을 공유합니다.
</div>

<img src="https://hcn1519.github.io/public/assets/thread.png">

**Thread** 는 프로세스 안에서 만들어지는 것들로, 프로세스들의 자원들을 공유합니다. 앞서 예를 들었던 웹 서버라는 프로세스가 다중 **Thread** 로 클라이언트에 대해 응답하는 방식을 살펴보면 아래 그림과 같습니다.

<!-- thread2 이미지 -->
<img src="https://dl.dropbox.com/s/8t4xfa3fktgw3kx/thread2.png">

여기서는 크게 3 가지의 **Thread** 를 생성합니다.

1. 클라이언트의 요청을 listen하는 **Thread**
2. 요청에 대해 서비스할 **Thread**
3. 추가적인 요청을 listen하는 **Thread**

즉, 웹 서버에 동시에 여러 사람이 요청을 보내올 때 하나의 프로세스가 각각의 클라이언트에 응대하는 것이 아니라, 각각의 반복적인 업무를 가지고 있는 여러 개의 **Thread** 를 생성하여 동시다발적으로 클라이언트에 대응(listen)하는 형태인 것입니다.

<div class="message">
정리하자면, <span style="font-weight: bold">Thread</span> 는 프로세스에서 이뤄지는 여러 가지 반복되는 일들을 세분화하여 작업을 수행하는 것이라고 할 수 있습니다.
</div>

#### Thread의 장점

**Thread** 사용의 장점은 다음과 같습니다.

1. 응답성(responsiveness) - 응용 프로그램이 긴 작업을 시행할 경우에도 스레드를 통해 또 다른 프로그램을 실행할 수 있다.
2. 자원 공유(resource sharing) - 한 응용 프로그램이 같은 주소 공간 내에서 여러 개의 다르 작업을 하는 스레드를 가질 수 있게 한다.
3. 경제성(economy) - 프로세스 생성보다 경제적
4. 규모 가변성(scalability) - 다중 CPU 상황에서 여전히 병렬적으로 일을 수행할 수 있다.

## Thread 예시(Java)


> 참고자료 : Operating System Concepts 8th edition
