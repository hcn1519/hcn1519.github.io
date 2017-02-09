---
layout: post
comments: true
title:  "Rails SNS 로그인 구현"
excerpt: "Rails에서 devise gem과 omniauth gem을 사용하여 SNS 로그인을 구현하는 포스팅입니다."
categories: Rails Oauth2.0 Devise
date:   2016-12-29 00:30:00
tags: [Rails, Omniauth, Devise]
image:
  feature: omniauth.png
---
{% highlight html %}
<h5>Rails SNS 로그인 구현</h5>
  <ol>
    <li>1. Oauth2.0 이해</li>
    <li>2. Gem과 기본 페이지 생성</li>
    <li>3. Devise 설정하기</li>
    <li>3-2. config 설정</li>
    <li>4-1. 모델 설정</li>
    <li>4-2. 컨트롤러 설정</li>
    <li>4-3. 뷰 설정</li>
  </ol>
{% endhighlight %}

<p>&nbsp;Rails에서 <code>Devise gem</code>을 통해 회원가입 기능을 처음 구현해본 분이라면, 회원가입 기능 구현 정말 쉽구나!라고 생각하실 것 같습니다. 그리고 그 다음으로 드는 생각이 '그런데 요새 누가 회원가입 일일이 하지? 나는 facebook 로그인 같은 것들 넣고 싶은데?'일 것이라고 생각합니다. 근데 이게 직접 구글링을 통해 구현해보려는 사람들에게는 꽤나 복잡합니다. 저같은 경우에도 처음에 이런저런 블로그 포스팅들을 보면서 기능 구현을 시도해 보았는데, 1주일정도 걸렸던 것 같네요.</p>
<p>&nbsp;이런 분들을 위해 이번에 여러 포스팅들을 참고하며 <code>Devise</code>와 <code>Omniauth gem</code>에 익숙하지 않은 분들의 시선에서 SNS 로그인 구현을 해보고자 합니다. 이메일 인증과 같은 다소 복잡해질 수 있는 부분은 제외하고 Devise, Omniauth를 통해 기본적으로 구현할 수 있는 부분과 oauth api 중 이메일을 제공하지 않는 api를 서로 다른 경로로 보내 email을 서버에 저장할 수 있도록 하는 것까지 해보겠습니다.</p>

<h4>목표 - Devise와 Omniauth를 사용하여 SNS 로그인 구현</h4>
<a href="https://github.com/hcn1519/oauth-devise-configuration">소스코드 github 페이지</a>(ruby 2.3.1, rails 5.0.0)
<h4>1. Oauth2.0 이해</h4>

<p>&nbsp;코딩을 하기에 앞서서 oauth가 어떤 것인지 먼저 알면 model과 controller를 구성할 때 왜 그렇게 구성했는지 이해하기 쉽습니다. 그래서 읽어보시면 좋을 자료를 알려드리자면, <a href="http://earlybird.kr/1584">http://earlybird.kr/1584</a>의 글을 한 번 읽어보길 권장합니다.</p>
<p>&nbsp;복잡한 내용은 제쳐두고, 핵심만 알려드리자면, 다음 그림을 참고하시면 됩니다.</p>

<img src="https//dl.dropbox.com/s/dgx0isn6contbjp/oauth2_triangle2.png">
<p>출처는 <a href="http://earlybird.kr/1584">http://earlybird.kr/1584</a> 입니다.</p>

<p>&nbsp;저희가 사용하는 <span style="font-weight:bold">oauth2.0</span>에는 다양한 로그인 방식이 있다고 나와있습니다. 그 중 기본은</p>

<ol>
  <li>사용자가 "facebook 로그인"과 같은 버튼을 누르면</li>
  <li>facebook 인증 창으로 연결되도록 하여, 로그인을 하게 한다.</li>
  <li>그러면 facebook은 우리에게 access token(토큰)이란 것을 주고,</li>
  <li>이 토큰을 통해 이름, 이메일, 프로필 이미지 등의 정보를 제공받습니다.</li>
</ol>

<p>&nbsp;Access token을 통해 우리가 만드는 앱과 facebook이 사용자 정보를 주고 받는다 정도만 이해하셔도 무방합니다.</p>

<h4>2. Gem과 기본 페이지 생성</h4>

<p>&nbsp;이제 본격적으로 rails에 Devise와 Omniauth 기능을 추가해보도록 하겠습니다.</p>
<p>&nbsp;가장 먼저 <code>Gemfile</code>을 설치합니다.(디자인이나 기타 필요한 gem은 진행과정에서 추가하도록 하겠습니다.)</p>

{% highlight html %}
gem 'devise'
gem 'omniauth'
gem 'omniauth-facebook'
gem "omniauth-google-oauth2"
gem 'omniauth-kakao', :git => 'git://github.com/hcn1519/omniauth-kakao'
{% endhighlight %}

{% highlight html %}
bundle install
{% endhighlight %}

<p>&nbsp;다음으로 기본 레이아웃을 설정하겠습니다.</p>

<p>&nbsp;여기서는 랜딩페이지(/visitor/main), 로그인 후 추가적으로 정보를 받는 페이지(register/info1,2)를 만들어 놓습니다.</p>

{% highlight html %}
rails g controller visitor main
rails g controller register info1 info2
{% endhighlight %}

<p>&nbsp;다음으로 Devise 관련 셋팅입니다.</p>

<h4>3. Devise 설정하기</h4>

{% highlight html %}
rails generate devise:install
rails generate devise user
{% endhighlight %}

<p>&nbsp;이 명령어는 <code>User</code>라는 이름의 모델로 Devise가 제공하는 기능에 따라 기본적인 파일들을 만듭니다. 다음으로,</p>

{% highlight html %}
rails generate devise:views
rails generate devise:controllers user
{% endhighlight %}

<p>&nbsp;이 두 명령어는 Controller와 View를 Devise에 맞게 만들어주는 명령어입니다. 위 명령어를 치면 다음과 같은 Controller와 View가 생성됩니다.</p>

<img src="https//dl.dropbox.com/s/kpegzzfivvzz4r7/devise_result.png">

<p>&nbsp;먼저 View의 경우 Devise를 써보았다면 로그인 페이지(/users/sign_in), 회원가입 페이지(/users/sign_up) 등의 페이지가 만들어지는데 그것을 수정할 수 있도록 해주는 view들입니다.</p>
<p>&nbsp;다음으로 Controller의 경우 Devise로 할 수 있는 일들(로그인, 회원가입, 비밀번호 찾기, SNS 로그인 관리 등)을 나눠서 처리할 수 있는 Controllers들입니다.(그냥 사용하면 작동하지 않고, route.rb를 설정해주어야 사용할 수 있습니다. 이 부분은 뒤에서 자세히 설명하도록 하겠습니다.)</p>

<p>&nbsp;그 다음은 <code>User</code> 모델에 column을 추가하는 작업입니다. 여기서 저는 profile_img를 추가하도록 하겠습니다.</p>

{% highlight html %}
rails g migration add_colums_to_users profile_img:string
{% endhighlight %}

<p>&nbsp;또한, User는 여러 소셜 로그인 경로를 통해서 들어올 수 있기 때문에, 각각의 소셜 로그인 정보를 DB에 저장해야 합니다. 그래서, <code>identity</code>란 모델을 user의 belongs_to 관계로 만들고 소셜 로그인 정보(provider와 uid)를 저장합니다.</p>

{% highlight html %}
rails g model identity user:references provider:string uid:string
{% endhighlight %}

<p>&nbsp;여기까지 하시면, 더 추가되는 DB가 없기 때문에, 마이그레이션을 해줍니다.</p>

{% highlight html %}
rake db:migrate
{% endhighlight %}


<h4>3-2. config 설정</h4>

<p>&nbsp;이제 만들어둔 모델과 컨트롤러가 적절히 작동하도록 만들기 위해서 config를 수정합니다.</p>

{% highlight ruby %}
# config/route.rb
devise_for :users, :controllers => { omniauth_callbacks: 'user/omniauth_callbacks'}
{% endhighlight %}

<p>&nbsp;<code>route.rb</code>를 살펴보면, devise_for :users가 이미 설정되어 있는데, 그 뒤에 위의 코드를 추가해주시면 됩니다.</p>

{% highlight ruby %}
# config/initializers/devise.rb
# config.omniauth :facebook, "key", "secret", 여기에 직접 key를 넣지 마세요
config.omniauth :facebook, ENV["Facebook_Key"], ENV["Facebook_Secret"]
config.omniauth :google_oauth2, ENV["Google_Key"], ENV["Google_Secret"]
config.omniauth :kakao, ENV["Kakao_Key"], :redirect_path => "/users/auth/kakao/callback"
{% endhighlight %}

<p>&nbsp;다음으로 API Key 설정입니다. API 키라는 것은 각 provider가 제공하는 로그인 데이터를 이용하기 위해, 해당 developer 사이트로 가서 발급받아야 하는 key입니다. facebook은 <a href="https://developers.facebook.com">https://developers.facebook.com</a> 구글은 <a href="https://developers.google.com">https://developers.google.com</a> 카카오는 <a href="https://developers.kakao.com">https://developers.kakao.com</a>를 사용하고 있습니다. 이 key를 발급 받는 방법은 검색해보면 쉽게 찾으실 수 있으므로 여기서는 따로 설명하지 않겠습니다.</p>

<p>&nbsp;또, API key는 devise.rb에 직접 넣어서 작동시킬 수 있지만, 이렇게 하면, 나만 알아야 하는 key가 노출되는 보안상의 문제가 생깁니다. 이러한 문제를 해결해주는 것이 환경변수입니다.(ENV["~"] 형태의 변수들) 환경변수는 보안과 과금 등에 직결되는 key를 git에 올리지 않아도 사용할 수 있도록 만들어주는 변수입니다. 이를 쉽게 구현해주는 것이 <code>figaro</code>라는 gem입니다. <code>figaro</code>는 config에 <code>application.yml</code>를 생성하고 이것이 git에 업데이트가 되지 않도록 하는 gem입니다.</p>

{% highlight html %}
# Gemfile
gem figaro
{% endhighlight %}

{% highlight html %}
bundle install
bundle exec figaro install
{% endhighlight %}

<p>&nbsp;위처럼 설정해주면 config에 <code>application.yml</code>가 생성됩니다. 해당 파일 안에 사용하고자 하는 환경변수를 넣어주면, 이 파일은 자동으로 <code>.gitignore</code>에 추가되어, git에 업데이트가 되지 않습니다. 간단한 예로,</p>
{% highlight ruby %}
# config/application.yml
Facebook_Key: "실제 발급 받은 키"
Facebook_Secret: "실제 발급 받은 비밀번호"
{% endhighlight %}

<p>&nbsp;다음과 같이 설정하면, ENV["Facebook_Key"]를 통해 devise.rb에 실제 키를 올리지 않고, 사용할 수 있습니다. 좀 더 자세한 내용은 다음 링크를 참고해주세요.(<a href="http://railsapps.github.io/rails-environment-variables.html">Rails app 환경변수</a>)</p>


<p>&nbsp;이제 모델과 컨트롤러, 뷰에 각각의 내용을 채워주어야 합니다.</p>

<h4>4-1. 모델 설정</h4>
{% highlight ruby %}
# app/models/user.rb
class User < ApplicationRecord
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :trackable, :validatable, :omniauthable

  def self.find_for_oauth(auth, signed_in_resource = nil)

    # user와 identity가 nil이 아니라면 받는다
    identity = Identity.find_for_oauth(auth)
    user = signed_in_resource ? signed_in_resource : identity.user

    # user가 nil이라면 새로 만든다.
    if user.nil?

      # 이미 있는 이메일인지 확인한다.
      email = auth.info.email
      user = User.where(:email => email).first

      unless self.where(email: auth.info.email).exists?
        # 없다면 새로운 데이터를 생성한다.
        if user.nil?
          # 카카오는 email을 제공하지 않음
          if auth.provider == "kakao"
            # provider(회사)별로 데이터를 제공해주는 hash의 이름이 다릅니다.
            # 각각의 omnaiuth별로 auth hash가 어떤 경로로, 어떤 이름으로 제공되는지 확인하고 설정해주세요.
            user = User.new(
              profile_img: auth.info.image,
              # 이 부분은 AWS S3와 연동할 때 프로필 이미지를 저장하기 위해 필요한 부분입니다.
              # remote_profile_img_url: auth.info.image.gsub('http://','https://'),
              password: Devise.friendly_token[0,20]
            )

          else
            user = User.new(
              email: auth.info.email,
              profile_img: auth.info.image,
              # remote_profile_img_url: auth.info.image.gsub('http://','https://'),
              password: Devise.friendly_token[0,20]
            )
          end
          user.save!
        end
      end
    end

    if identity.user != user
      identity.user = user
      identity.save!
    end
    user

  end

  # email이 없어도 가입이 되도록 설정
  def email_required?
    false
  end
end

{% endhighlight %}

{% highlight ruby %}
# app/models/identity.rb
class Identity < ActiveRecord::Base
  belongs_to :user
  validates_presence_of :uid, :provider
  validates_uniqueness_of :uid, :scope => :provider

  def self.find_for_oauth(auth)
    find_or_create_by(uid: auth.uid, provider: auth.provider)
  end
end
{% endhighlight %}

<p>&nbsp;다음과 같이 추가됩니다. 여기서 설명이 필요한 부분이 <code>user.rb</code>입니다. 먼저 <code>user.rb</code>에는 devise의 역할에 <code>:omniauthable</code>이 추가되어야 합니다. 다음으로 <code>self.find_for_oauth</code>입니다. 이 함수는 가장 먼저 회원가입을 누른 사용자가 이미 가입한 유저인지를 확인합니다. 그 다음으로 사용자가 가입하지 않았던 사람이라면, 유저 정보를 새롭게 생성합니다. 여기서 앱은 <code>auth hash</code>를 수정하여 원하는 정보를 얻을 수 있습니다.</p>

<p>&nbsp;<code>auth hash</code>란, 로그인 기능 provider들(즉, 페이스북, 구글)별로 얻을 수 있는 정보를 hash로 저장한 것을 말합니다.(정확한 정의는 아니고.. 제가 임의의로 이해한 내용입니다.) 그래서, 각각의 omniauth github 페이지를 들어가보면 다음과 같이 <code>auth hash</code> 섹션을 두고, 어떤 정보를 어떤 이름으로 제공하는지 보여줍니다. 아래 예시는 google-oauth2의 예시입니다.</p>

<img src="https//dl.dropbox.com/s/jp7iir1sgx86os9/auth%20hash.png">

<p>&nbsp;이 <code>auth hash</code>를 provider별로 살펴보면, 소셜 로그인을 제공하는 서비스들은 크게 두 가지로 나눌 수 있습니다. 하나는 이메일을 api로 제공하는 서비스, 다른 하나는 이메일을 제공하지 않는 서비스입니다. 페이스북과 구글, 네이버의 경우 이메일을 제공하고, 카카오나 트위터, 라인, 인스타그램은 이메일을 제공하지 않습니다. 여기서 문제가 되는 부분은 이메일이 없는 서비스들입니다. Devise는 기본적으로 이메일을 통해 회원들을 구분하는 기능을 가지고 있습니다. 하지만 이메일을 제공하지 않는 api로 로그인하는 회원들의 경우, 그 회원들은 이메일이 없으니 그들을 구분하는 방법이 없어집니다.(user 모델에 email_required? 부분은 이메일 필수 여부를 false로 만들어 일단 이메일이 없어도 로그인이 되도록 만들었습니다.)</p>
<p>&nbsp;물론, 앞서 언급한 access token은 회원별로 이미 고유한 것들이기 때문에 시스템은 token으로 회원을 구분합니다. 하지만, 개발을 할 경우 일반적으로 token을 가지고 작업을 하기보다는 이메일 혹은 이름 같은 것들로 회원을 구별하기 때문에, 데이터베이스상에서 유일하게 존재하는 정보가 필요합니다.</p>

<p>&nbsp;Note: 여기서는 사용자가 이메일을 제공하는 provider를 통해 로그인할 경우(ex 페이스북 로그인)와 그렇지 않은 서비스로 로그인할 경우(ex 카카오 로그인) 서로 다른 페이지로 redirection 되도록 설정하되 이메일을 자체적으로 제공하지 않는 서비스들의 경우 이메일 입력을 별도로 받는 페이지로 가도록 설정 하겠습니다.</p>

<h4>4-2. Controller 설정</h4>

{% highlight ruby %}
# app/controllers/user/omniauth_callback_controller.rb
class User::OmniauthCallbacksController < Devise::OmniauthCallbacksController
  def self.provides_callback_for(provider)
    class_eval %Q{
      def #{provider}
        @user = User.find_for_oauth(env["omniauth.auth"], current_user)

        if @user.persisted?
          sign_in_and_redirect @user, event: :authentication
        else
          session["devise.#{provider}_data"] = env["omniauth.auth"]
          redirect_to new_user_registration_url
        end
      end
    }
  end
  [:kakao, :facebook, :google_oauth2].each do |provider|
    provides_callback_for provider
  end
  # provider별로 서로 다른 로그인 경로 설정
  def after_sign_in_path_for(resource)
    auth = request.env['omniauth.auth']
    @identity = Identity.find_for_oauth(auth)
    @user = User.find(current_user.id)
    if @user.persisted?
      if @identity.provider == "kakao"
        register_info2_path
      else
        register_info1_path
      end
    else
      visitor_main_path
    end
  end
end
{% endhighlight %}

<p>&nbsp;Controller에서는 크게 2가지 기능을 수행합니다. 첫 번째는 User 모델에서 생성한 self.find_for_oauth 함수를 호출하되, 파라미터로 현재 session 데이터와 provider로부터 받은 토큰 데이터를 사용하게끔 합니다. 두 번째는 after_sign_in_path_for를 통해, 로그인 후 redirect 되는 경로를 설정합니다. 여기서는 kakao 로그인의 경우만 이메일을 추가적으로 필요로하기 때문에 이를 register_info2_path로 보내고, 나머지는 register_info1_path으로 보내도록 설정하였습니다.</p>

<h4>4-3. 뷰 설정</h4>

<p>&nbsp;View같은 경우에는 css의 영향이 커서 모든 파일을 하나하나 설명하다보면 글이 지나치게 길어질 것 같아서 필수적으로 설명해야 하는 부분만 설명하고, 나머지는 링크로 대체하도록 하겠습니다. 여기서 제가 사용한 css framework은 <a href="http://semantic-ui.com/introduction/getting-started.html">semantic-ui</a>라는 것으로 다음과 같은 결과를 만들 수 있습니다.</p>

<img src="https//dl.dropbox.com/s/5wecl37xbiek8jj/login.png">

<p>&nbsp;여기서 수정하는 view는 다음과 같습니다.</p>
{% highlight html %}
app/views/devise   -- registrations -- new.html.erb
                   -- sessions      -- new.html.erb
                   -- shared        -- _links.html.erb
   /views/register -- _common_info.html.erb
                   -- info1.html.erb
                   -- info2.html.erb
   /views/visitor  -- main.html.erb
{% endhighlight %}
<p>&nbsp;그리고 여기에 관여하는 CSS 파일은 다음과 같습니다.</p>
{% highlight html %}
app/assets/stylesheets -- application.scss
                       -- register.scss
                       -- signupin.scss
                       -- visitoer.scss
{% endhighlight %}

<p>&nbsp;assets과 css는 이 포스팅과 크게 관련이 없기 때문에, 여기서는 설명하지 않고, devise와 register 영역만 설명하도록 하겠습니다.(나머지는 github을 참고해주세요.)</p>

{% highlight erb %}
# app/views/devise/registrations/new.html.erb
# 회원 가입과 관련된 부분입니다.
<%= stylesheet_link_tag 'signupin', media: 'all', 'data-turbolinks-track' => true %>

<div class="ui middle aligned center aligned grid loginForm">
  <div class="column loginColumn">
    <h2 class="ui orange image header loginImage">
      회원가입
    </h2>
  <%= form_for(resource, as: resource_name, url: registration_path(resource_name), :html => {class: "ui large form"}) do |f| %>
    <%= devise_error_messages! %>
    <div class="ui raised segment loginBox">
      <div class="field">
        <%= f.label :email, :class => 'ui left aligned header' %>
        <%= f.email_field :email %>
      </div>

      <div class="field">
        <%= f.label :name, '비밀번호', :class => 'ui left aligned header' %>
        <!--<% if @minimum_password_length %>
        <em>(<%= @minimum_password_length %> 자 이상이어야 합니다.)</em>
        <% end %><br />-->
        <%= f.password_field :password, autocomplete: "off", :placeholder => '6자 이상이어야 합니다.' %>
      </div>

      <div class="field">
        <%= f.label :name, '비밀번호 확인', :class => 'ui left aligned header' %>
        <%= f.password_field :password_confirmation, autocomplete: "off" %>
      </div>

      <div class="actions">
        <%= f.submit "회원가입", :class => 'ui fluid small yellow submit button'%>
      </div>
        <% end %>
    </div>
    <%= render "devise/shared/links" %>
  </div>
</div>
{% endhighlight %}

{% highlight erb %}
# app/views/devise/sessions/new.html.erb
# 로그인과 관련된 부분입니다.
<%= stylesheet_link_tag 'signupin', media: 'all', 'data-turbolinks-track' => true %>

<div class="ui middle aligned center aligned grid loginForm">
  <div class="column loginColumn">
    <h2 class="ui orange image header loginImage">
      회원가입
    </h2>
  <%= form_for(resource, as: resource_name, url: registration_path(resource_name), :html => {class: "ui large form"}) do |f| %>
    <%= devise_error_messages! %>
    <div class="ui raised segment loginBox">
      <div class="field">
        <%= f.label :email, :class => 'ui left aligned header' %>
        <%= f.email_field :email %>
      </div>

      <div class="field">
        <%= f.label :name, '비밀번호', :class => 'ui left aligned header' %>
        <!--<% if @minimum_password_length %>
        <em>(<%= @minimum_password_length %> 자 이상이어야 합니다.)</em>
        <% end %><br />-->
        <%= f.password_field :password, autocomplete: "off", :placeholder => '6자 이상이어야 합니다.' %>
      </div>

      <div class="field">
        <%= f.label :name, '비밀번호 확인', :class => 'ui left aligned header' %>
        <%= f.password_field :password_confirmation, autocomplete: "off" %>
      </div>

      <div class="actions">
        <%= f.submit "회원가입", :class => 'ui fluid small yellow submit button'%>
      </div>
        <% end %>
    </div>
    <%= render "devise/shared/links" %>
  </div>
</div>

{% endhighlight %}

<p>&nbsp;사실 이 부분도 거의 기존의 devise form을 유지하고 그 위에 약간의 디자인을 덧붙인 것에 불과합니다. 유의할 점은 <code><%=render "devise/shared/links" %></code>부분이 devise에서 자체적으로 소셜 로그인과 연결되어 있는 부분으로 단순히 "sign in with facebook"이라고 나오는 부분을 수정하기 위해서는 저 부분을 수정해야 한다는 것입니다.</p>

{% highlight erb %}
# app/views/devise/shared/_links.html.erb
# 소셜 로그인 버튼을 수정하는 부분입니다.
<%- if devise_mapping.omniauthable? %>
  <div>
    <%- resource_class.omniauth_providers.each do |provider| %>
      <%= link_to omniauth_authorize_path(resource_name, provider) do %>
        <%- if provider.to_s == "google_oauth2" %>
          <% provider = "google plus" %>
        <% end %>
        <button class="ui fluid large <%= provider %> icon button sns">
          <i class="<%= provider %> icon" style="float: left"></i>
          <% if provider.to_s == "facebook" %>
            <% sns = '페이스북' %>
          <% elsif provider.to_s == "google plus" %>
            <% sns = '구글' %>
          <% else %>
            <% sns = '카카오' %>
          <% end %>
          <%= sns %> 계정으로 로그인
        </button>
      <% end -%>
    <% end -%>
  </div>
<% end -%>
<%- if controller_name != 'sessions' %>
    <%= link_to "로그인", new_session_path(resource_name) %>
<% end -%>

<%- if devise_mapping.recoverable? && controller_name != 'passwords' && controller_name != 'registrations' %>
    <%= link_to "비밀번호 찾기", new_password_path(resource_name) %>&nbsp; | &nbsp;
<% end -%>

<%- if devise_mapping.registerable? && controller_name != 'registrations' %>
    <%= link_to "가입하기", new_registration_path(resource_name), :name => 'test' %>
<% end -%>

<%- if devise_mapping.confirmable? && controller_name != 'confirmations' %>
  <%= link_to "Didn't receive confirmation instructions?", new_confirmation_path(resource_name) %><br />
<% end -%>

<%- if devise_mapping.lockable? && resource_class.unlock_strategy_enabled?(:email) && controller_name != 'unlocks' %>
  <%= link_to "Didn't receive unlock instructions?", new_unlock_path(resource_name) %><br />
<% end -%>
<!--"Sign in with #{OmniAuth::Utils.camelize(provider)}"-->
{% endhighlight %}

<p>&nbsp;여기서는 3가지 provider별로 나오는 버튼이 수정되도록 만들었습니다. 카카오의 경우 해외 서비스가 아니라서 semantic-ui 자체적으로 아이콘을 제공하지 않습니다. 그래서 저 부분은 기능만 작동하도록 만들었습니다.</p>

<p>&nbsp;추가적으로 register 컨트롤러와 view는 여기서 따로 설명하지 않았습니다. 이 부분은 코드를 보시면 어떻게 작동하는지 쉽게 이해될 것이라고 생각됩니다. 궁금한 사항 있으시면 소셜 댓글, 제 메일로 알려주시면 제가 아는 한도내에서 답변 드리도록 하겠습니다.</p>

<h4>참고한 레퍼런스</h4>
<ul>
<li><a href="https://luciuschoi.gitbooks.io/exploring_devise/content/devise_omniauth/omniauth-twitter.html">초레가 devise 파헤치기</a></li>
<li><a href="https://www.sitepoint.com/rails-authentication-oauth-2-0-omniauth/">sitepoint rails oauth 구현하기</a></li>
<li><a href="https://github.com/mkdynamic/omniauth-facebook">oauth facebook github 페이지</a></li>
<li><a href="https://www.digitalocean.com/community/tutorials/how-to-configure-devise-and-omniauth-for-your-rails-application">how to configure devise and omniauth for your rails application</a></li>
<li><a href="https://github.com/plataformatec/devise/wiki/OmniAuth:-Overview">devise 위키 oauth 파트</a></li>
</ul>
