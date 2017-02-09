---
layout: post
comments: true
title:  "Stress Testing에 대하여"
excerpt: "알고리즘을 테스트하고, 고치고, 디버깅하는데 쓰이는 stress testing에 대해서 알아봅니다."
categories: java algorithm stressTesting coursera
date:   2016-12-21 00:30:00
tags: [Java, Algorithm StressTesting, Coursera]
---

<p>&nbsp;문제를 해결하는 알고리즘이 실제로 모든 경우에 대해 귀납적으로(모든 경우에 맞는지 확인하는 방법을 통해) 맞는지 확인하는 방법으로 <code>Stress Testing</code>이라는 것이 있습니다. 테스트의 컨셉은 간단합니다. 무한루프를 돌려서 조건에 맞는 랜덤한 input값을 주고, 모든 값에 대해 올바른 답을 출력하는지 확인하는 것입니다. 예시를 통해서 알아 보겠습니다.</p>

<p>&nbsp;아래 예제는 주어진 숫자들 중 두 개를 선택하여, 가장 큰 값을 출력하는 코드입니다. 작동하는 순서는 다음과 같습니다.</p>
<ol>
<li>먼저 콘솔창에서 배열의 크기를 입력합니다.</li>
<li>다음으로 배열에 들어갈 숫자들을 입력합니다.</li>
<li>입력된 숫자들 중 가장 큰 두 개를 곱해서 최댓값을 출력합니다.</li>
</ol>
<img src="https//dl.dropbox.com/s/c8ph0eung4v4e9q/test.png">

{% highlight java %}
// MaxPairwiseProduct.java
import java.util.*;
import java.io.*;

public class MaxPairwiseProduct {
    static long getMaxPairwiseProduct(ArrayList<Long> numbers) {
        long result = 0;
        long n = numbers.size();
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (numbers.get(i) * numbers.get(j) > result) {
                    result = numbers.get(i) * numbers.get(j);
                }
            }
        }
        return result;
    }
    static long MaxPairwiseProductFast(ArrayList<Long> numbers){
      int n = numbers.size();

      int maxIndex1 = -1;
      for(int i=0; i< n; i++)
        if((maxIndex1 == -1) || numbers.get(i) > numbers.get(maxIndex1) )
          maxIndex1 = i;

      int maxIndex2 = -1;
      for(int i=0; i< n; i++)
        if((i != maxIndex1) && (maxIndex2 == -1 || numbers.get(i) > numbers.get(maxIndex2)))
          maxIndex2 = i;

      // System.out.println("index : " + maxIndex1 + " " + maxIndex2);
      return (long)(numbers.get(maxIndex1) * numbers.get(maxIndex2));
    }

    public static void main(String[] args) {
        FastScanner scanner = new FastScanner(System.in);
        int n = scanner.nextInt();
        ArrayList<Long> numbers = new ArrayList<Long>();
        for (int i = 0; i < n; i++) {
            numbers.add(scanner.nextLong());
        }
        System.out.println(getMaxPairwiseProduct(numbers));
        System.out.println(MaxPairwiseProductFast(numbers));
    }

    static class FastScanner {
        BufferedReader br;
        StringTokenizer st;

        FastScanner(InputStream stream) {
            try {
                br = new BufferedReader(new InputStreamReader(stream));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        String next() {
            while (st == null || !st.hasMoreTokens()) {
                try {
                    st = new StringTokenizer(br.readLine());
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return st.nextToken();
        }
        long nextLong() {
          return Long.parseLong(next());
        }
        int nextInt() {
            return Integer.parseInt(next());
        }
    }

}
{% endhighlight %}

<p>&nbsp;위의 코드에서 main을 보시면 2가지 메소드(<code>getMaxPairwiseProduct</code>와 <code>MaxPairwiseProductFast</code>)가 있습니다. 먼저 getMaxPairwiseProduct은 배열에서 두 개의 elements를 뽑아서 최댓값을 업데이트하는 형식의 메소드입니다. 다음으로 MaxPairwiseProductFast는 배열을 2번 도는데, 1번 째에 최댓값을 찾고, 2번 째에 처음에 뽑은 값을 제외한 것들 중의 최댓값을 뽑아서 결과로 리턴하는 메소드입니다. 동일한 일을 하는 메소드이지만, 속도 상으로 보면 getMaxPairwiseProduct는 O(n^2)이고, MaxPairwiseProductFast는 O(n)이기 때문에 MaxPairwiseProductFast가 훨씬 빠릅니다.</p>
<p>&nbsp;자, 그런데 실제로 두 메소드가 같은 일을 하는지는 확인해볼 필요가 있습니다. 값 몇 개 넣어보고 확인하는 것이 아니라, 주어진 조건 내에서 항상 작동하는지 여부를 테스트해볼 필요가 있는 것이죠. 여기서 사용되는 것이 <code>Stress Testing</code>입니다.(여기서는 조건을 배열 크기는 2<=n<=100이고, 배열 안에 들어갈 수 있는 숫자의 범위는 0<=n<=100,000로 설정하겠습니다.)</p>

{% highlight java %}
// Stress testing을 위해 변경한 main
public static void main(String[] args) {
    while(true){
      int k = rand.nextInt(100)+2; // 배열 크기 랜덤값 입력
      System.out.println(k);

      ArrayList<Long> a = new ArrayList<>();

      long x = 0L;
      long y = 100000L;
      Random r = new Random();
      for(int i=0; i< k; i++)
        a.add(x+((long)(r.nextDouble()*(y-x)))); //랜덤한 값을 배열에 집어 넣기

      for(int i=0; i<a.size(); i++)
        System.out.print(a.get(i)+ " ");
      System.out.println();

      long res1 = getMaxPairwiseProduct(a);
      long res2 = MaxPairwiseProductFast(a);

      if(res1 != res2){ //두 메소드에서 나온 값이 맞는지 확인
        System.out.println("Wrong Answer : " + res1 + ", "+ res2);
        break;
      } else
        System.out.println("OK");

    }
}
{% endhighlight %}

<p>&nbsp;위의 while문은 무한루프로서 두 메소드에서 나온 값이 실제로 같은 값인지 체크합니다. 둘이 다른 값이라면, Wrong Answer를 뿜습니다. 둘이 실제로 같은 값이라면, 계속 OK를 찍으면서 무한루프를 돌겠죠? 확인해보면 아래와 같습니다.</p>

<img src="https//dl.dropbox.com/s/jnf7qflwlte5r2u/test2.png">

<p>&nbsp;캡처상으로는 보여드리는데 한계가 있지만 무한루프를 돌고 있습니다. 주어진 값 내에서는 두 메소드가 동일한 작업을 하는 것을 확인할 수 있습니다.</p>

>내용 출처 : Coursera, Algorithmic Toolbox by University of California, San Diego & Higher School of Economics(week1)의 강의내용을 개인적으로 정리한 자료입니다.
