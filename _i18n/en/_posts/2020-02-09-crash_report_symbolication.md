---
layout: post
title: "Crash Report Symbolication"
date: "2020-02-09 00:53:17 +0900"
excerpt: "Exploring Crash Report Symbolication"
categories: iOS, macOS, BuildSystem, Symbol, CrashReport
tags: [iOS, macOS, BuildSystem, Symbol, CrashReport]
image:
  feature: iOS.png
table-of-contents: |
  ### Table of Contents
  1. [Generating Crash Reports](./crash_report_symbolication#1-generating-crash-reports)
  2. [Symbol and Symbolication](./crash_report_symbolication#2-symbol-and-symbolication)
  3. [Crash Report Symbolication](./crash_report_symbolication#3-crash-report-symbolication)
  4. [Appendix](./crash_report_symbolication#4-appendix)
---

In this post, we will explore how crash reports are generated in apps and how they can be symbolicated in AppStore Connect.

> Note: Before we begin, it's important to mention that much of the content in this article is a summary of [Understanding and Analyzing Application Crash Reports - Apple Doc](https://developer.apple.com/library/archive/technotes/tn2151/_index.html#//apple_ref/doc/uid/DTS40008184-CH1-INTRODUCTION).

## 1. Generating Crash Reports

When a crash occurs on the device you're using, the system generates a crash report and stores it internally on the device. Crash reports contain information about the environment at the time the crash occurred and other useful data.

<div class="message">
    Crash reports describe the conditions under which the application terminated, in most cases including a complete backtrace for each executing thread, and are typically very useful for debugging issues in the application.
</div>

You can find crash reports on the device's settings:

> Settings > Privacy > Analytics & Improvements > Analytics Data

When you examine these stored crash reports, you can get a rough idea of the environment in which the crash occurred. However, it's often challenging to determine exactly where in your source code the crash happened by looking at the backtrace from the thread where the crash occurred. While you can generally identify which framework had an issue, this information is too broad to be of significant help in debugging. The reason for this lack of clarity is that the crash report is in an "Unsymbolicated" state. The format in which crash reports are presented changes depending on whether they have been symbolicated.

## 2. Symbol and Symbolication

### Symbol

If you've read this far, you already know that crash logs need to be symbolicated for developers to analyze them properly. But what is "symbolication"? To understand symbolication, it's important to first know what a "symbol" is.

<div class="message">
    Symbol - A symbol in computer programming is a primitive data type whose instances have a unique human-readable form.
</div>

A "symbol" is a data type that is **human-readable**, and it is typically unique within the scope where it exists. Symbols in programming can include things like global variables, local variables, function names, and argument values.

Symbols are usually stored in a data structure called a "Symbol Table," often implemented as a hash table. A Symbol Table stores information about what each symbol means in the source code.

<div class="message">
    Symbol Table - In computer science, a symbol table is a data structure used by a language translator such as a compiler or interpreter, where each identifier (a.k.a. symbol) in a program's source code is associated with information relating to its declaration or appearance in the source.
</div>

The Symbol Table is typically kept separate from the compiled binary. In other words, when you release your app, the built `.app` doesn't include Symbol Table information. This is because the Symbol Table doesn't directly affect your app's execution, and it can be quite large. So, in most cases, the Symbol Table only exists in memory during the compiler's source code interpretation process, specifically during debugging and crash report symbolication.

> Removing symbols from object files compiled during the app build process is often referred to as [stripping](https://www.computerhope.com/unix/strip.htm). When distributing the app in a release, you use stripped binaries.

The information contained in a Symbol Table varies slightly depending on the programming language, but it generally includes:

* The symbol's name
* Whether the symbol is relocatable (absolute or relocatable)
* The location or address value of the symbol
* In high-level languages, Symbol Tables can also contain information about the symbol's data type, size, dimensions, length, and so on.

### Debug Symbol

A "Debug Symbol" (`dSYM`) is a type of symbol that carries additional information in the symbol table of an object file, such as a shared library or an executable.

<div class="message">
    A debug symbol is a special kind of symbol that attaches additional information to the symbol table of an object file, such as a shared library or an executable.
</div>

Therefore, Debug Symbols carry more information than regular Symbols. They include information about where the symbol in machine instructions (address information) maps to specific lines of your source code, the size of the symbol, and which class or struct it belongs to, among other things.

### Symbolication

Now, let's delve into what "symbolication" means in the context of crash reports.

<div class="message">
    Symbolication is the process of resolving backtrace addresses to source code method or function names, known as symbols.
</div>

Symbolication is the process of converting memory addresses in a backtrace into human-readable "symbols" such as method or function names. In symbolicated crash reports, you can see exactly where in your source code the crash occurred.

## 3. Crash Report Symbolication

We've briefly looked at how crash reports are generated on devices and how you can export them. However, many crashes occur on users' devices, and asking them to send their crash logs for debugging is inconvenient and not a practical way to analyze crashes.

To address this issue, Apple allows users who have agreed (or Test Flight users) to provide Diagnostic Data for their devices where crashes occurred (symbolicated crash reports). Let's explore how Apple provides Diagnostic Data and the central role of crash report symbolication in this process.

Images for each step can be found [here](https://developer.apple.com/library/archive/technotes/tn2151/Art/tn2151_crash_flow.png).

1. As your code is compiled, the compiler generates Debug Symbols alongside it. Debug Symbols contain information about how machine instructions (address information) in the compiled binary map to specific lines of your source code.
2. When you archive your app for App Store distribution, Xcode creates a `.xcarchive` file in the `~/Library/Developer/Xcode/Archives` directory.
3. When you distribute your app on the App Store or through Test Flight, you can choose whether to upload the `dSYM` file alongside it. Enabling this option allows you to view crash report information in iTunes Connect.
4. When a crash occurs in your app, an "Unsymbolicated" crash report is stored on the device.
5. You can obtain these unsymbolicated crash reports in various ways: by exporting them directly from a user's device, by connecting the device to a Mac and using Xcode to obtain them

, or by viewing Diagnostic Data from users who have agreed to share it in iTunes Connect.
6. You can symbolicate unsymbolicated crash reports using the `dSYM` file. Symbolication converts memory addresses in the backtrace into human-readable symbols.
7. In iTunes Connect, uploaded dSYM files are used to symbolicate crash reports, allowing you to see where crashes occurred in your source code.

> The `dSYM` file and the app binary identify each other using a "Build UUID." Each time you build, a new Build UUID is generated. This means that even if you build without changing your source code, the previously generated dSYM file and the newly created app binary will have different Build UUIDs.

## 4. Appendix

### Xcode - Configuring dSYM

You can decide whether to include Debug Symbols in the compiled binary through the Xcode Build Setting called "Debug Information Format."

<img width="707" alt="Screenshot 2019-12-14 at 10.03.34 PM" src="https://user-images.githubusercontent.com/13018877/70849116-9bd06700-1ebd-11ea-80db-19a2b04d7d7e.png">

Typically, in Debug mode, you include Debug Symbols in the binary, while in Release mode, you exclude them to reduce binary size. Below is a build result when you set the "Debug Information Format" to "DWARF with dSYM File" and build:

<img width="1018" alt="Screenshot 2020-01-28 at 2.25.59 AM" src="https://user-images.githubusercontent.com/13018877/73197982-a39a5100-4175-11ea-8f90-fe21f809494c.png">

## References

* [Understanding and Analyzing Application Crash Reports - Apple Doc](https://developer.apple.com/library/archive/technotes/tn2151/_index.html#//apple_ref/doc/uid/DTS40008184-CH1-INTRODUCTION)
* [Symbol](https://en.wikipedia.org/wiki/Symbol_(programming))
* [Symbol Table](https://en.wikipedia.org/wiki/Symbol_table)
* [Debug Symbol](https://en.wikipedia.org/wiki/Debug_symbol)