---
layout: post
comments: true
title:  "Passenger-Nginx를 이용하여 AWS에 Rails 앱 배포하기"
excerpt: "Passenger gem과 Nginx를 이용하여 git에 올린 Rails 앱을 AWS를 이용하여 배포하는 것에 대해 이야기합니다."
categories: Rails AWS Nginx
date:   2016-02-25 00:30:00
tags: [Rails, Passenger, Nginx]
image:
  feature: nginx.jpg
translate: false
---
## 목차

<ol>
  <li>AWS 인스턴스 환경설정</li>
  <li>Ruby, Rails, Passenger gem 설치</li>
  <li>Nginx 설치</li>
  <li>Nginx 기본 셋팅</li>
  <li>앱을 조금 더 빠르게 만드는 Nginx 셋팅</li>
</ol>


두어달 전 쯤에 처음 AWS에 Nginx를 사용해서 Rails 앱을 배포한 적이 있었습니다. 당시 앱을 배포하기 전까지 궁금했던 점이 몇 가지 있었습니다. 그 중에서 가장 궁금했던 점은 아래 내용이었습니다.
<div class="message">
Development 모드에서 개발을 할 때 <code>rails s</code>라는 명령어로 서버를 켰다가 껐다가 하는데, 실제 Production 모드에서도 이런 식으로 서버를 켰다가 껐다가 하나요? 만약 그렇다면, 서버를 키기 위해서 컴퓨터를 계속 켜놔야 되는데 전 서버를 돌릴만한 여유 컴퓨터가 없는데요?
</div>

쓰고보니, 다른 분들은 이것에 대해 고민할 지에 대해 새로운 고민이 생기긴 했는데, 결론부터 얘기하자면 그럴 필요가 없습니다. 그리고 Rails 앱을 위해(Rails에만 쓸 수 있는 것은 아닙니다.) 컴퓨터를 계속 켜놓을 필요가 없게 만들어주는 것이 Nginx라는 웹 서버입니다. 생활코딩 페이지(<a href="https://opentutorials.org/module/384/3462" target="_blank">생활코딩 Nginx</a>)에 자세한 설명이 되어 있으니 참고하시기 바랍니다.


다시 돌아와서, 이 Nginx는 Rails 앱을 Production 모드로 배포할 수 있게 해줍니다. 그리고 Rails 앱을 배포할 수 있도록 도와주는 gem에는 `Passenger`와 `Unicorn`이 있습니다. 여기서는 그 중 `Passenger`라는 gem을 이용하여 AWS 인스턴스에 Nginx를 설치하고, 할당받은 ip주소를 입력하면 내가 만든 Rails 앱이 배포되는 작업을 해보도록 하겠습니다.

<h4>목표 - Passenger gem과 Nginx를 이용하여 Rails 앱 배포하기</h4>

참고로, 여기서는 서버를 띄우는 데 필수적인 AWS 인스턴스 환경설정에 대해서는 설명하지만, putty를 사용해서 인스턴스에 접근하는 방법이나, Mac 터미널을 이용하여 인스턴스를 실행하는 것에 대해서는 설명하지 않으려고 합니다. AWS에서 제공하는 사용법을 따라하시면, (사실 쉽지는 않지만) 충분히 하실 수 있으리라 생각합니다. 또한 자신의 github에 이미 Rails 프로젝트가 있다는 가정으로 글을 진행하도록 하겠습니다.

* <a href="http://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/putty.html" target="_blank">윈도우 사용자들의 putty를 활용한 인스턴스 접속
* <a href="http://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html" target="_blank">맥 사용자들의 ssh를 활용한 인스턴스 접속

<h4>1. AWS 인스턴스 환경설정</h4>

<p>&nbsp;가장 먼저 AWS에 로그인을 해야겠죠? 로그인을 하시고, 왼쪽 상단에 service라는 탭이 있습니다. 그 중 EC2라는 탭을 선택합니다.</p>
<img src="https://dl.dropbox.com/s/tqn7c89kxlzt4gz/aws_start.png">
<p>&nbsp;그럼 다음과 같은 화면이 나오는데, Launch Instance로 인스턴스를 생성합니다.</p>
<img src="https://dl.dropbox.com/s/1iik9ht3o667azy/aws2.png">
<p>&nbsp;다음으로 리눅스 종류를 선택하라고 하는데, Amazon Linux를 선택합니다. 참고로, Ubuntu같은 리눅스 배포판을 아시는 분들도 있으실텐데요. 어떤 것으로 만들어도 큰 차이는 없습니다. 다만 Amazon Linux의 경우 <code>yum</code>이라는 명령어로 패키지(프로그램)를 설치하고, Ubuntu같은 경우에는 <code>apt-get</code> 명령어로 패키지를 설치합니다. 여기서는 yum을 사용하여 패키지를 설치하므로, ubuntu를 통해 설치하는 분들은 yum을 apt-get으로 바꿔서 설치를 진행하시면 됩니다.</p>
<p>&nbsp;리눅스 배포판 선택 이외에 나머지 설정은 그대로 두시면 됩니다. 인스턴스 생성을 완료하면 다음과 같은 화면이 나옵니다.</p>
<img src="https://dl.dropbox.com/s/uhyolr588tbn2vj/aws3.png">
<p>&nbsp;여기서 launch-wizard-7을 클릭하시면 Security Groups탭으로 넘어가게 됩니다. 그리고 아래 Inbound에서 edit을 클릭하여 설정을 아래와 같이 변경합니다.</p>
<img src="https://dl.dropbox.com/s/22qrr7dklxmk3ec/aws4.png">
<p>&nbsp;이는 인스턴스에 특정 port를 열어주는 것인데, http로 되어 있는 80번 포트는 production 모드를 위한 것이고, 3000번 포트는 development 모드용입니다.</p>


<h4>2. Ruby, Rails, Passenger gem 설치</h4>

<p>&nbsp;이 다음으로 인스턴스를 실행하는 방법은 위에 소개한 putty를 이용하거나, ssh를 이용하여 인스턴스에 접속하면 됩니다. 접속에 성공하였다면, login-as:에 <code>ec2-user</code>를 입력하면 다음과 같이 출력됩니다.</p>
<img src="https://dl.dropbox.com/s/m8e2xwkq9ugx167/ec2.png">
<p>&nbsp;이제 Ruby, Rails, passenger를 순차적으로 설치해보도록 하겠습니다. Ruby와 Rails 설치 방법은 몇 가지가 있는데, 그 중 RVM(Ruby Version Manager)을 이용한 방법이 가장 쉽고, 무난한 방법입니다. RVM은 <a href="https://rvm.io/">https://rvm.io</a>에서 설치할 수 있습니다. 해당 사이트에 접속하여 스크롤을 조금 내리면 <code>installation documentation</code>이라는 탭이 있습니다.</p>
<img src="https://dl.dropbox.com/s/rtw4koeruvx14px/ec22.png">
<p>&nbsp;들어가보면, RVM 설치 옵션에 Ruby나 Rails를 같이 설치할 수 있는 항목이 있습니다. 그 중 위의 두 명령어만 입력합니다.</p>
<img src="https://dl.dropbox.com/s/g6xqcivjfk26xj1/ec23.png">

<p>&nbsp;아래 명령어를 입력하면 다음과 같은 화면이 나옵니다. Warning~~라고 나오는데, 해당 명령어도 써줍니다.</p>
<img src="https://dl.dropbox.com/s/6gsbtekhl8b9i62/image1.png">
```shell
source ~/.profile
```

<p>&nbsp;이렇게 하면 RVM 설치가 완료되는데 RVM이 잘 설치되었는지 확인할 필요가 있습니다.</p>
```shell
rvm -v
```

<img src="https://dl.dropbox.com/s/4whx5upbrz7kbv8/ec24.png">
<p>&nbsp;다음과 같이 출력되면, 설치가 잘 된 것입니다. 이제 다음과 같은 명령어로 Ruby와 Rails를 설치합니다.</p>

```shell
rvm install ruby-2.2.1(내 프로젝트에 맞는 ruby 버전 입력)
gem install rails -v 4.2.4(내 프로젝트에 맞는 rails 버전 입력)
```

<p>&nbsp;이렇게 굳이 Ruby와 Rails의 버전을 자신의 프로젝트와 일치시켜 주는 이유는 설치된 패키지와 자신의 프로젝트의 패키지간의 충돌이 일어날 수 있기 때문입니다. 충돌이 일어나면 RVM을 통해 버전을 관리할 수 있지만, 디버깅이 좀 필요합니다.(사실 저는 처음 이 작업을 할 떄, 이 문제 때문에 하루종일 인스턴스를 10번정도 만들었다 지운 적이 있습니다. 이런저런 rvm 명령어를 써야하는 작업이니, 기존 프로젝트와 버전을 맞춰서 Ruby와 Rails를 설치할 것을 권장합니다.)</p>
<p>&nbsp;어쨌든 설치가 완료되면, Ruby와 Rails 버전을 체크합니다.</p>

```shell
ruby -v
rails -v
```

<img src="https://dl.dropbox.com/s/daiqp59rvhgxkmh/ec25.PNG">
<p>&nbsp;저같은 경우 Ruby는 2.2.1버전을, Rails는 4.2.4 버전을 설치했기 때문에 위와 같이 나옵니다.</p>
<p>&nbsp;여기까지가 Ruby, Rails 설치 과정입니다. 이제 프로젝트에 <code>passenger</code> gem을 설치할 차례입니다. 먼저 git으로 프로젝트를 clone한 후(다운 받은 후) passenger를 설치해야 하는데, git이 설치되어 있지 않았을 겁니다. 그래서</p>

```shell
sudo yum install git-all
git clone https://github.com/hcn1519/myproject.git(자신의 프로젝트 url)
```

<p>&nbsp;이렇게 하면 github에 올려놓았던 프로젝트가 인스턴스에 넘어옵니다. 프로젝트 clone이 완료되면 해당 프로젝트에 들어 가서 <code>passenger</code> gem을 설치합니다.</p>

```ruby
cd myproject
gem install passenger
```

<p>&nbsp;새로운 프로젝트를 만들면 gem들이 제대로 설치되지 않았을 겁니다. 그러므로 기존 프로젝트의 gem을 한 번 더 설치해주고, 마이그레이션도 해줍니다.</p>

```ruby
bundle install
rake db:migrate
```

<p>&nbsp;이렇게하면 다음과 같은 에러가 뜨는데, nodejs가 설치되어 있지 않기 때문에 나오는 오류입니다. 그러므로 nodejs를 설치해주어야 하는데요.</p>

```
rake aborted!
Bundler::GemRequireError: There was an error while trying to load the gem 'uglifier'.
/home/ec2-user/.rvm/gems/ruby-2.2.1/gems/bundler-1.11.2/lib/bundler/runtime.rb:80:in `rescue in block (2 levels) in require'
/home/ec2-user/.rvm/gems/ruby-2.2.1/gems/bundler-1.11.2/lib/bundler/runtime.rb:76:in `block (2 levels) in require'
/home/ec2-user/.rvm/gems/ruby-2.2.1/gems/bundler-1.11.2/lib/bundler/runtime.rb:72:in `each'
/home/ec2-user/.rvm/gems/ruby-2.2.1/gems/bundler-1.11.2/lib/bundler/runtime.rb:72:in `block in require'
/home/ec2-user/.rvm/gems/ruby-2.2.1/gems/bundler-1.11.2/lib/bundler/runtime.rb:61:in `each'
/home/ec2-user/.rvm/gems/ruby-2.2.1/gems/bundler-1.11.2/lib/bundler/runtime.rb:61:in `require'
/home/ec2-user/.rvm/gems/ruby-2.2.1/gems/bundler-1.11.2/lib/bundler.rb:99:in `require'
/home/ec2-user/myproject/config/application.rb:7:in `<top (required)>'
```

<p>&nbsp;간단한 디버깅으로 nodejs를 설치해줍니다.</p>

```shell
sudo yum install nodejs npm --enablerepo=epel
```

<p>&nbsp;그리고 다시 rake db:migrate해주시면 정상 작동하는 것을 보실 수 있습니다.</p>

<img src="https://dl.dropbox.com/s/wg6kaomlnpw4qqd/image2.png">

<p>&nbsp;여기까지 완료하면 Nginx 이외의 환경설정은 완료한 것입니다.</p>

<h4>3. Nginx 설치</h4>


<p>&nbsp;이제 Nginx를 설치할 차례입니다. Nginx는 리눅스의 관리자인 <code>root</code> 사용자를 통해서 설치할 수 있습니다. 그러므로 기존 <code>ec2-user</code>로 설정되어 있는 사용자를 root로 변경해야 합니다.</p>

```shell
sudo passwd
```

<p>&nbsp;먼저 <code>root</code>사용자의 비밀번호를 설정합니다. 저는 간단하게 password로 설정했습니다. 다음으로,</p>

```shell
su
```

<p>&nbsp;다음과 같이 입력하고 방금 설정한 비밀번호를 입력하면<code>ec2-user</code>로 되어 있던 사용자가 <code>root</code>로 변경됩니다.</p>

<img src="https://dl.dropbox.com/s/m9ipotplov23lxq/image4.png">

<p>&nbsp;이제 Nginx를 설치하면 됩니다.</p>

```shell
passenger-install-nginx-module
```

<img src="https://dl.dropbox.com/s/oarbbuxe9oebkfk/image5.png">
<p>&nbsp;처음에 이런 화면이 나올텐데, 사뿐히 Enter를 눌러주시고, 다음으로 ruby를 선택해줍니다.</p>

<img src="https://dl.dropbox.com/s/7jsuje62zdo77o2/image6.png">

<p>&nbsp;그리고 다음과 같은 경고문구가 나옵니다.</p>

<img src="https://dl.dropbox.com/s/8bo18qb0ahxn7ms/image7.png">

<p>&nbsp;내용을 읽어보시면 아시겠지만, 보안상의 문제로 Nginx가 특정 폴더에 접근할 수 없다고 합니다. 그러니 진행되던 설치를 종료하고, 해당 명령어를 입력하고 다시 설치를 해줍니다.</p>

```shell
ctrl + c
sudo chmod o+x "/home/ec2-user"
passenger-install-nginx-module
```

<p>&nbsp;다시 설치를 실행하면, 다음과 같은 새로운 오류창이 나옵니다.</p>

<img src="https://dl.dropbox.com/s/kqaragj89gnjbv3/image8.png">

<p>&nbsp;읽어보시면, curl과 관련된 소프트웨어가 설치가 안 되었다는 것을 알 수 있습니다. 설치 과정을 종료하고(ctrl + c), 해당 소프트웨어를 설치해줍니다.</p>

```shell
sudo yum install libcurl-devel.x86_64
passenger-install-nginx-module
```

<p>&nbsp;다시 설치를 시작하면, 이번에는 다음과 같은 경고가 나옵니다.</p>

<img src="https://dl.dropbox.com/s/93jq7fo0gujk4q4/image9.png">

<p>&nbsp;내용을 보면, Phusion Passenger는 최소 1GB의 메모리가 필요한데, 네 가상메모리는 995MB(10MB 부족..)라서 메모리가 부족하다는 내용입니다. 그래서 다음과 같은 명령어를 실행해라라는 얘기인데, 쿨하게 따라 해줍니다.</p>

```shell
sudo dd if=/dev/zero of=/swap bs=1M count=1024
sudo mkswap /swap
sudo swapon /swap
passenger-install-nginx-module
```

<p>&nbsp;그리고 다시 Nginx 설치를 하면, 이렇게 Nginx 설치 옵션과 관련하여 우리에게 질문을 합니다. 1번을 선택하고 진행합니다.</p>

<img src="https://dl.dropbox.com/s/3xyuyr7i3udqrry/image10.png">

<p>&nbsp;다음으로 한 번 더 파일을 어디다가 저장하겠냐고 다음과 같이 질문하는데 그냥 enter를 누릅니다.</p>

<img src="https://dl.dropbox.com/s/hxd5ktkiy7xbyw4/image11.png">
<p>&nbsp;그럼 이제 더 이상 질문 없이 Nginx가 설치됩니다.</p>


<img src="https://dl.dropbox.com/s/wtvqbwu5qd1ehnc/image12.png">

<p>&nbsp;설치가 완료되면 <code>root</code>사용자에서 빠져나옵니다.</p>

```shell
exit
```


<h4>4. Nginx 기본 셋팅</h4>

<p>&nbsp;이제 드디어 Nginx를 셋팅할 차례입니다. Nginx와 관련해서 이런저런 글들을 보면서 Passenger와 Nginx에 대하여 조금은 설명하고 설정에 대해 서술하려고 했으나, 이게 짧지가 않다보니 여기다가 설명내용을 추가하면 글이 너무 길어질 것 같아서, Passenger와 Nginx와 관련된 보다 자세한 내용은 다음 글에서 쓰겠습니다. 여기서는 그것보다 바로 셋팅해서 Nginx를 사용해서 ip address를 실제 서버에 올리는 작업을 해보도록 하겠습니다.</p>
<p>&nbsp;Nginx 설치과정에서 특별한 설정을 하지 않았다면(설치시 enter만 눌렀다면), Nginx 파일들은 <code>/opt/nginx/</code> 안에 있습니다. 그 중 Nginx 환경설정(configuration) 파일은 <code>/opt/nginx/conf/nginx.conf</code> 안에 있습니다. 그리고 서버 설정을 위해서는 해당 파일에 들어가서 추가적인 내용을 써줘야 합니다.</p>

```shell
sudo vi /opt/nginx/conf/nginx.conf
```

<p>&nbsp;해당 파일에 들어가면 어떤 것은 #으로 주석처리 되어 있고, 아닌 것도 있습니다. 이건 rails에서 여러가지 파일(class)에 들어가면 다양한 옵션들을 간단히 주석을 해제하여 쓸 수 있도록 해주는 것과 마찬가지의 것들입니다. 여기서 눈여겨 보아야 하는 설정은 http와 server입니다.</p>
<p>&nbsp;기본 서버 설정은 다음과 같이 하면 됩니다.</p>

{% highlight nginx %}
http {
  server {
    listen 80;
    root /home/ec2-user/myproject/public;
    passenger_enabled on;
  }
}
{% endhighlight %}

<p>&nbsp;즉, 37번 째 줄에 새로운 <code>server{}</code>블록을 만들고 해당 내용을 추가하면 됩니다. <code>root</code>에 쓴 경로의 경우, public폴더에 들어가서 pwd 명령어를 치면 나오는 경로를 그대로 적어 넣으면 됩니다.</p>
<p>&nbsp;이렇게 설정하고 해당 파일을 저장하고 나오면 가장 기본적인 Nginx 셋팅은 끝났습니다. 이제 서버를 키고 꺼봐야겠죠? 해당 설정에서 서버를 키고 끄는 명령어는 다음과 같습니다.</p>

```
sudo /opt/nginx/sbin/nginx
sudo fuser -k 80/tcp
```
<p>&nbsp;첫 번째 명령어는 서버를 키는 명령어이고, 두 번째 명령어는 서버를 끄는 명령어입니다. 간단히 생각해서 <code>rails s</code>와 <code>ctrl + c</code>의 명령어라고 생각하시면 됩니다. 그런데 Production 모드에서는 서버를 무조건 껐다가 켜야 새롭게 설정한 내용들이 적용됩니다. 그래서, 서버를 자주 켰다가 꺼야하기 때문에 명령어가 좀 더 직관적이고 쉬우면(start, stop, restart, reload) 좋습니다.</p>

```shell
sudo service nginx stop
sudo service nginx start
sudo service nginx restart
sudo service nginx reload
```

<p>&nbsp;위와 같은 명령어로 서버를 켰다 껐다를 할 수 있습니다. 하지만 해당 명령어를 입력해보면, 아마 <code>command not found</code>와 같은 명령어가 나올 겁니다. 이를 해결하기 위해서 간단한 설정을 해주어야 하는데, Amazon Linux(Redhat 계열)와 Ubuntu(Debian 계열)에서 이를 설정하는 방법이 다릅니다.</p>

<h5>1) Amazon Linux(ec2-user) 설정</h5>
<p>&nbsp;아래 명령어로 파일을 열고,</p>
```shell
sudo vi /etc/rc.d/init.d/nginx
```
<p>&nbsp;기존 내용은 모두 지우고, 아래 내용을 붙여넣으면 됩니다.</p>

```shell
#!/bin/sh
. /etc/rc.d/init.d/functions
. /etc/sysconfig/network
[ "$NETWORKING" = "no" ] && exit 0

nginx="/opt/nginx/sbin/nginx"
prog=$(basename $nginx)

NGINX_CONF_FILE="/opt/nginx/conf/nginx.conf"

lockfile=/var/lock/subsys/nginx

start() {
    [ -x $nginx ] || exit 5
    [ -f $NGINX_CONF_FILE ] || exit 6
    echo -n $"Starting $prog: "
    daemon $nginx -c $NGINX_CONF_FILE
    retval=$?
    echo
    [ $retval -eq 0 ] && touch $lockfile
    return $retval
}

stop() {
    echo -n $"Stopping $prog: "
    killproc $prog -QUIT
    retval=$?
    echo
    [ $retval -eq 0 ] && rm -f $lockfile
    return $retval
}

restart() {
    configtest || return $?
    stop
    start
}

reload() {
    configtest || return $?
    echo -n $”Reloading $prog: ”
    killproc $nginx -HUP
    RETVAL=$?
    echo
}

force_reload() {
    restart
}

configtest() {
    $nginx -t -c $NGINX_CONF_FILE
}

rh_status() {
    status $prog
}

rh_status_q() {
    rh_status >/dev/null 2>&1
}

case "$1" in
start)
rh_status_q && exit 0
$1
;;
stop)
rh_status_q || exit 0
$1
;;
restart|configtest)
$1
;;
reload)
rh_status_q || exit 7
$1
;;
force-reload)
force_reload
;;
status)
rh_status
;;
condrestart|try-restart)
rh_status_q || exit 0
;;
*)
echo $"Usage: $0 {start|stop|status|restart|condrestart|try-restart|reload|force-reload|configtest}"
exit 2
esac
```

<p>&nbsp;그리고 아래 명령어를 치면 정상 작동합니다.</p>
```shell
sudo chmod +x /etc/rc.d/init.d/nginx
```

<img src="https://dl.dropbox.com/s/d8o4rzvl97w3t67/image13.png">
<img src="https://dl.dropbox.com/s/tfjmia4dkhidtlt/image14.png">

<p>&nbsp;저의 경우 root 페이지를 설정해놓지 않아서 다음과 같은 페이지가 나왔습니다. root 페이지를 설정해주시면, 올바르게 페이지가 나옵니다.</p>
<h5>2) Ubuntu 설정</h5>

```shell
wget -O init-deb.sh http://library.linode.com/assets/660-init-deb.sh
sudo mv init-deb.sh /etc/init.d/nginx
sudo chmod +x /etc/init.d/nginx
sudo /usr/sbin/update-rc.d -f nginx defaults
```

<p>&nbsp;여기까지 해서 Nginx 기본 셋팅에 대해 알아보았습니다.</p>

<h4>5. 앱을 조금 더 빠르게 만드는 Nginx 셋팅</h4>

<p>&nbsp;Nginx 기본 셋팅 내용이 Nginx 실행과 관련된 내용이었다면, 이 부분은 Nginx 속도 개선과 관련된 내용입니다. 우리가 만든 앱의 속도는 앱 자체의 성능(rails 코드)와도 관련이 있지만, 서버에서의 처리와도 관련이 깊습니다. 여기서는 Nginx의 속도를 높일 수 있는 몇 가지 설정에 대해 알아보도록 하겠습니다.</p>



<h5>1) gzip 압축 설정</h5>

<p>&nbsp;gzip은 .gz 확장자로 파일을 압축하여 서버에서 파일 전송을 줄여주는 역할을 하는 설정입니다. 즉, 메일로 파일을 보낸다고 했을 때, 1000개의 파일을 각각 보내는 것보다 1개의 압축 파일을 보내는 것이 빠른 것처럼, gzip 설정은 서버에서 파일을 압축하여 속도를 개선하는 것입니다.</p>

{% highlight nginx %}
server{
  #gzip 설정 적용
  gzip  on;

  #압축 수준(1부터 9까지)
  gzip_comp_level  6;

  #모든 파일을 압축하는 것이 아니라, 크기가 좀 있는 파일만 압축하도록 만듦
  gzip_min_length  1000;

  #프록시 서버를 통해 접속하는 사용자에 대한 gzip 설정
  gzip_proxied     any;

  #압축할 파일 확장자 설정
  gzip_types  text/plain text/css application/x-javascript application/json text/javascript text/xml text/css application/xml image/png image/jpeg image/jpg image/gif;
}
{% endhighlight %}

<h5>2) buffer와 파일 전송 한계량 설정</h5>

<p>&nbsp;이 설정은 컴퓨터의 메모리같은 역할을 하는 buffer에 대한 설정과 파일 전송량 한계 설정에 대한 설정입니다.</p>

{% highlight nginx %}
#body와 header의 버퍼 크기 설정
client_body_buffer_size 10K;
client_header_buffer_size 1k;

#파일 전송 한계 설정(8m은 8mb까지 허용)
client_max_body_size 8m;

large_client_header_buffers 2 1k;
{% endhighlight %}


<h5>3) 로딩 지연시간의 한계 설정</h5>

<p>&nbsp;이 설정은 페이지 로딩이 일정시간 넘어가면 서버와의 연결을 끊도록 하는 설정입니다. 오류가 있어서 안되는 것들을 쳐내고? 되는 클라이언트만 다뤄서 속도 개선을 하는 설정입니다.</p>

{% highlight nginx %}
client_body_timeout 12;
client_header_timeout 12;
send_timeout 10;
{% endhighlight %}

<h5>4) 특별한 변화가 없는 파일들 유지하기</h5>

<p>&nbsp;이 설정은 이미지 파일이나, css, js 파일 같이 특별한 변화가 많이 없는 파일들의 캐시 만료 기간을 설정하여 다음 번 접속시 로딩 속도를 높이는 방법입니다.</p>

{% highlight nginx %}
location ~* .(jpg|jpeg|png|gif|ico|css|js)$ {
  expires 365d;
  access_log off;
}
{% endhighlight %}

<p>&nbsp;최종적인 파일은 다음과 같습니다.</p>

{% highlight nginx %}
worker_processes  1;

events {
  worker_connections  1024;
}

http {
  passenger_root /home/ubuntu/.rvm/gems/ruby-2.2.1/gems/passenger-5.0.24;
  passenger_ruby /home/ubuntu/.rvm/gems/ruby-2.2.1/wrappers/ruby;

  include       mime.types;
  default_type  application/octet-stream;

  #access_log  logs/access.log  main;
  sendfile        on;
  keepalive_timeout 65;

  server {
    listen 80;
    passenger_enabled on;
    root /home/ec2-user/myproject/public;

    client_max_body_size 8M;
    client_body_buffer_size 10K;
    client_header_buffer_size 1k;
    large_client_header_buffers 2 1k;

    client_body_timeout 12;
    client_header_timeout 12;
    send_timeout 10;

    gzip on;
    gzip_http_version 1.1;
    gzip_vary on;
    gzip_comp_level 6;
    gzip_proxied any;
    gzip_types text/plain text/html text/css application/json application/javascript application/x-javascript text/    javascript image/x-icon image/png image/jpeg image/jpg image/gif;

    location ~* .(jpg|jpeg|png|gif|ico|css|js)$ {
      expires 365d;
      access_log off;
    }
  }
}
{% endhighlight %}

<h5>더 볼만한 추가 자료</h5>

<ul>
  <li><a href="https://www.phusionpassenger.com/library/walkthroughs/basics/ruby/" target="_blank">Passenger 이해하기</a></li>
  <li><a href="http://nginx.org/en/docs/beginners_guide.html" target="_blank">Nginx 기본 가이드</a></li>
  <li><a href="https://www.digitalocean.com/community/tutorials/how-to-deploy-rails-apps-using-passenger-with-nginx-on-centos-6-5" target="_blank">Passenger와 아마존 리눅스(Redhat 계열) 셋팅</a></li>
  <li><a href="http://edapx.com/2012/10/28/nginx-passenger-rvm-and-multiple-virtual-hosts/" target="_blank">Passenger와 우분투 셋팅</a></li>
  <li><a href="https://www.digitalocean.com/community/tutorials/how-to-optimize-nginx-configuration" target="_blank">Nginx 속도 개선 관련 Doc1</a></li>
  <li><a href="http://www.revsys.com/12days/nginx-tuning/" target="_blank">Nginx 속도 개선 관련 Doc2</a></li>
</ul>
