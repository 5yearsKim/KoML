
# 섹션 태그 

## xml 시작

KoML은 xml 로 작성되어 있어요. xml 이 생소하다면 [여기](https://kylog.tistory.com/41)를 참고해주세요!<br>
xml 확장자의 파일을 만들고 모든 koml 문서의 시작 부분에 다음과 같은 코드를 작성해주세요. 이 문서가 xml 형식이고 한글 인코딩을 사용한다는 의미에요.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xml>
<koml>
  ... <!-- <case> 들을 여기 적어주세요! -->
</koml>
```
xml 문서에서는 <koml> 처럼 태그를 열고 </koml>처럼 태그를 닫아주어야 해요. 

<br>

## \<case\>
내가 챗봇이 이해했으면 하는 패턴들과 답변 템플릿을 case 태그 안에 적어주세요.
\<case\> 안에는 필수적으로 \<pattern\> 과 \<template\>이 포함되어야 해요.

```xml
<case>
  <pattern>살쪘어</pattern>
  <template>누가 살쪄!</template>
</case>
```
```
<< 살쪘어
>> 누가 살쪄!
```

<br/>

## \<pattern\>
<br/>

### 나열

\<pattern> 에는 하나의 패턴 뿐만 아니라 여러가지 패턴을 적을 수 있어요. 
```xml
<case>
  <pattern>
    <li>졸리다</li>
    <li>잠온다</li>
  </pattern>
  <template>졸리면 자라</template>
</case>
```

```
<< 졸리다
>> 졸리면 자라
<< 잠온다
>> 졸리면 자라
```

### 와일드카드(*)
어떤 말이 나와도 매치가 되게끔 하고 싶으면 와일드카드(*)를 사용할 수 있어요.
```xml
<case>
  <pattern>국힙 원탑은 *</pattern>
  <template>원탑은 싸이 아님?</template>
</case>
```
```
<< 국힙 원탑은 빈지노
>> 원탑은 싸이 아님?
<< 국힙 원탑은 타블로
>> 원탑은 싸이 아님?
```

<br/>

### 품사 와일드카드(_)
특정 품사의 포함 여부에 관계없이 패턴을 매치시키고 싶으면 품사 와일드카드(_)를 사용할 수 있어요.<br>
품사 와일드카드의 종류는 다음과 같아요.
```
*** 조사
_j: 조사 전체
_jks: 주격 조사
_jkc: 보격 조사
_jkg: 관형격 조사
_jko: 목적격 조사
_jkb: 부사격 조사
_jkv: 호격 조사
_jkq: 인용격 조사
_jx: 보조사

*** 어미 
_e: 어말 어미
_ef: 종결 어미
_ec: 연결 어미

*** 부사
_m: 부사 전체
_mm: 관형사
_mag: 일반 부사
_maj: 접속 부사

**** 부호 및 외국어
_s: 부호 전체
_sf: 마침표, 물음표, 느낌표
_sn: 숫자
```

품사 와일드카드는 다음과 같이 사용할 수 있어요.

```xml
<case>
  <pattern>너_j 꿈_j 뭐_e</pattern>
  <template>해적왕</template>
</case>
```
```
<< 너 꿈 뭐야
>> 해적왕
<< 너 꿈 뭐니
>> 해적왕
<< 너 꿈이 뭐니
>> 해적왕
<< 너는 꿈이 뭐니
>> 해적왕
```

> **_NOTE:_**  조사 와일드카드(_)는  와일드카드(*) 뒤에 사용될 수 없어요. 예를들어 *_j 같은 표현은 허용되지 않아요.

<br/>

## \<template\>

\<template> 에서는 조사 해결, 랜덤 선택, 로직에 따라 답변 선택 등 다양한 기능을  지원해요. <br> 기능에 관한 자세한 설명은 **템플릿** 섹션을 참고해주세요! 

<br/>


## \<follow>

질문에 바로 답하는 것 뿐만 아니라 앞선 문맥에 대화가 이어지게끔 할 수도 있어요. follow 태그를 이용하면 앞선 답변의 패턴이 일치하는 경우에만 답변을 해요. 

```xml
<case>
  <!-- follow 안에는 패턴을 적어넣을 수 있어요 -->
  <follow>*해적왕*</follow>
  <pattern>왜_sf</pattern>
  <template>샹크스랑 약속했거든</template>
</case>
```

```
<< 너 꿈이 뭐야
>> 해적왕
<< 왜?
>> 샹크스랑 약속했거든
<< 왜?
>> None
```

> **_NOTE:_**  \<pattern>과 마찬가지로 \<follow> 도 \<li>를 통해서 복수의 패턴을 입력할 수 있어요.


<br>

\<follow> 에는 패턴 뿐만 아니라 다른 \<case> 의 id 도 넣을 수 있어요. \<case> 에 id 를 할당하고 \<follow> 에 cid 에 \<case>의 id 를 넣어주면 돼요.
```xml
<case id='good_singer'>
  <pattern>너_j 노래 잘해_s</pattern>
  <template>기가 막히지</template>
</case>

<case>
  <follow cid='good_singer'/>
  <pattern>
    <li>*해봐*</li>
    <li>*불러봐*</li>
  </pattern>
  <template>언더에선 안부름ㅎ</template>
</case>
```

```
<< 너 노래 잘해?
>> 기가 막히지
<< 불러봐
>> 언더에선 안부름ㅎ
<< 불러봐
>> None
```

> **_NOTE:_**   복수의 id를 cid를 넣고 싶으면 `cid = "id_1, id_2"` 이런 식으로 csv 형식으로 넣어주면 돼요.


