---
layout: post
comments: true
title:  "Oracle(SQL)에서 여러 개의 테이블 한 번에 drop하기"
excerpt: "SQL 명령어로 여러 개의 테이블을 한 번에 drop하는 방법에 대해 알아봅니다."
categories: Oracle Sql Language
date:   2016-11-27 00:30:00
tags: [SQL, Oracle, Language]
---

<p>&nbsp;먼저 본 내용은 다음 질문의 내용을 정리한 내용임을 밝힙니다.</p>

<a href="http://stackoverflow.com/questions/26968999/oracle-drop-multiple-table-in-a-single-query">
stackoverflow 질문 링크
</a>

<p>&nbsp;SQL을 사용할 때, 여러 개의 테이블을 일일이 DROP TABLE 명령어를 써가면서 튜플들을 지워나가는 것은 상당히 귀찮은 일입니다. 그래서 검색을 해보니 저와 비슷한 생각을 했던 사람들이 있더군요. 그래서 이번 포스팅에서는 여러 개의 테이블을 한 번에 DROP하는 방법을 알아봅니다.</p>

<p>&nbsp;첫 번째 방법은 다음 명령어를 SQL에 입력하면 됩니다.</p>

{% highlight sql %}
begin
for rec in (select table_name from user_tables
            where table_name like '%')
loop execute immediate 'drop table ' ||rec.table_name|| ' cascade constraint';
end loop;
end;
/
{% endhighlight %}

<img src="https://dl.dropbox.com/s/xwa3njepyxz6mev/drop%20multiple%20table.PNG">

<p>&nbsp;여기서 주의하실 점은 'loop execute ~' 이하의 문장은 '' 안에도 띄어쓰기를 정확히 쓰셔야 한다는 점입니다. 왜냐하면, 저 문장이</p>

{% highlight sql %}
drop table myTable cascade constraint;
{% endhighlight %}

<p>&nbsp;이 명령을 모든 user_tables에 대하여 반복적으로 실행하기 때문입니다.</p>

<p>&nbsp;두 번째 방법은 복붙입니다. 다음 명령어를 치게 되면 콘솔창에 현재 유저가 다룰 수 있는 테이블들의 DROP TABLE 명령어가 셋팅 됩니다. 그걸 복붙 하시면 됩니다.</p>

{% highlight sql %}
SELECT 'DROP TABLE ' || table_name || ' cascade constraint;' FROM user_tables;
{% endhighlight %}
