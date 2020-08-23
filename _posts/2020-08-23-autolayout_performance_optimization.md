---
layout: post
title: "AutoLayout 성능 최적화 Tips"
date: "2020-08-23 00:53:17 +0900"
excerpt: "성능 관점 AutoLayout을 적절히 사용하는 방법에 대해 살펴봅니다."
categories: iOS, AutoLayout
tags: [iOS, AutoLayout]
image:
  feature: iOS.png
---

## Introduction

이 글에서는 성능 관점에서의 AutoLayout에 대해 살펴보고자 합니다.

> 이 글은 [High Performance AutoLayout](https://developer.apple.com/videos/play/wwdc2018/220)의 많은 내용을 참고하고 있습니다.

## Content

1. [AutoLayout의 Layout 정의 방식](./autolayout_performance_optimization#1-autolayout의-layout-정의-방식)
2. [AutoLayout Engine과 Layout 업데이트](./autolayout_performance_optimization#2-autolayout-engine과-layout-업데이트)
3. [AutoLayout Performance Tips](./autolayout_performance_optimization#3-autolayout-performance-tips)

## 1. AutoLayout의 Layout 정의 방식

AutoLayout이 나오기 이전에 iOS에서 View의 Layout은 Frame 기반(Size와 Position)으로 정의되었습니다. Frame 중심으로 View의 위치를 결정하는 것은 직관적으로 이해가 가능한 것이 가장 큰 장점입니다. 하지만, Frame 기반 Layout 시스템은 해상도가 다른 디바이스에서는 각 해상도별 Size와 Position별로 각 View의 Frame을 설정해주어야 하는 문제가 있습니다. 이 문제는 하나의 Layout 코드로 지원해야 하는 디바이스가 늘어남에 따라 큰 문제가 되었습니다.

AutoLayout은 이러한 기존 Frame 기반 Layout 시스템의 문제를 해결하기 위해 Constraint 기반 Layout 시스템을 사용합니다. Constraint은 단어 그대로 제약을 의미하는데, 이 제약은 View의 관계에 대한 제약을 의미합니다. 그래서 Constraint을 설정한다라는 것은 대부분* 2개의 View 사이에 Layout 관계를 설정(e.g. A View의 bottom과 B View의 top 사이의 간격이 20pt이다.)하여 View가 동적으로 화면에 나타날 수 있도록 합니다. 이러한 Constraint을 통해 나타나는 두 개 View 사이의 관계는 1개의 일차 방정식으로 정의될 수 있습니다. AutoLayout은 설정된 방정식들을 모두 계산하여 각 View의 위치가 적절히 설정될 수 있도록 합니다.

![view_formula_2x](https://user-images.githubusercontent.com/13018877/90341628-04b74280-e03c-11ea-9007-fbab21946612.png)

> 대부분이라는 표현을 사용한 것은 단일 View에도 Constraint를 적용할 수 있기 때문입니다. 예를 들어, View의 width, height을 특정 값으로 고정하는 것이 대표적인 단일 View에다가 Constraint을 적용하는 케이스입니다.

## 2. AutoLayout Engine과 Layout 업데이트

앞서서 AutoLayout 시스템에서는 설정된 여러 개의 일차 방정식을 계산하여 View의 Layout을 구성한다고 언급하였습니다. 그리고 여기서 방정식을 계산을 담당하는 것이 AutoLayout Engine입니다. 이 Engine은 아래와 같이 동작합니다.

1. View는 Constraint을 추가합니다. 이 때 View는 추가된 Constraint을 방정식으로 변환하고 이를 Engine쪽으로 전달합니다.
2. Engine은 전달 받은 방정식을 계산합니다. 여기서 Engine은 우리가 방정식의 해를 구하는 것처럼 각각의 변수를 계산합니다.
3. 계산 결과 값은 View의 Origin, Size 값과 유사한 형태인 Variable(minX, minY, width, height 등)을 View에게 전달됩니다.

![Engine](https://user-images.githubusercontent.com/13018877/90423226-0bef5680-e0f7-11ea-907d-b44d0cc787c8.png)

![스크린샷 2020-08-22 오후 8 29 39](https://user-images.githubusercontent.com/13018877/90955204-87b22000-e4b6-11ea-8010-421389fd17f6.png)

Engine은 각각의 Variable에 값을 설정할 때마다, Variable의 값이 변경되었다는 것을 View에게 알립니다. View는 Variable 변경 이벤트를 받을 때마다, `setNeedsLayout()`을 호출합니다.

![notify](https://user-images.githubusercontent.com/13018877/90424852-c1bba480-e0f9-11ea-9f00-cf7b9484db6f.png)

`setNeedsLayout()`이 호출되면 해당 View의 `layoutSubViews()`가 호출됩니다. 여기서 View는 Engine의 데이터를 Frame으로 복사하고, 자신과 자신의 SubView의 Layout을 결정하게 됩니다.

![스크린샷 2020-08-22 오후 8 49 44](https://user-images.githubusercontent.com/13018877/90955520-05772b00-e4b9-11ea-9a2e-f1c7cdbaeae0.png)

## 3. AutoLayout Performance Tips

### 1. 관계가 없는 View 사이에 Constraint 설정하지 않기

Engine은 서로 관계가 없는(dependency가 없음) View의 Constraint을 별개로 인지합니다. 그래서 View끼리 Constraint이 걸려 있지 않을 때, Constraint 계산 비용은 linear하게 증가합니다. 바꿔 말하면, 여러 개의 View에 독립적으로 걸려 있는 Constraint을 하나의 View로 묶어서 처리하는 방식은 Constraint 계산 비용을 증가시킬 수 있습니다. 그러므로, View의 Constraint은 필요한 경우에만 서로 관련되도록 처리하는 것이 성능적으로 좀 더 좋습니다.

![스크린샷 2020-08-22 오후 11 25 03](https://user-images.githubusercontent.com/13018877/90958329-ba681280-e4ce-11ea-88e9-d1ecf276c7f8.png)

### 2. Constraint을 자연스럽게 사용하기

- 억지로 Constraint을 적게 사용하지 않기

Constraint은 직관적으로 필요한 만큼 추가되는 것이 좋습니다. 억지로 Constraint을 적게 설정하려고 한다면 오히려 Constraint 계산 비용이 커지는 경우가 발생할 수 있습니다. 예를 들어 Constraint 최적화를 위해 Constraint를 추가/제거하는 작업은 계산 비용을 낮춘다고 생각할 수 있지만 오히려 비용을 크게 만드는 경우가 많습니다. 이런 경우에는 오히려 Constraint을 여러 개 두는 것이 나을 수도 있습니다.

- 두 개의 Layouts을 하나의 View로 표현하기 위해, Constraint을 복잡하게 설정하지 않기

때때로 두개의 Layout을 하나의 View로 표현하기 위해 복잡한 Constraint을 설정하는 경우가 발생할 수 있습니다. 추가되는 Constraint이 많으면 많아질수록 Constraint을 통해 나타나는 Layout을 직관적으로 확인하기 어렵습니다. 이런 경우에는 직관적으로 View가 Constraint을 통해 명확히 표현될 수 있는가를 중점에 두고, Constraint을 설정하는 것이 좋습니다.(별도의 View로 나누거나, 새로운 SubView를 추가하여 Constraint 복잡도를 줄이거나 등의 방법을 사용)

![스크린샷 2020-08-23 오전 3 27 23](https://user-images.githubusercontent.com/13018877/90963169-95849700-e4f0-11ea-9ce6-ce141655464f.png)

![스크린샷 2020-08-23 오전 3 26 05](https://user-images.githubusercontent.com/13018877/90963171-97e6f100-e4f0-11ea-88a7-b6d321841cc8.png)

### 3. Priority 설정은 일반적으로 성능에 큰 영향을 미치지 않는다.

AutoLayout Engine이 View로부터 계산된 Variable을 제공해줄 것을 요청 받을 때, Engine은 우선적으로 전달 받은 Constraint에 에러가 있는지 여부를 확인합니다. 그리고 이 때 에러가 있다면, Engine은 View에게 에러를 최소화(minimize error)해줄 것을 요청합니다.* 이 때, 에러를 최소화하는 과정에서 [Simplex Algorithm](https://en.wikipedia.org/wiki/Simplex_algorithm)를 사용하여 에러를 최소화하는 최적해(Variable)를 도출합니다. 이러한 Variable 도출 과정은 일반적으로 비용이 크지 않기 때문에 AutoLayout의 성능에 있어서 큰 영향을 미치지 않습니다.

![스크린샷 2020-08-23 오후 6 50 13](https://user-images.githubusercontent.com/13018877/90975685-809c1800-e571-11ea-92a7-f4f26ac1febf.png)

> 애플 공식 문서 및 WWDC에서 Engine이 어떤 경우에 에러 최소화 메시지를 View에게 요청하는지 명확히 언급하고 있지 않습니다. 다만, WWDC에서 Priority를 언급하는 과정에서 에러 최소화에 대한 얘기를 꺼낸 것으로 미루어 볼 때, Engine은 Priority가 없을 때에는 Constraint이 만족될 수 없는 경우에 대해서 View에 에러 최소화 메시지를 요청하는 것을 추측해볼 수 있습니다.

### 4. Constraint Churn 없애기

Constraint Churn이라는 것은 시각적으로는 동일한 Layout 결과물을 내부적으로 복잡한 Constraint 설정, 불필요한 반복적 Constraint 추가/제거 작업으로 뒤섞는 것을 의미합니다. 즉, 실제 View의 레이아웃 변경은 없지만, Engine이 더 많은 일을 하게 만드는 경우 Constraint Churn이 있다고 말합니다. Constraint Churn이 많아질 경우 AutoLayout의 성능에 악영향을 끼칠 수 있습니다. Constraint Churn은 다음과 같은 작업을 수행할 경우 주로 발생하게 됩니다.

- 모든 Constraint 제거
- 변경이 필요하지 않은 Constraint 변경
- 반복적 Constraint 추가/제거

#### Constraint Churn과 Render Loop

Constraint Churn을 발생시키는 작업을 의도치 않게 수행할 수 있는 곳이 `updateConstraints()`와 `layoutSubViews()`입니다. iOS에서 View를 화면에 그릴 때, Render Loop를 거칩니다. 이 Render Loop는 아래와 같은 흐름으로 진행이 됩니다.

<img width="1338" alt="스크린샷 2020-08-06 오후 5 40 15" src="https://user-images.githubusercontent.com/13018877/89510719-e7989d80-d80b-11ea-8e44-7d5c26d448dd.png">

1. `updateConstraints()` 호출 - View Hierarchy의 leaf부터 Window 방향으로 호출
2. `layoutSubViews()` 호출 - Window부터 SubViews 방향으로 호출
3. `draw(rect:)` 호출 - Window부터 SubViews 방향으로 호출

Render Loop는 View의 bounds가 변경되거나, 회전 이벤트가 발생하거나, `setNeedsLayout()`, `layoutIfNeeded()`가 호출될 때마다 수행됩니다. 바꿔 말하면, Render Loop의 메소드들은 매우 많이 호출됩니다.(특히 ScrollView의 스크롤 수행시) 그렇기 때문에 `updateConstraints()`을 오버라이딩하여 Constraint 업데이트를 수행할 때, 별도 예외처리 없이 Constraint 추가/제거 작업을 반복적으로 수행할 경우 Layout 성능에 이슈가 발생할 수 있습니다. 정리하면, Render Loop 사이클 안에서 어떤 처리가 필요할 경우 아래 사항을 우선적으로 고려해보면 좋습니다.

1. Constraint 업데이트는 최대한 필요한 경우에만(최초 설정, 이벤트 발생시 업데이트 필요한 경우 등)에만 수행되는 것이 좋습니다.
2. `updateConstraints()`, `layoutSubViews()`은 오버라이딩하지 않으면 Layout이 제대로 잡히지 않을 경우에만 사용하는 것이 좋습니다.

![스크린샷 2020-08-23 오후 8 31 45](https://user-images.githubusercontent.com/13018877/90977348-afb98600-e57f-11ea-93e8-05a81738dc1a.png)

# 참고자료

- [AutoLayout - Understanding AutoLayout](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/AutolayoutPG/index.html#//apple_ref/doc/uid/TP40010853-CH7-SW1)
- [AutoLayout - Anatomy of a Constraint](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/AutolayoutPG/AnatomyofaConstraint.html#//apple_ref/doc/uid/TP40010853-CH9-SW1)
- [High Performance AutoLayout](https://developer.apple.com/videos/play/wwdc2018/220)