---
layout: post
title: "Optimizing AutoLayout Performance"
date: "2020-08-23 00:53:17 +0900"
excerpt: "Exploring how to efficiently use AutoLayout from a performance perspective."
categories: iOS, WWDC, AutoLayout, UIKit, UIView
tags: [iOS, WWDC, AutoLayout, UIKit, UIView]
image:
  feature: iOS.png
---

## Introduction

In this post, we will explore how to use AutoLayout efficiently from a performance perspective.

> This post references a lot of content from [High Performance AutoLayout](https://developer.apple.com/videos/play/wwdc2018/220).

## Content

1. [Layout Definition in AutoLayout](./autolayout_performance_optimization#1-layout-definition-in-autolayout)
2. [AutoLayout Engine and Layout Updates](./autolayout_performance_optimization#2-autolayout-engine-and-layout-updates)
3. [AutoLayout Performance Tips](./autolayout_performance_optimization#3-autolayout-performance-tips)

## 1. Layout Definition in AutoLayout

Before AutoLayout, iOS defined the layout of views in a frame-based manner (size and position). Defining view positions primarily based on frames was intuitive and easy to understand. However, frame-based layouts posed a problem when adapting to devices with different screen resolutions. As the number of devices to support increased, this became a significant issue.

AutoLayout addresses the limitations of the frame-based layout system by using a constraint-based layout system. Constraints are, as the name suggests, restrictions that define the relationship between views. When using AutoLayout, various constraints are set up between views. For example, defining that the top of view A is 20 points below the bottom of view B becomes one constraint.

The significant advantage of defining layouts with constraints is that you don't need to set static values for view sizes or positions. In AutoLayout, the size and position of views are dynamically calculated based on the defined constraints and adapt to the environment. This dynamic layout determination effectively resolves many problems caused by device fragmentation. For instance, when implementing a layout where a screen should leave a certain margin and fill the rest, you no longer need to specify view sizes for each resolution. You only need to set the margin values as constraints, and AutoLayout handles the rest.*

> While AutoResizingMask supports similar functionality, it is generally applicable only in simpler UIs.

## 2. AutoLayout Engine and Layout Updates

### AutoLayout and Equations

The relationship between two views expressed through constraints can be defined by a single linear equation. For example, when setting a gap of 8 points between the trailing edge of RedView and the leading edge of BlueView, the following equation is established:

![some2](https://user-images.githubusercontent.com/13018877/91072672-d0173c80-e674-11ea-8641-65e9ac89e3c8.png)

AutoLayout's task is to find the solutions to these linear equations. When all solutions either have exactly one answer or a single viable answer*, each view's position is determined.

> Note: AutoLayout can create situations where multiple solutions are possible by using settings like Priority or Inequality. In such cases, AutoLayout performs Error Minimization to find the optimal solution and uses that value.

### AutoLayout Engine

The AutoLayout Engine is the core module that calculates the set of equations derived from the constraints. The engine operates as follows:

1. Views add constraints. When constraints are added, views convert them into equations and send them to the engine.
2. The engine calculates the received equations. It calculates each variable as if it were solving equations.
3. The calculated results, in the form of variables (minX, minY, width, height, etc.), are sent back to the views.

![Engine](https://user-images.githubusercontent.com/13018877/90423226-0bef5680-e0f7-11ea-907d-b44d0cc787c8.png)

![스크린샷 2020-08-22 오후 8 29 39](https://user-images.githubusercontent.com/13018877/90955204-87b22000-e4b6-11ea-8010-421389fd17f6.png)

Every time a variable is set in the AutoLayout Engine, it notifies the views that the variable has changed. Views, upon receiving this notification, call `setNeedsLayout()`.

![notify](https://user-images.githubusercontent.com/13018877/90424852-c1bba480-e0f9-11ea-9f00-cf7b9484db6f.png)

When `setNeedsLayout()` is called, the view's `layoutSubviews()` is triggered. In this method, the view copies the engine's data into frames and determines the layout of itself and its subviews.

![스크린샷 2020-08-22 오후 8 49 44](https://user-images.githubusercontent.com/13018877/90955520-05772b00-e4b9-11ea-9a2e-f1c7cdbaeae0.png)

## 3. AutoLayout Performance Tips

### 1. Avoid Setting Constraints Between Unrelated Views

The AutoLayout Engine treats constraints between views that are unrelated (have no dependencies) as separate entities. Consequently, when constraints are not set between views, the cost of constraint calculation increases linearly. In other words, consolidating constraints that are independently attached to multiple views into a single view can increase the cost of constraint calculation. Therefore, it's better for view constraints to relate to each other only when necessary for performance.

![스크린샷 2020-08-22 오후 11 25 03](https://user-images.githubusercontent.com/13018877/90958329-ba681280-e4ce-11ea-88e9-d1ecf276c7f8.png)

### 2. Use Constraints Naturally

- Don't force constraints to be minimal

It's recommended to add constraints as needed. Trying to minimize constraints forcefully may lead to increased constraint calculation costs. For example, you may consider repeatedly adding/removing constraints for constraint optimization, but this often increases costs. In such cases, it may be more efficient to have multiple constraints rather than trying to minimize them.

- Avoid complex constraints to represent two layouts as a single view

Sometimes, to represent two layouts as a single view, you may create complex constraints. The more constraints you add, the harder it becomes to intuitively understand the layout defined by constraints. In such cases, it's better to prioritize creating constraints that make it clear how the view is represented through constraints (using separate views or adding new subviews to reduce constraint complexity).

![스크린샷 2020-08-23 오전 3 27 23](https://user-images.githubusercontent.com/13018877/90963169-95849700-e4f0-11ea-9ce6-ce141655464f.png)

![스크린샷 2020-08-23 오전 3 26 05](https://user-images.githubusercontent.com/13018877/90963171-97e6f100-e4f0-

11ea-88a7-b6d321841cc8.png)

### 3. Priority Settings Generally Don't Impact Performance Significantly

When the AutoLayout Engine requests values from views, it first checks whether the received constraints contain errors. If there are errors, the Engine asks the views to minimize the errors. During this error minimization process, the Engine uses the [Simplex Algorithm](https://en.wikipedia.org/wiki/Simplex_algorithm) to find the optimal solution that minimizes errors. This process is generally not costly, so it doesn't significantly impact AutoLayout's performance.

![스크린샷 2020-08-23 오후 6 50 13](https://user-images.githubusercontent.com/13018877/90975685-809c1800-e571-11ea-92a7-f4f26ac1febf.png)

> AutoLayout treats constraints other than Required Priority (1000) as optional constraints. AutoLayout does not prioritize optional constraints initially. It calculates all other constraints first and, if there's any ambiguity in the layout, it uses optional constraints to resolve the ambiguity. This entire process is AutoLayout's error minimization process.

### 4. Eliminate Constraint Churn

"Constraint churn" refers to unnecessarily complex constraints or repetitive addition/removal of constraints that don't change the visual layout but add unnecessary complexity. In other words, while the actual view layout remains the same, constraint operations cause the AutoLayout Engine to do more work. Excessive constraint churn can negatively impact AutoLayout's performance. Constraint churn often occurs in the following situations:

- Removing all constraints and reapplying them.
- Modifying constraints that don't need to be changed.
- Repeatedly adding and removing constraints.

On the contrary, you can reduce constraint churn by following these practices:

- Avoid removing all constraints.
- Add constraints only once for static constraints that don't need to be added dynamically during updates.
- Modify only the necessary constraints.
- Use view hiding instead of adding/removing constraints when possible.*

> Note: Hiding a view is much less costly than changing constraints. Therefore, if hiding a view while maintaining the correct layout is possible, it's better for performance to not modify the constraints.

#### Constraint Churn and the Render Loop

Unintentional constraint operations can occur inside the `updateConstraints()` and `layoutSubviews()` methods. When rendering views on iOS, you go through a Render Loop. This loop operates as follows:

1. `updateConstraints()` is called - Views are called leaf-to-window in the view hierarchy.
2. `layoutSubviews()` is called - Called from window to subviews.
3. `draw(rect:)` is called - Called from window to subviews.

The Render Loop is executed whenever the view's bounds change, a rotation event occurs, or when `setNeedsLayout()` and `layoutIfNeeded()` are called. In other words, the methods in the Render Loop are called frequently as layout changes are needed, so they may be called many times. Thus, when overriding `updateConstraints()`, it's essential to consider constraint operations carefully to avoid performance issues. When dealing with the Render Loop cycle, prioritize the following considerations:

1. Update constraints only when necessary (e.g., during initial setup or when constraints need updates due to events).
2. Consider using `updateConstraints()` and `layoutSubviews()` only when you genuinely need them for layout changes.

![스크린샷 2020-08-23 오후 8 31 45](https://user-images.githubusercontent.com/13018877/90977348-afb98600-e57f-11ea-93e8-05a81738dc1a.png)

# References

- [AutoLayout - Understanding AutoLayout](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/AutolayoutPG/index.html#//apple_ref/doc/uid/TP40010853-CH7-SW1)
- [AutoLayout - Anatomy of a Constraint](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/AutolayoutPG/AnatomyofaConstraint.html#//apple_ref/doc/uid/TP40010853-CH9-SW1)
- [High Performance AutoLayout](https://developer.apple.com/videos/play/wwdc2018/220)