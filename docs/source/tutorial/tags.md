# 응용 태그

## \<blank>

\<blank>를 사용하면 유저의 답변 중 특정 부분을 \<pattern> 에서 캐치해서 \<template>에서 활용할 수 있어요. 

```xml
<case>
  <pattern>내 이름은 <blank/></pattern>
  <template>안녕 <blank/>! 만나서 반가워ㅋㅋ</template>
</case>
```
```
<< 내 이름은 피카츄 
>> 안녕 피카츄! 만나서 반가워ㅋㅋ
```

<br>

그런데 blank 에 원하는 내가 필요한 말 이외에 다른 말이 포함되어 있을 수 있어요.

```
<< 내 이름은 피카츄입니다
>> 안녕 피카츄입니다! 만나서 반가워ㅋㅋ
```

<br>

이럴 때는 \<blank> 에 `pos` 를 사용해서 원하는 특정 품사만 가져올 수 있어요. 

```xml
<case>
  <!-- 명사만 가져오기 -->
  <pattern>내 이름은 <blank pos='N'/></pattern> 
  <template>안녕 <blank/>! 만나서 반가워ㅋㅋ</template>
</case>
```

```
<< 내 이름은 피카츄입니다
>> 안녕 피카츄! 만나서 반가워ㅋㅋ
```

> **_NOTE:_** 와일드카드(*)와 마찬가지로 조사 와일드카드(_)는 blank 뒤에 올 수 없어요. 
<br>
<br>
> **_NOTE:_** `pos` 뿐만 아니라 `npos`를 이용해 원하지 않는 품사를 필터링 할 수도 있어요. 
<br>
> **_NOTE:_** 여러개의 품사 태그를 제외/포함 시키고 싶다면 `npos="J,E"` 와 같이 csv 형식으로 입력해주면 돼요.


<br>

여러개의 \<blank\> 를 활용하고 싶을때는 `key` 또는 `idx`를 활용해서 가져오고 싶은 \<blank> 를 지정할 수 있어요.
```xml
<!-- idx 로 순서 배치 -->
<case>
  <pattern>너_j <blank pos='N'/> 좋아 <blank pos='N'/> 좋아_sf</pattern>
  <template>나는 <blank idx='2'/> 보다는 <blank idx='1'/> 좋은듯</template>
</case>

<!-- key 로 가져오기 -->
<case>
  <pattern>너_j <blank pos='N'/> 랑 <blank pos='N' key='target'/> 중 뭐_j 좋아_sf</pattern>
  <template>나는 <blank key='target'/>! </template>
</case>
```

```
<< 너는 치킨이 좋아 피자가 좋아?
>> 나는 피자 보다는 치킨 좋은듯
<< 너는 파이리랑 꼬부기중 뭐가 좋아?
>> 나는 꼬부기! 
```

> **NOTE:** idx 를 지정할 때에는 \<template>의 \<blank>에 idx 에 \<pattern> 에 \<blank> 의 순서를 넣어주면 돼요. 


<br>
<br>

## \<set>, \<get>
\<set>과 \<get> 을 이용하면 \<blank> 의 경우 처럼 \<template> 에서의 단어를 바로 답변에 사용하는것이 아니라 기억해두었다가 추후 답변에 활용할 수 있어요. 

```xml
<case>
  <pattern>내가 제일 좋아하는 음식은 <blank pos='N'/></pattern>
  <template>너 <set key='favorite_food'><blank/></set> 좋아하는구나.. 기억할게!</template>
</case>

<case>
  <pattern>* 제일 좋아하는 음식_j 뭔지 알아_sf</pattern>
  <template>알지. <get key='favorite_food'/>잖아ㅋㅋ</template>
</case>
```

```
<< 내가 제일 좋아하는 음식은 떡볶이야
>> 너 떡볶이 좋아하는구나.. 기억할게!
<< 졸리다
>> 졸리면 자라
<< 너 내가 제일 좋아하는 음식이 뭔지 알아?
>> 알지. 떡볶이잖아ㅋㅋ
```

>**NOTE:** \<set>과 \<get>에는 `key` 값이 꼭 필요해요.
<br>
>**NOTE:** \<get> 에 매치되는 key 값이 \<set>에서 설정되지 않았을 수 있어요. 이 경우는 \<func> 태그를 이용해서 key 값의 설정 여부에 따라 결과를 처리할 수 있어요. 이에 관해서는 **Custom Function** 항목을 참조해주세요!

<br>
<br>

## \<think>
\<think> 태그는 챗봇이 혼자 생각하게끔 하는 태그에요. 챗봇의 \<template> 내용이 노출되지 않게 할 때 유용해요.


```xml
<!-- think -->
<case>
  <pattern>내 취미는 <blank npos='J, EF'/></pattern>
  <!-- think 안에 있는 부분이 노출되지 않음 -->
  <template><think><set key='hobby'><blank/></set></think>안물안궁</template>
</case>

<case>
  <pattern>내 취미_j 뭐*</pattern>
  <template><get key='hobby'/>라매ㅋㅋ</template>
</case>
```

```
<< 내 취미는 농구하는거야
>> 안물안궁
<< 내 취미가 뭐라고?
>> 농구하는거라매ㅋㅋ
```



