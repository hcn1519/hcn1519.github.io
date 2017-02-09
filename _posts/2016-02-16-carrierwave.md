---
layout: post
comments: true
title:  "Rails에서 carrierwave를 이용하여 AWS S3에 이미지 올리기"
excerpt: "Rails에서 이미지를 다루는 대표 gem중 하나인 carrierwave를 이용하여 AWS S3에 이미지를 올리는 방법에 대해 알아봅니다."
categories: Rails AWS 
date:   2016-02-17 00:30:00
tags: [Rails, Carrierwave, AWS_S3]
image:
  feature: RailsBanner.jpg
---
{% highlight html %}
<h5>Carrierwave를 이용하여 AWS S3에 이미지 올리기</h5>
  <ol>
    <li>프로젝트 진행을 위한 기본 scaffold 구성</li>
    <li>carrierwave, mini_magick, fog 설치</li>
    <li>carrierwave, mini_magick, fog 셋팅</li>
    <li>효율적으로 이미지 사용하기</li>
  </ol>
{% endhighlight %}

<p>&nbsp;정보의 대부분이 문자, 그림으로 이루어진 웹 어플리케이션에서 이미지를 다루는 것은 중요한 문제입니다. 이미지도 문자열과 마찬가지로, 서버에 저장되고 보여질 필요가 있습니다. 예컨데, 커뮤니티 게시판에 이미지가 포함된 글을 올린다고 했을 때, 내가 쓴 글의 제목과 내용이 특정 게시판에 가면 보여지듯이 이미지도 같이 보여져야만 합니다.</p>
<p>&nbsp;그렇다면 이미지는 어떻게 저장해야 되는 걸까요? 여러가지 방법이 있습니다만, 여기서 소개하는 방법은 AWS(아마존 웹 서비스)에서 제공하는 클라우드 저장공간(S3)에 내가 만든 이미지를 저장해놓고, 저장시 생성되는 이미지 경로만 따로 우리 데이터베이스에 저장해서 이미지가 호출될 필요가 있을 때, 지속적으로 불러들이는 방법입니다. 간단하게 생각해서 구글드라이브나 드랍박스에 우리가 이미지를 저장하게 되면 특정 이미지 경로를 얻을 수 있는데, 여기서 이미지 경로만 데이터베이스에 저장하는 작업을 자동화하는 것이라고 생각하시면 됩니다.</p>
<p>&nbsp;그리고 이 작업을 도와주는 rails의 gem들이 바로 <code>carrierwave</code>, <code>mini_magick</code>, <code>fog</code>입니다. 이 포스팅에서는 해당 gem들을 어떻게 사용할 수 있는지 알아보겠습니다. 작업에 사용된 ruby와 rails 버전은 각각 <code>ruby 2.2.2</code>, <code>rails 4.2.4</code>입니다.</p>


<h4>1. 프로젝트 진행을 위한 기본 scaffold 구성</h4>
<p>&nbsp;먼저 이미지를 올리기 위한 게시판을 scaffold로 간단하게 구성해보겠습니다.</p>
{% highlight html %}
rails generate scaffold Post title:string content:text
{% endhighlight %}
<p>&nbsp;다음으로 scaffold로 만든 index페이지를 기본 페이지로 만들기 위해 <code>config/route.rb</code>에 root를 추가해줍니다.</p>
{% highlight ruby %}
#config/route.rb
Rails.application.routes.draw do
  root :to => 'posts#index'
  resources :posts
end
{% endhighlight %}
다음으로 migration 해주시면 기본 설정은 끝납니다.
{% highlight html %}
rake db:migrate
{% endhighlight %}

<h4>2. carrierwave, mini_magick, fog 설치</h4>
<p>&nbsp;gem의 설치에 앞서서 각각의 gem이 어떤 역할을 하는지 간략하게 알아보면 다음과 같습니다.</p>
<ol>
  <li><code>Carreirwave</code>는 이미지 파일뿐만 아니라, 여러가지 파일을 업로드하는 것을 도와주는 gem입니다.</li>
  <li><code>Minimagick</code>은 image_magick의 rails버전인데, 이미지를 만들고, 수정하고, 지우는 작업들을 도와주는 gem입니다.(유사품: Rmagick)</li>
  <li><code>Fog</code>는 클라우드에 파일의 저장을 쉽게할 수 있도록 도와주는 gem입니다.</li>
</ol>
<p>&nbsp;각각의 gem이 하는 일을 보시면 이미지 업로드에 왜 해당 gem들이 필요한지 알 수 있을 것이라 생각됩니다. 이제 프로젝트에 각각의 gem을 설치해보도록 하겠습니다.</p>
{% highlight ruby %}
#Gemfile
gem 'carrierwave', github: 'carrierwaveuploader/carrierwave'
gem 'mini_magick'
gem 'fog-aws'
{% endhighlight %}
<p>&nbsp;다음으로</p>
{% highlight html %}
bundle install
{% endhighlight %}
<p>&nbsp;까지 해주면 필요한 gem의 설치가 완료됩니다.</p>
<p>&nbsp;또한 minimagick을 사용하기 위해서는 image_magick도 설치해주어야 합니다.</p>

{% highlight html %}
sudo apt-get -y install imagemagick
{% endhighlight %}

<h4>2. carrierwave, mini_magick, fog 셋팅</h4>

<p>&nbsp;다음으로 해당 gem들을 사용할 수 있도록, 각각의 github페이지에서 제공하는 사용법을 활용하여 해당 gem들을 사용해보도록 하겠습니다.</p>

<h5>(1) Uploader 셋팅</h5>

<p>&nbsp;가장 먼저 carrierwave uploader 셋팅을 위해</p>

{% highlight html %}
rails generate uploader S3
{% endhighlight %}

<p>&nbsp;아래에서 볼 수 있듯이 <code>app/uploaders/s3_uploader.rb</code>에 새로운 파일이 생성된 것을 확인할 수 있습니다.</p>
<img src="http://dl.dropbox.com/s/e3xbpkna2rzgnmf/uploader.PNG">

<p>&nbsp;해당 파일에 들어가보면, carrierwave에서 제공하는 다양한 저장 옵션이 주석처리되어 있습니다.</p>
{% highlight ruby %}
class S3Uploader < CarrierWave::Uploader::Base

  # 이미지를 조정할 수 있는 툴 설정
  # Include RMagick or MiniMagick support:
  # include CarrierWave::RMagick
  include CarrierWave::MiniMagick

  # 이미지를 저장할 장소의 종류를 설정
  # Choose what kind of storage to use for this uploader:
  # storage :file
  storage :fog

  #이미지가 저장되는 위치
  # Override the directory where uploaded files will be stored.
  # This is a sensible default for uploaders that are meant to be mounted:
  def store_dir
    "uploads/#{model.class.to_s.underscore}/#{mounted_as}/#{model.id}"
  end

  # 요청한 이미지가 없을 때 대체해서 사용하는 default 이미지 설정
  # Provide a default URL as a default if there hasn't been a file uploaded:
  # def default_url
  #   # For Rails 3.1+ asset pipeline compatibility:
  #   # ActionController::Base.helpers.asset_path("fallback/" + [version_name, "default.png"].compact.join('_'))
  #
  #   "/images/fallback/" + [version_name, "default.png"].compact.join('_')
  # end

  # 이미지를 저장할 사이즈 조정
  # Process files as they are uploaded:
  # process scale: [200, 300]
  #
  # def scale(width, height)
  #   # do something
  # end

  # 여러가지 이미지의 버전 설정
  # Create different versions of your uploaded files:
  # version :thumb do
  #   process resize_to_fit: [50, 50]
  # end

  # 저장될 파일들의 확장자 설정
  # Add a white list of extensions which are allowed to be uploaded.
  # For images you might use something like this:
  def extension_whitelist
    %w(jpg jpeg gif png)
  end

  # 저장되는 파일의 이름 설정
  # Override the filename of the uploaded files:
  # Avoid using model.id or version_name here, see uploader/store.rb for details.
  # def filename
  #   "something.jpg" if original_filename
  # end
end
{% endhighlight %}
<p>&nbsp;각각의 옵션이 어떤 역할을 하는지 주석으로 간략하게 서술해 놓았는데, 필요한 부분에 대해서는 <a href="https://github.com/carrierwaveuploader/carrierwave" target="_blank">Carrierwave github 페이지</a>를 참조하시기 바랍니다. 여기서 설정은 위와 동일하게 하면 됩니다. 짚고 넘어갈 점은 mini_magick을 설정해두고, storage를 fog로 변경하여 s3에 이미지 업로드가 문제 없이 될 수 있도록 설정해두었다는 점입니다.</p>

<h5>(2) Model 셋팅</h5>
<p>&nbsp;다음으로 만들어놓은 Post model에 각각의 post가 이미지를 가져야 하기 때문에 이미지 링크가 저장될 공간을 확보해두어야 합니다. 그에 따라 기존 model에 새로운 문자열 저장 공간(column)을 만들어야 합니다.</p>
{% highlight html %}
rails g migration add_s3_to_posts image:string
rake db:migrate
{% endhighlight %}
<p>&nbsp;이렇게 명령어를 실행하면 post모델에 image라는 이름으로 string을 저장할 수 있는 공간이 생성됩니다. 또한 post 모델이 uploader를 사용할 수 있도록 mount 명령어를 추가해주어야 합니다.</p>
{% highlight ruby %}
#app/models/post.rb
class Post < ActiveRecord::Base
  mount_uploader :image, S3Uploader
end
{% endhighlight %}
<p>&nbsp;여기까지가 carrierwave 관련 셋팅이고, 다음으로 fog 셋팅을 진행하도록 하겠습니다.</p>

<h5>(3) config 설정</h5>
<p>&nbsp;<code>fog-aws</code>를 사용하기 위해서는 <code>config/initializers</code>에 fog.rb 파일을 직접 생성해야 합니다. 그리고 다음의 코드를 해당 파일에 넣어주세요.</p>
{% highlight ruby %}
CarrierWave.configure do |config|
  config.fog_provider = 'fog/aws'                        # required
  config.fog_credentials = {
    provider:              'AWS',                        # required
    aws_access_key_id:     'xxx',                        # required
    aws_secret_access_key: 'yyy',                        # required
    region:                'ap-northeast-2',             # optional, defaults to 'us-east-1'
  }
  config.fog_directory  = 'name_of_directory'            # required
end
{% endhighlight %}

<p>&nbsp;위 코드에서 id, key, region, 'name_of_directory'부분을 여러분들의 설정에 맞게 변경해주어야 합니다. 여기서 region은 서울의 경우 ap-northeast-2이며, 도쿄는 ap-northeast-1입니다. ID와 Key의 경우 s3 탭에서 설정하는 것이 아니고,</p>

<img src="http://dl.dropbox.com/s/dpzkl7v69172vsb/aws_users.png">

<p>&nbsp;우측 상단의 본인 계정탭의 Security Credentials에서 생성하는 것입니다. 그리고 Security Credentials에서 users탭을 누르고 user를 생성하되, 중간에 id와 key의 경우 따로 메모해두시고, <code>fog.rb</code>에 채워넣으시면 됩니다. 또한 Permissions 항목에서 Attach policy를 한 후 s3full_access로 한 개의 policy를 생성해야 s3에 정상적으로 사진을 저장할 수 있습니다.</p>
<p>&nbsp;다음으로 fog_directory의 경우 S3의 Bucket 이름으로, 간단한 생성 방법을 알려주는 링크로 설명을 대신하겠습니다.</p>
<a href="http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html" target="_blank">Creating a Bucket</a>

<h5>(4) View에서 이미지 파일을 올리고  볼 수 있게 하는 parameter 셋팅</h5>

<p>&nbsp;이제 파일을 저장할 수 있도록 <code>:image</code> parameter 전송 셋팅을 해주고, view에서 해당 이미지가 보이도록 설정해주겠습니다.</p>
<p>&nbsp;가장 먼저 <code>app/views/posts/_form.html.erb</code>의 경우</p>

{% highlight erb %}
<%= form_for(@post) do |f| %>
  <% if @post.errors.any? %>
    <div id="error_explanation">
      <h2><%= pluralize(@post.errors.count, "error") %> prohibited this post from being saved:</h2>

      <ul>
      <% @post.errors.full_messages.each do |message| %>
        <li><%= message %></li>
      <% end %>
      </ul>
    </div>
  <% end %>

  <div class="field">
    <%= f.label :title %><br>
    <%= f.text_field :title %>
  </div>
  <div class="field">
    <%= f.label :content %><br>
    <%= f.text_area :content %>
  </div>
  <div class="field">
    <%= f.label :image %><br>
    <%= f.file_field :image, accept: 'image/png,image/gif,image/jpeg' %>
  </div>
  <div class="actions">
    <%= f.submit %>
  </div>
<% end %>
{% endhighlight %}
<p>&nbsp;이에 대한 결과물로 다음과 같은 form이 만들어집니다.</p>
<img src="http://dl.dropbox.com/s/z76rqnc9sreneew/new.PNG">

<p>&nbsp;form을 구성할 때 rails scaffold에서는 parameter를 두 번 체크하는 시스템을 가지고 있습니다. <code>app/controllers/posts_controller.rb</code>에는 다음과 같은 부분이 있습니다.</p>
{% highlight ruby %}
class PostsController < ApplicationController
  private
    # Never trust parameters from the scary internet, only allow the white list through.
    def post_params
      params.require(:post).permit(:title, :content, :image)
    end
end
{% endhighlight %}
<p>&nbsp;rails scaffold는 위의 <code>post_params</code>부분에서 view에서 넘어 온 parameter와 컨트롤러가 허용할 parameter를 비교하고, 허가 설정을 하지 않은 parameter에 대해서는 데이터를 넘기지 않습니다.(<a href='http://hcn1519.github.io/articles/2016-02/parameter' target='_blank'>Strong parameter</a>) 따라서 위 처럼 <code>:image</code>를 추가해주어야 합니다.</p>

<p>&nbsp;다음으로 <code>app/views/posts/index.html.erb</code>는</p>
{% highlight erb %}
<p id="notice"><%= notice %></p>

<h1>Listing Posts</h1>

<table>
  <thead>
    <tr>
      <th>Title</th>
      <th>Content</th>
      <th colspan="3"></th>
    </tr>
  </thead>

  <tbody>
    <% @posts.each do |post| %>
      <tr>
        <td><%= post.title %></td>
        <td><%= post.content %></td>
        <td><%= image_tag("#{post.image}") %></td>
        <td><%= link_to 'Show', post %></td>
        <td><%= link_to 'Edit', edit_post_path(post) %></td>
        <td><%= link_to 'Destroy', post, method: :delete, data: { confirm: 'Are you sure?' } %></td>
      </tr>
    <% end %>
  </tbody>
</table>

<br>
<%= link_to 'New Post', new_post_path %>
{% endhighlight %}

<p>&nbsp;마지막으로 <code>app/views/posts/show.html.erb</code>는</p>

{% highlight erb %}
<p id="notice"><%= notice %></p>

<p>
  <strong>Title:</strong>
  <%= @post.title %>
</p>

<p>
  <strong>Content:</strong>
  <%= @post.content %>
</p>
<p>
  <strong>사진:</strong>
  <%= image_tag("#{@post.image}") %>
</p>

<%= link_to 'Edit', edit_post_path(@post) %> |
<%= link_to 'Back', posts_path %>

{% endhighlight %}
<p>&nbsp;위의 결과물로 다음과 같은 <code>show.html.erb</code>가 만들어집니다.</p>
<img src="http://dl.dropbox.com/s/7z11wm9fabya0td/show.png">

<p>&nbsp;또한 AWS S3에 해당 이미지 파일이 잘 저장되어 있음을 확인할 수 있습니다.</p>
<img src="http://dl.dropbox.com/s/xa6nzl9g4u5g11u/s3_check.png">

<p>&nbsp;지금까지 기본적으로 이미지를 S3에 저장하는 방법을 알아보았습니다.</p>

<h4>4. 효율적으로 이미지 사용하기</h4>

<p>&nbsp;위에서 소개한 방법만으로 이미지를 다루는 것도 간단한 이미지를 다루는데 전혀 무리가 없습니다. 하지만, 이미지 파일의 크기가 너무 커서 사이트 로딩에 지장을 주는 상황이면 어떻게 해야 할까요? 한 페이지에 많은 이미지를 로딩하는 서비스(ex - 소셜 커머스, 쇼핑몰 등)에서도 원본 사진을 그대로 사용하는 것은 올바른 방법일까요?</p>
<p>&nbsp;물론 원본 사진을 그대로 써야하는 서비스도 분명 존재합니다. 하지만 대부분의 경우에는 사진의 퀄리티를 조금은 줄이더라도 속도를 개선하는 방향을 선택합니다. 그리고 사실 2MB 크기의 이미지를 200KB로 줄인다고 했을 때, 이미지 퀄리티가 우려할 정도로 많이 떨어지지 않습니다. 반면에  로딩속도는 엄청나게 빨라집니다.</p>

<p>&nbsp;그렇다면 이미지 용량은 어떤 식으로 줄여야 할까요? 가장 중요한 요소는 사진의 해상도(크기)입니다. 즉 <code>1920x1080</code> 크기의 사진을 <code>480x270</code>의 사이즈로 줄이게 되면 용량이 많이 줄어듦니다. 사진 크기를 이렇게 많이 줄여도 되나?라고 생각할 수 있지만, 대부분의 스마트폰은 너비(width)가 최대 400px 수준입니다. 즉, 사진을 적절히 줄여서 사용하는 것은 효율적으로 이미지를 활용하는 것이라 할 수 있습니다.</p>
<p>&nbsp;하지만, 데스크탑, 노트북에서 작은 이미지가 크게 늘여져서 나오는 현상도 바람직하지는 않습니다. 그런데, Carrierwave는 고맙게도 다양한 화면에서 적절한 이미지가 출력될 수 있도록 이미지를 여러가지 '버전'으로 저장할 수 있게 해줍니다. 즉, 큰 화면에는 큰 화면에 맞는 큰 이미지를 보여주고, 작은 화면에서는 작은 화면에 맞게 작은 이미지만 보여주는 것이 가능하다는 것입니다.</p>

<p>&nbsp;그리고 여러가지 이미지 '버전'은 <code>app/uploaders/s3_uploader.rb</code>에 minimagick을 통해 설정할 수 있습니다.</p>

{% highlight ruby %}
class S3Uploader < CarrierWave::Uploader::Base
  include CarrierWave::MiniMagick
  
  version :detail do
    process :resize_to_fit => [600, 10000]
  end
  version :main do
      process :resize_to_fill => [240, 180]
  end
end
{% endhighlight %}

<p>&nbsp;위의 예시처럼 설정하면 Carrierwave는 detail이라는 버전의 이미지와 main이라는 이미지를 본래 이미지를 조건에 따라 S3 안에 저장합니다. 위의 예시의 경우 detail 버전의 사진은 너비를 600px로 고정하고, 세로를 맞춘 사진이 됩니다. main 버전의 경우 4:3 비율로 사진을 축소 저장한 것입니다. 각각의 버전별 사용방법은 간단합니다. 그냥 기존 이미지 경로에 <code>.detail</code>, <code>.main</code>만 추가해주면 됩니다. 위의  예시에서 <code>app/views/posts/show.html.erb</code>의 이미지 태그인 <code><%= image_tag("#{@post.image}") %></code>의 경우, <code><%= image_tag("#{@post.image.main}") %></code>이라는 형식으로 쓰게 되면, main사이즈로 저장된 이미지가 출력됩니다.</code> 추가적으로 <code>:resize_to_fill</code>은 저 비율에 맞게 사진을 맞추는 것을 의미하고, <code>:resize_to_fit</code>은 짧은 길이에 맞춰서 나머지 부분을 조절하는 옵션입니다.</p>
<h5>(참고)추가 커스터마이징</h5>

<p>&nbsp;여기까지 잘 따라오셨으면, 이미지 버전에 대한 이해와 사용법까지 잘 이해했으리라 생각됩니다. 이 부분은 제가 Carrierwave를 사용할 때 맞닥뜨렸던 이슈와 관련된 추가 커스터마이징 내용입니다.</p>
<p>&nbsp;당시 프로젝트에서 저는 사용자가 스마트폰 사진을 웹에 올릴 수 있도록 하는 기능을 넣었습니다. 그런데 최근 나오는 아이폰6, 갤럭시S6, G4 등의 스마트폰은 모두 해상도가 어마어마합니다.(아이폰 <code>1920x1080</code>, 안드로이드 <code>2560x1440</code>) 그래서 위에서 사용한 방식대로 사진 사이즈를 줄여야 했는데, 문제는 스마트폰 사진 유형이 <strong>두 가지</strong>가 있다는 점이었습니다. 그래서 다음과 같은 코드를 새롭게 추가하였습니다.</p>

{% highlight ruby %}
class S3Uploader < CarrierWave::Uploader::Base
  include CarrierWave::MiniMagick
  
  version :detail do
    process :resize_to_fit => [600, 10000]
  end
  version :main do
      process :resize_to_fill => [240, 180] ,:if => :horizontal?
      process :resize_to_fill => [240, 320]  ,:if => :vertical?
  end

  def horizontal?(new_file)
    image = MiniMagick::Image.open(self.file.file)
    true if image[:height] < image[:width]
  end
  
  def vertical?(new_file)
    image = MiniMagick::Image.open(self.file.file)
    true if image[:height] > image[:width]
  end
end
{% endhighlight %}

<p>&nbsp;참고로 저는 <code>:main</code>버전에 대해서만 이 기능이 필요했기 때문에, <code>:main</code>에만 추가 코드를 작성했습니다. 의미는 다음과 같습니다. "사진이 가로가 긴 사진이면, <code>240x180</code>사이즈를 <code>:main</code>으로 저장하고, 세로가 긴 사진이면 <code>240x320</code>을 <code>:main</code>으로 저장해라!" 즉, 사진의 비율을 4:3로 만들고 사진 해상도를 줄이는 작업을 한 것이죠.</code></p>

<p>&nbsp;여기까지해서 Rails 프로젝트에 Carrierwave를 사용해서 AWS S3에 이미지를 올리는 방법에 대해 알아보았습니다. 글이 조금이라도 도움이 되셨길 바라며, 피드백, 수정 사항은 언제든지 환영합니다. 소스코드는 Github에서 확인하실 수 있습니다.</p>
<a href="https://github.com/hcn1519/carrierwave_aws_s3" target="_blank">Carreirwave로 AWS S3에 이미지 올리기</a>

<h5>더 볼만한 추가 자료</h5>

<ul>
  <li><a href="https://github.com/carrierwaveuploader/carrierwave" target="_blank">Carrierwave github 페이지</a></li>
  <li><a href="https://rorlab.gitbooks.io/railsguidebook/content/contents/walkthrough/gallery_layout.html" target="_blank">초보자를 위한 레일즈 가이드북, Carrierwave - 한글 파일 인코딩 자료 포함</a></li>
  <li><a href="http://lifesforlearning.com/uploading-images-with-carrierwave-to-s3-on-rails/" target="_blank">인도 형님이 쓰신 Carrierwave 자료 - 이미지 버전 설명 관련</a></li>
</ul>
