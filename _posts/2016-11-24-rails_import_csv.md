---
layout: post
comments: true
title:  "Rails에서 CSV 파일 import하기(by rake)"
excerpt: "커맨드라인에서 rake 명령어를 통해 CSV 데이터를 Rails 프로젝트 안에 넣는 방법에 대해 알아봅니다."
categories: rails rake csv
date:   2016-11-27 00:30:00
tags: [Rails, CSV, Rake]
image:
  feature: csvImport.png
---

<p>&nbsp;대부분의 프로젝트는 모델을 설계한 이후에 관련 데이터를 집어넣어야만 합니다. 예를 들자면, 학교 강의실 위치 데이터를 내 프로젝트에 넣고자 할 경우, 건물이름, 강의실 번호 등의 속성으로 설계된 모델에 각각의 강의실 정보를 입력해야 합니다. 그런데 form으로 그런 데이터를 집어넣을 수 있다는 것은 알고 있으실텐데, 이걸 form으로 일일이 집어 넣는 것은 정말 시간이 많이 드는 일입니다. 예컨데 강의실이 1,000개가 있다면, 강의실 입력 작업을 1,000번 해야되는 거죠.</p>

<p>&nbsp;이런 번거로운 작업을 대신 해주는 것이 CSV입니다. CSV는 무슨 거창한 것이 아니라, <code>Comma Separated Values</code>의 약자로 쉽게 생각하자면 메모장에 콤마(,) 단위로 데이터가 입력된 파일입니다. 이번 포스팅에서는 CSV로 만든 파일을 Rails 프로젝트의 데이터베이스에 올리는 방법을 알아보도록 하겠습니다.</p>

<h4>1. CSV 파일 생성하기</h4>
<a href="https://dl.dropbox.com/s/njvwf7ifcutpl3s/LectureRoom.csv" download>
LectureRoom.csv 다운로드
</a>
<p>CSV 파일은 Excel만 할 줄 아신다면 만드는 방법이 매우 간단합니다. 엑셀에서 다른 이름으로 저장하기에서 CSV 확장자로 저장만 해주면 됩니다.</p>

<img src="https://dl.dropbox.com/s/ubx9wc6jjh94ytq/csvSave.png"/>

<h4>2. CSV 파일 업로드</h4>
<p>&nbsp;그런데 Rails 프로젝트의 모델에 해당 CSV 데이터를 그대로 올려주려면, Excel에서 데이터를 만들 때 규칙을 지켜주어야 합니다. 즉, 모델의 속성명들과 CSV 데이터의 순서나 이름을 맞춰주어야 합니다. 다음과 같이 LectureRoom이라는 모델을 제가 만들었다고 가정하겠습니다.</p>

<img src="https://dl.dropbox.com/s/uayd6rzga3rnm15/lectureRoom.png">

<p>&nbsp;현재 LectureRoom 모델에는 building_name, room_number, full_name라는 3 가지 속성이 있습니다. 이와 같은 경우 CSV 파일의 경우 첫 번째 행에 속성명이 써있어야 하고, 다음 줄부터 데이터가 들어갑니다. 즉, 다음과 같이 데이터가 입력되어야 합니다.</p>

<img src="https://dl.dropbox.com/s/ua8em8n859ic8ta/lectureRoomExcel.png">

<p>&nbsp;여기서 id의 경우 모델의 기본 속성 중 하나이므로, 들어가도 무방합니다. 이제 이 파일을 <code>public</code>에 저장합니다. 파일명은 적당히 <code>ClassRoom.csv</code>로 설정하겠습니다.</p>

<h4>3. CSV 파일과 Rails 모델 연동하기</h4>

<p>&nbsp;다음은 CSV 파일과 Rails 모델의 연동입니다. 연동의 방법은 controller를 통해 연동하거나, rake 명령어를 통해 연동하는 방법이 있는데요. rake 명령어로 rake db:migrate하듯이 데이터를 올리는 것이 훨씬 간단하기 때문에, 여기서는 rake 명령어를 통해 연동을 해보도록 하겠습니다.</p>

<p>&nbsp;Rails 프로젝트 폴더를 살펴보면 <code>/lib/tasks</code>라는 폴더가 있습니다. 그곳에 <code>import_classrooms_csv.rake</code>라는 파일을 생성합니다. 다음으로 해당 파일 안에 다음 코드를 넣어줍니다.</p>

{% highlight ruby %}
require 'csv'
namespace :import_classrooms_csv do
  task :create_classrooms => :environment do
    CSV.foreach("public/ClassRoom.csv", :headers => true) do |row|
      ClassRoom.create!(row.to_hash)
    end
  end
end
{% endhighlight %}

<p>&nbsp;어떤 작업을 하는 지 간단하게 살펴보자면 다음과 같습니다.</p>

<ol>
<li>Rails에 내장되어 있는 CSV를 import합니다.</li>
<li>namespace는 해당 명령을 :import_classrooms_csv로 호출하겠다는 의미입니다.</li>
<li>task 이하는 해당 rake 명령어가 어떤 작업을 하는지를 보여주는 부분입니다.</li>
<li>여기서는 public 폴더에 있는 ClassRoom.csv 파일의 내용을 가지고, ClassRoom 모델을 생성하기 때문에 ClassRoom.create!(row.to_hash)를 넣었습니다.</li>
</ol>

<p>&nbsp;결과 화면은 다음과 같습니다.</p>

<img src="https://dl.dropbox.com/s/eq0jl6krmxcyw6y/rake.png">

<p>&nbsp;이제 rake 명령어로 해당 작업을 실행해주면 됩니다.</p>

{% highlight html %}
rake import_classrooms_csv:create_classrooms
{% endhighlight %}

<p>&nbsp;별 문제 없이 데이터가 들어갔다면, 다음과 같이 다음과 같이 나옵니다.</p>

<img src="https://dl.dropbox.com/s/3b3opt20toxgt2j/rakeTask.png">

<p>&nbsp;이제 데이터가 제대로 들어갔는지 콘솔을 통해 확인해보도록 하겠습니다.</p>

{% highlight html %}
rails c
ClassRoom.all
{% endhighlight %}

<p>&nbsp;확인해보시면, 데이터들이 다음과 같이 정상적으로 들어간 것을 확인하실 수 있습니다.</p>
<img src="https://dl.dropbox.com/s/fpjprhm910tvteq/example.png">
