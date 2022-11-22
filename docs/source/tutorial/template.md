
# 템플릿 태그 

## 조사 와일드카드
한국어의 특징 중 하나는 단어의 받침 여부에 따라 뒤에 붙는 조사가 달라진다는 거에요. (고기**를**~, 치킨**을**~) KoML에서는 조사 와일드카드를 이용해서 이를 해결할 수 있어요.
```
** 받침 O/받침 X **
_i: 이/가(I_GA)
_eun: 은/는(EUN_NEUN)
_gwa: 과/와(GWA_WA)
_eul: 을/를(EUL_REUL)
_a: 아/야(A_YA)
_euro: 으로/로(EURO_RO)
_ix: 이/x(I_X)
```

**사용 예시**

```xml
<case>
  <pattern><blank pos="N"/>먹으러 갈래?</pattern>
  <template>누가 <blank/>_eul 먹냐. 난 <blank/>_eun 별로ㅎ. </template>
</case>
```
```
<< 치킨 먹으러 갈래?
>> 누가 치킨을 먹냐. 난 치킨은 별로ㅎ. 
<< 피자 먹으러 갈래?
>> 누가 피자를 먹냐. 난 피자는 별로ㅎ. 
```

<br>
<br>

## \<random>
챗봇이 같은 질문에 똑같은 답변을 반복하면 재미 없겠죠? 하나의 케이스에 여러가지 답변을 다양하게 하려면 \<random> 태그를 활용할 수 있어요. 작성하고자 하는 템플릿을 \<ri> (random item의 약자)에 넣어주세요.

```xml
<case>
  <pattern>
    <li>안녕</li>
    <li>하이</li>
  </pattern>
  <template>
    <random>
      <ri>안녕~~~</ri>
      <ri>반가워!</ri>
      <ri>인사 잘한다</ri>
    </random>
  </template>
</case>
```

```
<< 안녕
>> 반가워!
<< 하이
>> 안녕~~~
<< 안녕
>> 안녕~~~
<< 하이
>> 인사 잘한다
```

<br>

\<random> 에서는 \<ri>의 가중치를 조정해 답변의 확률을 조정할 수도 있어요.


```xml
<case>
  <pattern>로또</pattern>
  <template>
    <random>
      <ri weight='3'>꽝</ri>
      <ri weight='1'>당첨!</ri>
    </random>
  </template>
</case>
```
```
>> 꽝
<< 로또
>> 꽝
<< 로또
>> 꽝
<< 로또
>> 당첨!
```
>**NOTE:** \<ri>의 weight 는 숫자만 입력할 수 있어요. 기본 weight 값은 1이에요.

<br>
<br>

## \<switch>

\<switch> 를 사용해서 조건에 따라 다른 답변을 내놓을 수 있어요. <br><br>
\<switch> 태그 안에는 3개의 필수 요소가 \<pivot>, \<scase>, \<default> 를 포함해야 돼요. \<pivot>에 기준이 되는 표현을 입력하고 \<scase> 에서 `pivot="ㅁㅁ"` 에 매치되는 답변을 적어주세요. 매치되지 않는 경우는 \<default>에서 처리해요.

```xml
<case>
  <!-- 형용사만 추출  -->
  <pattern>오늘 날씨가 <blank pos='VA'/></pattern>
  <template>
    <switch>
      <pivot><blank/></pivot>
      <scase pivot='좋'>커플들 다 뒤져라</scase>
      <scase pivot='나쁘'>놀러갈라 그랬는데 집에서 쉬어야겠네</scase>
      <scase pivot='흐리'>이거 또 미세먼지 아냐?</scase>
      <default>그렇네 날씨가 <blank/>네</default>
    </switch>
  </template>
</case>
```
```
<< 오늘 날씨가 좋다
>> 커플들 다 뒤져라
<< 오늘 날씨가 나쁘다
>> 놀러갈라 그랬는데 집에서 쉬어야겠네
<< 오늘 날씨가 흐리다
>> 이거 또 미세먼지 아냐?
<< 오늘 날씨가 춥다
>> 그렇네 날씨가 춥네
<< 오늘 날씨가 덥다
>> 그렇네 날씨가 덥네
```

<br>

>**NOTE** \<switch> 는 \<func> 태그와 조합하면 재밌고 다양한 기능을 구현할 수 있어요. \<func> 태그에 관해서는 **Custom Function** 을 참조해주세요!



