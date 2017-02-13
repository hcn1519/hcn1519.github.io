---
layout: post
comments: true
title:  "Java Scanner의 에러 체크하기(Validation)"
excerpt: "Java에서 Scanner Class의 에러를 체크하는 방법입니다."
categories: Java Validation Language
date:   2016-10-04 00:30:00
tags: [Java, Scanner, Validation, Language]
image:
  feature: errorCheck.PNG
---

<p>&nbsp;자바에서는 사용자로부터 콘솔창에서 입력을 받을 때, Scanner라는 클래스를 사용합니다. 이 포스팅에서는 Scanner를 사용할 때 잘못된 입력(예를 들어, 정수형 3을 받아야 하는데 "aaa"같은 String이 들어오는 경우)이 들어오는 것을 방지하는 것에 대해 알아봅니다.</p>

<h4>1. 단일입력 처리</h4>

<p>&nbsp;먼저 Scanner로 단 1개의 <code>0또는 자연수</code>만 받는 예제입니다. 실수도 안 되고, 음의 정수도 안 되고, 문자열도 안 받습니다. 띄어쓰기로 여러 개를 넣어도 받지 않습니다.</p>

{% highlight java %}
class ScannerErrCheck{ //scanner로 입력 받는 데이터타입 예외처리용 class입니다.
  int scNum;
  void errorCheckNum(Scanner scNum){ // 0또는 자연수 체크하는 메소드

    while(true){

      if(scNum.hasNextInt()){ // 정수를 받는지 체크
        this.scNum = scNum.nextInt();
        String[] lengthOfInput = scNum.nextLine().split(" ");
        this.coef = new float[lengthOfInput.length];
        if(lengthOfInput.length != 1){ // 1개만 받는지 체크
          System.err.println("1개의 숫자만 입력하세요.");
          scNum.reset();
          continue;
        }
        if(this.scNum >= 0) // 0 이상 자연수라면 차수 결정
        break;
        else { // 음의 정수이면, 재입력 요구
          System.err.println("0 또는 자연수를 입력하세요.");
          scNum.reset();
          continue;
        }
        } else { // 실수이면, 재입력 요구
          System.err.println("정수를 입력하세요.");				
          scNum.next();
        }
      }
    }
  }
  public class Main {
    public static void main(String[] args){
      ScannerErrCheck err1 = new ScannerErrCheck(); // scanner가 1개의 자연수만 받도록 하는 class
      Scanner scNum = new Scanner(System.in);
      System.out.println("1개의 자연수를 입력하세요 >>");
      err1.errorCheckNum(scNum);
    }
  }
{% endhighlight %}

<h4>2. 복수개 입력 실수인지 체크</h4>

<p>&nbsp;다음으로는 Scanner로 띄어쓰기를 통해 여러개의 data를 받을 때 실수형인지 체크하는 예외 처리입니다.</p>

{% highlight java %}
class ScannerErrCheck{ //scanner로 입력 받는 데이터타입 예외처리용 class입니다.
  float[] scArr = new float[5];

  void errorCheckArr(Scanner scArr){

    int counter =0;
    while(true){ 	// 입력 받은 수를 scArr[i]에 저장하는 작업 진행
      for(int i=0; i< this.scArr.length ; i++){  
        if (scArr.hasNextFloat()) {	// 받은 수가 실수(혹은 정수)일 경우 입력,
          this.scArr[i] = scArr.nextFloat();  
          counter++;
        }
        else { // 실수가 아니라면 입력을 리셋하고, 새로운 입력 요구
          System.err.println("모든 계수는 실수형이어야 합니다.");
          scArr.reset();
          scArr.next();
        }
      }
      if(counter == this.coef.length)	// counter 갯수가 배열의 길이와 같아지면 루프 종료
      break;
      else {	// 1개의 입력이라도 실수형이 아니라면, 전부 새로운 입력 요구
        counter = 0;
        scArr.reset();
      }
    }

  }
}
public class Main {
  public static void main(String[] args){
    ScannerErrCheck err1 = new ScannerErrCheck();
    Scanner scArr = new Scanner(System.in);
    System.out.println("여러개의 실수를 입력하세요. >>");
    err1.errorCheckArr(scArr); // 에러 체크 메소드
  }
}
{% endhighlight %}

<p>&nbsp;적절히 위의 방식을 섞어서 쓰면 이런 저런 곳에서 활용할 수 있을 것 같네요.</p>

<h5>더 볼만한 추가 자료</h5>

<ul>
  <li><a href="http://stackoverflow.com/questions/3059333/validating-input-using-java-util-scanner" target="_blank">Stackoverflow validation 관련 포스팅</a></li>
</ul>
