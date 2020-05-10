---
layout: post
title: "Expression과 Statement"
date: "2020-05-09 00:53:17 +0900"
excerpt: "Expression과 Statement에 대해 정리하였습니다."
categories: Expression, Statement, Language, C, Terminology
tags: [Expression, Statement, Language, C, Terminology]
---

## 목차

1. [Introduction](./expression_statement#introduction)
1. [Expression](./expression_statement#expression)
    1. [Evaluation](./expression_statement#evaluation)
    1. [Side Effect](./expression_statement#side-effect)
    1. [Undefined Behavior](./expression_statement#undefined-behavior)
1. [Statement](./expression_statement#statement)

## Introduction

컴파일러는 컴파일 과정에서 문제가 생길 경우 유용한 에러 혹은 경고 문구를 제공합니다. 그런데 컴파일러에서 발생하는 에러들을 살펴보면 `expression`과 `statement`라는 문구가 꽤 많이 등장하는 것을 알 수 있습니다.

<img width="815" alt="스크린샷 2020-05-10 오후 7 57 51" src="https://user-images.githubusercontent.com/13018877/81497316-9a825980-92f8-11ea-9956-6004c50043f1.png">

얼핏 보면 둘의 차이가 커보이지 않지만, 컴파일러는 어떤 위치에 `expression`과 `statement`이 오는지를 명확하게 구분합니다. 또한 대부분의 언어 Reference에서도 `expression`과 `statement`을 구분합니다. 예를 들어서, if 조건문에 대해서 항상 if `statement`이라고 부르지 if `expression`이라고 하지 않습니다. 이번 글에서는 여기서 나오는 `expression`, `statement`가 무엇인지에 대해 살펴보겠습니다.

## Expression

`expression`에 대한 정의를 몇 가지 자료에서 찾아 보면 다음과 같이 서술되어 있습니다.

<div class="message">
    expression - formulas that shows how to compute a value.
</div>

* [C Programming: A Modern Approach, KNKing](http://knking.com/books/c2/index.html)

<div class="message">
    An expression in a programming language is a syntactic entity that may be evaluated to determine its value. It is a combination of one or more constants, variables, functions, and operators that the programming language interprets and computes to produce another value.
</div>

* [Expression (computer science) - Wikipedia](https://en.wikipedia.org/wiki/Expression_(computer_science))

<div class="message">
    An expression is a sequence of operators and operands that specifies computation of a value, or that designates an object or a function, or that generates side effects, or that performs a combination thereof.
</div>

* [ISO/IEC 9899:2018 - 6.5 Expressions](https://www.iso.org/standard/74528.html)

위의 정의들을 종합해보면 다음과 같은 것들을 알 수 있습니다.

* `expression`은 value에 대한 표현이다.
* `expression`은 하나의 구문을 의미한다.
* `expression`은 evaluate 될 수 있다.
* `expression`이 evaluate 되면 하나의 value가 도출된다.
* `expression`은 side effect를 만든다.

위 정의에서 가장 중요한 것은 `expression`이 항상 **단일한 value** 가 된다는 점입니다.(여기서 말하는 value는 ([명확한 정의를 확인하기 쉽지 않지만](https://stackoverflow.com/questions/3300726/what-is-a-value-in-the-context-of-programming)) 메모리에 저장되어 있는 정보(객체)를 의미합니다.) 즉, `expression`은 언제나 그 결과가 하나의 저장된 값으로 귀결되어, 해당 `expression`이 수행되는 시점에 언제나 값이 존재해야 합니다.

가장 대표적인 `expression`의 예시로는 수식이 있습니다. `2 + 3`과 같은 수식은 결과 값(value)이 `5`가 됩니다. 위 수식이 아니더라도 모든 수식은 하나의 단일한 값으로 귀결됩니다. 그래서 수식은 모두 `expression`이라고 할 수 있습니다. 또한 `a + 3`와 같은 변수를 포함하는 수식도 `expression`입니다. `a + 3`은 `a`라는 변수를 포함하지만, 해당 수식이 실제로 수행되는 시점에서 `a`의 값은 언제나 하나입니다. 그렇기 때문에 `a + 3`도 항상 하나의 값을 가진다고 얘기할 수 있습니다.

* Void Return Function도 `expression`입니다.

C에서는 `void`를 리턴 타입으로 명시한 경우 function이 `void`를 리턴합니다.

```c
void innerFunction() {
    printf("innerFunction\n");
    return;
}

void outerFunction() {
    printf("outerFunction\n");
    return innerFunction();
}

outerFunction();
// outerFunction
// innerFunction
```

function의 리턴 값이 존재하지 않는다는 말은 함수 호출부에 제공되는 리턴 값이 존재하지 않는다는 말을 의미하는 것이지, 실제 함수의 리턴 값이 없다는 것을 의미하는 것은 아닙니다. 리턴 값이 없는 function의 경우에도 **리턴 값이 없음**을 리턴합니다. 정리하면, 리턴 값이 없는 함수도 리턴하는 값이 존재하고, function은 리턴 타입과 관계 없이 `expression`이라고 할 수 있습니다.

> C에서는 void를 제한적인 위치에서 사용되는 하나의 데이터 타입(`incomplete type`)으로 정의하고 있습니다.

### Evaluation

위의 설명에서 `expression`을 evalute한다는 표현이 나옵니다. evalutation은 한국어로 번역하면 평가라는 의미를 가지고 있습니다. 그래서 번역서나 일부 블로그에서는  `expression`을 평가한다라는 표현을 쓰기도 합니다. 하지만 평가라는 단어는 등급을 매긴다라는 의미가 강하기 때문에 `expression`을 평가한다는 표현은 어감이 어색합니다. `expression can be evaluated its value`와 같은 표현에서 evalute의 뜻은 **expression이 나타내는 value를 도출한다**는 의미가 좀 더 적절합니다.(이후의 서술에서도 이 표현을 사용합니다)

Evaluation도 수식에 대한 예시를 통해서 이해할 수 있습니다. 앞서서 `2 + 3` 수식이 `5`라는 value로 귀결된다라고 하였습니다. 여기서 `2 + 3`이 `5`라는 value인 것을 확인하는 것을 evaluation이라고 합니다.

> Note: 수학에서 `expression`은 수식을 의미하고, evaluation은 대입을 의미합니다.

* JavaScript Evaluation

JavaScript와 같은 언어에서는 [eval()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval)이라는 함수가 공식적으로 지원됩니다. `eval()` 함수는 문자열로 표현되는 `expression`의 value를 리턴하는 함수입니다.

```javascript
eval('2 + 2');  // returns 4
```

iOS에서 `WKWebView`를 통한 JS interface 호출시 사용하는 [evaluateJavaScript(_:completionHandler:)](https://developer.apple.com/documentation/webkit/wkwebview/1415017-evaluatejavascript) API도 이와 동일한 역할을 하는 것을 확인할 수 있습니다.

* NSExpression

Foundation에서도 JavaScript의 eval()과 유사한 `NSExpression`이라는 API를 제공합니다. 이는 ObjectiveC, Swift 문자열에 대한 evaluation 기능을 제공합니다.

```swift
let sumExpression = NSExpression(format: "1 + 2 + 3")
let sumResult = sumExpression.expressionValue(with: nil, context: nil) as? Int // 6

let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
let avgExpression = NSExpression(forFunction: "average:", arguments: [NSExpression(forConstantValue: numbers)])
let avgResult = avgExpression.expressionValue(with: nil, context: nil) as? Double // 5.5
```

### Side Effect

함수 내부의 변화가 함수 외부의 상태에 영향을 끼칠 때, 일반적으로 함수가 Side Effect를 가진다라고 합니다. 이러한 Side Effect 개념은 `expression`에서도 동일하게 적용됩니다. `expression`을 evaluate하는 과정에서 `expression` 외부의 환경에 영향을 끼칠 때 해당 `expression`은 Side Effect가 있다고 말합니다.

C에서 assignment operator(`=`)는 Side Effect를 일으키는 대표적인 `expression`입니다. assignment operator는 할당되는 값을 리턴하여 다음과 같은 표현이 가능합니다.

```c
int a = 0;
while (a = 3) { } // a = 3이라는 expression을 evaluate할 때, value가 3이 됩니다.
```

assignment operator는 `expression` 외부에 값을 설정하는 동작을 수행합니다. 위에서 `a = 3`이라는 `expression`에 대한 evaluation이 진행될 때, a라는 변수의 값이 0에서 3으로 변경이 발생하므로 `expression` 외부에 영향을 끼쳤고 이는 Side Effect가 발생했다고 말합니다.

> Note: assignment operator의 경우 C에서는 `expression`으로 취급하지만, `expression`으로 취급하지 않는 언어도 많습니다. 예를 들어, Swift에서는 assignment operator가 `expression`으로 취급되지 않고, statement로 취급되어 assignment operator가 value를 리턴하지 않습니다.

KNK에서는 `expression`의 연산자의 값 계산 과정에서 값을 계산하는 것 이외의 동작(i.e. 피연산자를 조작하는 동작)이 수행될 때, Side Effect가 있다고 말하기도 합니다.

<div class="message">
We don't normally expect operators to modify their operands, since operators in mathmatics don't. Writing i+j doesn't modify either i or j; It simply computes the result of adding i and j. Most C operators don't modify their operands, but some do. We say that these operators have side effects, since they do more than just compute a value.
</div>

* 출처: [C Programming: A Modern Approach, KNKing - Ch 4.2 Assignment Operators](http://knking.com/books/c2/index.html)

### Undefined Behavior

<div class="message">
    If a side effect on a scalar object is unsequenced relative to either a different side effect on the same scalar object or a value computation using the value of the same scalar object, the behavior is undefined.
</div>

C에서 expression의 evaluation 과정에서 발생하는 side effect간의 우선순위를 결정하지 못 하여(컴파일러마다 다를 때), 하나의 value가 도출될 수 없을 때, undefined behavior가 발생하였다고 말합니다. 아래의 예시와 같은 경우에 undefined behavior가 발생하였다고 할 수 있습니다.

```c
int a, b, c;
a = b = c = 0;

// Warning: Unsequenced modification and access to 'a'
c = (b = a + 2) - (a = 1);
```

위 코드에서 `c = (b = a + 2) - (a = 1)` 은 Undefined Behavior가 발생한 케이스입니다. 여기서 우선 순위가 결정되지 못 한 것은 `(b = a + 2)`와 `(a = 1)`입니다. 두 `expression`은 evaluation의 우선순위가 C standard 기준으로 동일합니다. 즉, 컴파일러에 따라서 `(b = a + 2)`이 먼저 evaluation 될 수도 있고, `(a = 1)`이 먼저 evaluation이 될 수 있습니다. 그리고 각각의 `expression`은 `a` 또는 `b`의 값을 바꾸는 Side Effect를 가지고 있습니다. 이 Side Effect의 발생 우선 순위가 명확하지 않기 때문에 이와 같은 경우를 Undefined Behavior가 발생했다고 말합니다. Undefined Behavior가 발생했을 때에는 `expression`을 나누는 것을 통해 우선순위를 명확히 해주면 문제가 해결됩니다.

## Statement

`statement`에 대한 정의도 몇 가지 자료에서 찾아 보면 다음과 같이 서술되어 있습니다.

<div class="message">
    A statement is a command to be executed when the program runs.
</div>

* [C Programming: A Modern Approach, KNKing](http://knking.com/books/c2/index.html)

<div class="message">
    In computer programming, a statement is a syntactic unit of an imperative programming language that expresses some action to be carried out.
</div>

* [Statement (computer science) - Wikipedia](https://en.wikipedia.org/wiki/Statement_(computer_science))

<div class="message">
    A statement specifies an action to be performed. Except as indicated, statements are executed in sequence.
</div>

* [ISO/IEC 9899:2018 - 6.8 Statements and Blocks](https://www.iso.org/standard/74528.html)

위의 정의를 종합적으로 보면, `statement`는 아래와 같은 특성을 가지는 것을 확인할 수 있습니다.

* `statement`는 하나의 구문(syntactic unit)이다.
* `statement`는 수행되는 명령을 명시한다.
* `statement`는 런타임에서 명시된 명령을 실행(execute)한다.

여기서 주목할 점은 `statement`가 명시된 명령을 수행한다는 점입니다. 여기서 명령은 사용자가 프로그램에 대해 내리는 명령을 의미하는 것으로, 일반적으로 언어별로 미리 정의된 keyword를 통해서 명령이 동작합니다. 예를 들어서 C에서 조건문을 처리하는 if `statment`의 경우 아래와 같은 문법으로 명령을 수행합니다.

```c
if (expression)
    statement
else
    statement
```

예시로 든 if `statement와` 같은 조건문 처리뿐만 아니라(`Selection statement`), 반복문도 `while`, `for` 등과 같은 keyword를 사용하고 그 문법에 맞춰 명령을 수행하여 `statement`에 해당(`Iteration statement`)됩니다.

또한, C에서 모든 expression은 마지막에 세미콜론(`;`)을 붙이는 것을 통해 `statement`가 될 수 있습니다. 이렇게 세미콜론이 붙은 `expression`은 `expression statement`라고 합니다. C 컴파일러는 `expression statement`의 경우에 expression에 대한 evaluation을 수행하여, value를 도출하는 명령을 수행합니다. 이 때, 일반적으로 side effect가 발생하게 되는데, 그렇지 않은 경우 C 컴파일러에서는 `Expression result unused`와 같은 warning 메시지를 보여줍니다.

> Note: Side Effect가 발생했다는 것을 어떤 문제가 발생했다고 이해하면 안 됩니다. Side Effect가 일어났다는 것은 외부 State에 대한 변화가 발생한 것으로 이해해야 합니다.

# 참고자료

* [C Programming: A Modern Approach, KNKing](http://knking.com/books/c2/index.html)
* [Expression (computer science) - Wikipedia](https://en.wikipedia.org/wiki/Expression_(computer_science))
* [Statement (computer science) - Wikipedia](https://en.wikipedia.org/wiki/Statement_(computer_science))
* [ISO/IEC 9899:2018](https://www.iso.org/standard/74528.html)