---
layout: post
comments: true
title:  "Big-O notation"
excerpt: "Big-O notation에 대해 알아봅니다."
categories: java algorithm coursera Big-O
date:   2017-01-07 00:30:00
tags: [Java, Algorithm, Coursera, Big-O, logarithm]
---

<p>아래 내용은 Big-O notation을 이해하기 위해 stackOverFlow의 답변 내용을 번역한 것입니다. 본 질문은 다음과 같습니다.</p>
<a href="http://stackoverflow.com/questions/2307283/what-does-olog-n-mean-exactly">stackOverFlow 본 질문</a>

<p>또한, 이 내용만으로 설명이 저 개인적으로는 완벽하다고 생각하지 않아서 Khan academy의 내용을 추가적으로 첨부합니다. 내용 정리가 굉장히 잘 되어 있으니 참고하실 수 있을 것이라 생각됩니다.</p>
<a href="https://www.khanacademy.org/computing/computer-science/algorithms/asymptotic-notation/a/asymptotic-notation">Khan academy - Asymptotic notation</a>

#### The logarithm 1.

&nbsp;말의 목에 밧줄을 묶어놨다고 상상해보세요. 만약 밧줄을 말의 목에 바로 걸어두었다면 이것은 1입니다. 이제 밧줄을 막대기에 묶었다고 생각해보세요. 말은 밧줄을 당기기위해 더 많은 힘을 사용해야 합니다. 말이 밧줄을 당겨야 하는 시간은 밧줄의 강도와 막대기의 크기에 따라 다릅니다. 여기서 밧줄을 당기기 위해 자기 힘의 10배를 내야한다고 가정하겠습니다.

&nbsp;이제 밧줄이 막대기에 1번 감겨 있다면, 힘을 10배 더 내야합니다. 2번 감으면 100배, 3번 감으면 1,000배의 힘을 내야 하는 것이죠. 우리는 여기서 각각의 줄 감기가 힘을 10배 씩 늘리는 것을 확인할 수 있습니다. loagrithm이란 특정 수를 몇 번 곱해야 원하는 숫자가 나오는가에 대한 것입니다. 예를 들어, base가 10일 경우(log10 n) 3은 1,000의 로그이며, 6은 1,000,000의 로그입니다.

그렇다면, O(log n)은 무슨 의미일까요?

위의 예시에서는 *'성장률'* 이 O(log n)입니다. 각각의 추가적인 줄 감기는 매번 10배의 힘을 더 요구합니다.

| Turns | Max Force |
|:--------|:-------:|
| 0   | 1   |
| 1   | 10   |
| 2   | 100   |
| 3   | 1000   |
| n   | 10^n   |
{: rules="groups"}

위의 예시에서는 밑이 10인 예시이지만, Big O에서는 밑은 중요하지 않습니다. 이제 1-100 사이의 수를 찾는 게임을 상상해보겠습니다.

Your Friend: Guess my number between 1-100!
Your Guess: 50
Your Friend: Lower!
Your Guess: 25
Your Friend: Lower!
Your Guess: 13
Your Friend: Higher!
Your Guess: 19
Your Friend: Higher!
Your Friend: 22
Your Guess: Lower!
Your Guess: 20
Your Friend: Higher!
Your Guess: 21
Your Friend: YOU GOT IT!  

이 경우 7번의 추론이 필요했습니다. 그런데 여기에 들어간 관계는 무엇인가요? 하나의 추론이 추가될 때마다 알 수 있는 최대 숫자는 어떻게 될까요?

| Guesses | Items   |
|:--------|:-------:|
|  1      |   2     |
|  2      |   4     |
|  3      |   8     |
|  4      |   16    |
|  5      |   32    |
|  6      |   64    |
|  7      |   128   |
|  10     |   1024  |
{: rules="groups"}

&nbsp; 이 그래프를 확인해보면, 우리가 binary search를 사용할 경우 1-100 사이의 숫자를 찾는데에는 *최대* 7번의 추론이 필요합니다. 만약 1-128 사이의 숫자를 추론하려면 여전히 7번의 추론이면 충분하지만, 1-129의 사이의 숫자를 얻어내려면 8번의 추론이 필요합니다.(binary search는 밑이 2인 로그를 전제합니다.) 알아두어야 할 것은 Big O는 항상 최악의 경우를 전제로 합니다. 운이 좋다면 1번에 숫자를 찾아낼 수도 있습니다.

&nbsp;그렇다면 O(n log n)은 어떨까요? 이는 2개의 루프가 중첩되어 있을 때, 바깥의 루프가 n의 속도로 증가하고(O(n)), 안쪽 루프가 log n의 속도로 증가할 때(O(log n)), 전체 runnign time은 O(n) * O(log n) = O(n log n)이 됩니다.(ex - merge sort)



#### The logarithm 2.

logarithmic running-time 함수의 가장 흔한 속성은

* 어떤 행동을 수행할 다음 요소의 선택은 여러 가지 가능성 중 하나이다.
* 오직 1개만 선택되어야 한다.
또는
* 행동이 수행되는 요소는 n의 자리수이다.

&nbsp;이 속성 때문에 전화번호부에서 사람을 찾는 것이 O(log n)입니다. 우리는 원하는 결과값을 얻기 위해 모든 사람을 볼 필요가 없습니다. 대신, 우리는 divide-and-conquer(분할 정복)해서 전체를 다 보기 전에 작은 부분만 보고도 결과 값을 얻을 수 있습니다. 물론 전화번호 양이 많은 책을 찾는 것은 여전히 많은 시간이 듭니다. 하지만, 양이 증가하는 속도는 검색 속도보다 빠르게 늘어나지는 않습니다.
&nbsp;우리는 전화번호부 예시를 다른 종류의 running time 계산 문제로 확장할 수 있습니다. 우리는 전화번호부를 비즈니스(노란색), 특별한 이름과 사람들(흰색) 등으로 나눌 수 있습니다. 하나의 전화번호는 최대 1명의 개인 혹은 비즈니스에 할당됩니다. 우리는 또한 특정한 페이지를 펼치는 것이 constant time이 든다는 것을 가정합니다.

* O(1) (average case): 주어진 페이지에 사람의 이름이 있고, 바로 번호를 찾을 수 있는 경우
* O(log n): 사람의 이름을 주고, 전화번호부 책의 중간을 펼칩니다. 그리고 그 부분에 찾는 사람의 이름이 있는지 확인합니다. 이름이 펼친 부분에 없고, 이름 순서가 빠르다면, 책의 처음과 그 중간 지점의 중간을 새롭게 펼칩니다. 반대로 이름 순서가 느리다면 중간지점을 처음지점으로 두고 책의 끝을 마지막으로 두어 새로운 중간지점을 펼칩니다. 이 작업을 이름을 찾을 때까지 반복합니다.
* O(n): 전화번호에 숫자 5가 들어간 사람의 번호를 모두 찾는 작업
* O(n): 번호를 주고, 사람 또는 비즈니스 번호를 찾는 작업
* O(n log n): 전화번호 출력에 오류가 있어서 번호가 랜덤으로 정렬되었다. 이를 이름의 오름차순으로 정렬(AtoZ)하고, 차곡차곡 새로운 비어 있는 전화번호부에 등록하는 작업


> 내용 출처: The rope-logarithm example was grabbed from the excellent Mathematician's Delight book by W.Sawyer.
