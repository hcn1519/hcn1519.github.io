---
layout: post
comments: true
title:  "Greedy algorithm(탐욕 알고리즘)"
excerpt: "Greedy algorithm에 대해 알아봅니다."
categories: java algorithm greedy_algorithm coursera
date:   2017-01-02 00:30:00
tags: [Java, Algorithm, Greedy, Coursera]
---

<h4>Greedy algorithm이란?</h4>
<p>&nbsp;탐욕 알고리즘은 최적해를 구하는 데에 사용되는 근사적인 방법으로, 여러 경우 중 하나를 결정해야 할 때마다 그 순간에 최적이라고 생각되는 것을 선택해 나가는 방식으로 진행하여 최종적인 해답에 도달한다.(출처 : 위키피디아)</p>

<h4>Greedy algorithm의 과정</h4>

<p>&nbsp;Greedy algorithm는 3가지 절차를 거친다. 이는,</p>
<ol>
  <li>Make some greedy choice.</li>
  <li>Reduce to a smaller subproblem.</li>
  <li>Iterate.</li>
</ol>

<p>&nbsp;인데, 이를 약간 해석하자면,</p>
<ol>
  <li>가장 탐욕스런 선택을 한다.</li>
  <li>문제를 조금 더 작은 문제로 분해한다.</li>
  <li>반복한다.</li>
</ol>

<p>&nbsp;다음과 같다. 물론 이것만으로는 조금 부족하다. 이 과정을 보완하는 방법으로 첫 번째 선택이 실제로 최적의 선택인지를 증명하는 과정이 필요한데, 그 과정에서 나오는 것이 <code>safe move</code>이다.</p>

<h4>Safe move란?</h4>
>Greedy choice 중 "첫 번째로 선택한 것"이 "최적의 선택과 일치"할 경우 이를 Safe move라 한다.

<p>&nbsp;Greedy algorithm은 첫 번째 선택이 safe move라는 것을 증명해야만 올바른 답을 얻을 수 있다. 이에 맞춰 과정을 다시 한 번 정리하면,</p>

<ol>
  <li>가장 탐욕스런 선택을 한다.</li>
  <li style="color:#b20000">이 선택이 safe move인지 증명한다.</li>
  <li>문제를 조금 더 작은 문제로 분해한다.</li>
  <li>반복한다.</li>
</ol>

<p>&nbsp;다음과 같이 정리될 수 있다.</p>

<h4>Fractional Knapsack 문제</h4>

<p>&nbsp;Greedy 알고리즘의 가장 대표적인 문제로 언급되는 것이 Knapsack 문제입니다. 문제는 다음과 같습니다.</p>

<img src="https//dl.dropbox.com/s/5x37ekxmdsxtq7s/knapsack.png">

>배낭을 매고 긴 여행을 떠난다. 배낭에 담을 수 있는 총 무게와 담을 수 있는 물건의 가짓수가 주어진다. 물건에는 모두 value가 있고, 가지고 있는 총량도 정해져 있다. 이 때 value가 최대가 되도록 가방을 싸고, 최대 value 값을 출력하시오.(ex) 물건 가짓수 : 3, 가능한 무게 : 50, 물건1 : value - 60, weights - 20, 물건2 : value - 100, weights - 50, 물건1 : value - 120, weights - 30 경우 180 출력)

<img src="https//dl.dropbox.com/s/u7qe6w9dk6kvdx0/sample.png">

<p>&nbsp;이 문제를 풀 때 Greedy 알고리즘의 방식에 따라 가장 탐욕스러운 선택을 하되, 그 선택이 safe move인지 판단한 후 이를 반복하는 과정을 진행합니다. 여기서의 safe move는 바로, 무게당 value가 가장 큰 물건을 먼저 배낭에 담는 것입니다. 즉, value/weight의 값이 가장 큰 값을 먼저 가방에 집어 넣는 것이죠.</p>

{% highlight html %}
Knapsack(W, w1, v1, . . . , wn, vn)
  A ← [0, 0, . . . , 0], V ← 0
  repeat n times:
  if W = 0:
    return (V , A)
  select i with wi > 0 and max vi
  wi
  a ← min(wi ,W)
  V ← V + a vi/wi
  wi ← wi−a, A[i] ← A[i]+a, W ← W−a
return (V , A)
{% endhighlight %}

<p>&nbsp;이를 수도 코드로 표현하면 다음과 같습니다. 가방의 무게가 0이 될 때까지 루프가 돌고, vi/wi가 최대인 값을 찾아서 가방에서 뺄 수 있는만큼 빼는 작업을 반복합니다. 이 코드는 제대로 작동하는 코드이긴 합니다만 Big-O가 크다는 문제점을 지니고 있습니다. value/weight의 값을 찾는 과정이 O(n)이고, 전체 루프가 O(n)이어서 최악의 경우 n^2 횟수만큼 코드가 돌아야 하기 때문에 Big-O가 O(n^2)이기 때문입니다.</p>
<p>&nbsp;그런데 이 Big-O는 쉽게 줄어들 수 있습니다. 바로 value/weight의 최댓값을 찾는 sorting의 과정을 기존 메인 루프를 돌기 전에 진행하는 것입니다. 배열 sorting의 Big-O는 O(nlogn)으로 알려져 있습니다. 그렇기 때문에 sorting의 과정을 기존 메인 루프 앞에 놓으면 O(nlogn) + O(n)이 되어 최종 Big-O는 O(nlogn)이 되는 것이죠. 이를 java 코드로 구현한 것은 아래와 같습니다.</p>

{% highlight java %}
private static double getOptimalValue(int capacity, int[] values, int[] weights) {
    double value = 0;
    double perValue[] = new double[values.length];
    int priority[] = new int[values.length];

    // value/weight을 perValue 배열에 저장합니다.
    // int double간의 casting에 유의하세요.
    for(int i=0; i<perValue.length; i++){
      perValue[i]= (double)values[i]/(double)weights[i];
      priority[i] = i;
    }

    double temp = 0.0;
    int temp2=0;
    // perValue 값이 큰 순으로 sorting 진행
    // 기존 값의 인덱스를 유지하기 위해 priority 배열도 함께 sorting
    for(int i=0; i<perValue.length; i++){
      for(int j=i; j<perValue.length; j++){
        if(perValue[i]<perValue[j]){
          temp = perValue[i];
          perValue[i] = perValue[j];
          perValue[j] = temp;

          temp2 = priority[i];
          priority[i] = priority[j];
          priority[j] = temp2;
        }
      }
    }

    // 우선순위의 숫자가 큰 것이 먼저 실행되도록 설정
    for(int i=0; i<values.length; i++){
        if(weights[priority[i]] <= capacity){
          value += (double)perValue[i]*weights[priority[i]];
          capacity -= weights[priority[i]];
        } else if(weights[priority[i]] > capacity){
          value += (double)(perValue[i]*capacity);
          capacity = 0;
        }
      if(capacity <0) break;
    }
    return value;
}
{% endhighlight %}

>내용 출처 : Coursera, Algorithmic Toolbox by University of California, San Diego & Higher School of Economics(week3)의 강의내용을 개인적으로 정리한 자료입니다.
