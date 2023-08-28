---
layout: post
comments: true
title: "Understanding iOS URLSession"
excerpt: "Exploring the URLSession API in iOS for networking."
categories: iOS URLSession Networking UIKit
date: 2017-07-30 00:30:00
tags: [iOS, URLSession, Networking, UIKit]
image:
  feature: iOS.png
---

## Table of Contents

1. [URLSession's Request and Response](#urlsession-request-and-response)
1. [Basic Concepts of URLSession](#basic-concepts-of-urlsession)
    1. [Session](#session)
    1. [Request](#request)
    1. [Task](#task)
1. [Using URLSession dataTask](#using-urlsession-datatask)

To facilitate communication with servers in iOS apps, Apple provides the `URLSession` API. `URLSession` is a fundamental API that underlies popular libraries like Alamofire and SDWebImage for data exchange with servers in iOS app development. `URLSession` supports several protocols, including HTTP, and provides features such as authentication, cookie management, and caching.

## URLSession's Request and Response

Like any other HTTP communication, `URLSession` has a fundamental structure consisting of a `Request` and a `Response`. First, `Request` can be made directly through a `URL` object or by creating a `URLRequest` object with options. Next, the `Response` can be received in the form of a `Completion Handler` for configured `Task` or by invoking specified methods via the `URLSessionDelegate`.

Generally, for simple responses, you can use `Completion Handlers`. However, scenarios like supporting file downloads in the background when the app is in the background state, or situations where default options for authentication and caching are not used, would require using the `Delegate` pattern.

## Basic Concepts of URLSession

`URLSession` typically follows the following life cycle:

1. Determine the `Session` configuration and create a `Session`.
2. Set up the URL and Request objects for communication.
3. Decide on the `Task` to use and write corresponding `Completion Handlers` or `Delegate` methods.
4. Execute the chosen `Task`.
5. After the Task is completed, the `Completion Handler` is executed.

### 1. Session

`URLSession` primarily supports three types of Sessions:

1. `Default Session`: The basic session with disk-based caching support.
2. `Ephemeral Session`: A session that doesn't store any data.
3. `Background Session`: A session that allows communication even after the app has terminated.

### 2. Request

You can use `URLRequest` to configure how the request to the server should be made. You can specify options such as how data should be cached, which HTTP method to use (GET, POST, etc.), and what content to send.

### 3. Task

Task objects typically handle URL-based content retrieval after the Session sends the server request. Three types of Tasks are supported:

1. `Data Task`: Used for sending and receiving data objects.
2. `Download Task`: Used for downloading data and storing it in files. Supports background downloads.
3. `Upload Task`: Used for uploading data in file form.

## Using URLSession dataTask

Networking APIs like `URLSession` are generally used globally within an app. Therefore, it's recommended to create a separate module (class) and define static functions inside it, rather than writing methods directly in a ViewController.

```swift
// Works properly in Swift 5.1 and iOS 13 environment.
class NetworkHandler {
    class func getData(resource: String) {
        // Create a session and configure it.
        let defaultSession = URLSession(configuration: .default)

        guard let url = URL(string: "\(resource)") else {
            print("URL is nil")
            return
        }

        // Create a request.
        let request = URLRequest(url: url)

        // Create a dataTask.
        let dataTask = defaultSession.dataTask(with: request) { (data: Data?, response: URLResponse?, error: Error?) in
            // Handle data retrieval errors.
            guard error == nil else {
                print("Error occur: \(String(describing: error))")
                return
            }

            guard let data = data, let response = response as? HTTPURLResponse, response.statusCode == 200 else {
                return
            }

            // Successful communication results in data being received in the 'data' object.

            // If the received data is in JSON format,
            // you can serialize the JSON into Swift data types.
            // JSON serialization is the process of converting JSON data into a String format that can be used in Swift.
            guard let jsonToArray = try? JSONSerialization.jsonObject(with: data, options: []) else {
                print("json to Any Error")
                return
            }
            // Perform desired operations.
            print(jsonToArray)
        }
        dataTask.resume()
    }
}

NetworkHandler.getData(resource: "http://www.example.com")
```

Starting with Swift 4, JSON serialization is now possible at the object level (`Codable`). For more information, please refer to the link below.

[Example of Using Swift 4 JSON Serialization](https://gist.github.com/hcn1519/0d685b1f0aba74ed9577e9cab1b02b6f)