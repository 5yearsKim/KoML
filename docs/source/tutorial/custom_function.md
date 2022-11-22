
# 커스텀 함수

당신이 파이썬을 다룰 수 있다면 KoML을 이용해서 굉장히 재미있는 것을 해볼 수 있어요. 예를들어, 지금 시각을 알려주는 예시를 생각해볼게요. 

```
<< 지금 몇시야?
>> 음.. 지금 오후 8시 36분!
```

지금 시각은 정해져 있는 값이 아니기 때문에 \<template> 에 미리 입력해서 답변을 내놓기 어려워요. 이럴 때 \<func> 태그를 활용할 수 있어요.

<br>

## \<func>

\<func> 태그를 이용하기 위해서는 먼저 파이썬 함수를 정의해줘야해요. 지금 시각을 알려주는 함수를 간단히 작성해볼게요.

```python
def show_date(context=None):
    import time
    tick = time.localtime()
    h, m = tick.tm_hour, tick.tm_min

    if h > 12:
        h -= 12
        am_pm = '오후'
    else:
        am_pm = '오전'
    return f'{am_pm} {h}시 {m}분'
```
>**NOTE** 모든 KoML함수의 마지막 parameter는 context 가 주어져야 해요. context는 KoML 의 전반적인 동작(앞 뒤 문맥, 단어 기억 등)에 중요한 역할을 한답니다.

<br>

koml 파일은 다음과 같이 작성해주세요.
```xml
<!-- custom_function.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xml>
<koml>
  <case>
    <pattern>지금 몇시야_sf</pattern>
    <template>음.. 지금 <func name='show_date'/>!</template>
  </case>
</koml>
```
<br>

이후 KomlBot 을 동작시킬 때 이 함수를 사용할거라는 것을 알려주어야 해요. `CustomBag`을 사용해서 함수를 전달할 수 있어요.
```python
from koml import KomlBot, CustomBag

bag = CustomBag(funcs={'show_date': show_date}) 

bot = KomlBot(bag)
bot.learn(['custom_function.xml'])
bot.converse()
```
>**NOTE** \<func> 태그에 name 에는 CustomBag 에 넣어준 key 값이 들어가야 해요.

<br>

다음과 같은 결과를 확인할 수 있어요.
<br>

```
<< 지금 몇시야?
>> 음.. 지금 오후 8시 36분!
```

<br>
<br>

## \<arg>
\<func> 에는 인자가 들어갈 수 있어요. \<arg>감싸서 필요한 인자를 \<func>태그 안에 넣어주세요. <br>
\<func>과 \<arg> 를 이용하면 이런 기능을 구현해볼 수 있어요.

```
<< 내 이름 뭔지 알아?
>> 아니.. 뭔데?
<< 어니언이야
>> 아 오키ㅋㅋ 이제 기억할게! 
<< 내 이름 뭔지 알아?
>> 응ㅋㅋ 알지
<< 뭔데?
>> 어니언이잖아ㅋㅋ 날 뭘로 보고
```

<br>

KomlBot 이 \<set>을 통해 특정 키워드를 알고 있는지 여부를 판단하는 함수를 다음과 같이 작성할 수 있어요.

```python
def know(key: str, context= None) -> str:
    if key in context.memo:
        return 'true'
    else:
        return 'false'
```
<br>
koml 파일에 다음 케이스들을 추가해주세요.

```xml
<case id = 'know_username'>
  <pattern>* 내 이름_j 뭔지 알아_s</pattern>
  <template>
    <switch>
      <!-- 'username' 을 아는지 여부를 pivot 으로 제공 -->
      <pivot><func name='know'><arg>username</arg></func></pivot>
      <scase pivot='true'>응ㅋㅋ 알지</scase>
      <default>아니.. 뭔데?</default>
    </switch>
  </template>
</case>

<!-- 이름을 아는 경우 -->
<case>
  <follow cid='know_username'>응 *</follow>
  <pattern>
    <li>* 뭔데_s</li>
    <li>뭐야_s</li>
  </pattern>
  <template><get key='username'/>_ix잖아ㅋㅋ 날 뭘로 보고</template>
</case>

<!-- 이름을 모르는 경우 -->
<case>
  <follow cid='know_username'>아니 *</follow>
  <pattern>
    <li>내 이름은 <blank pos='N'/></li>
    <li><blank pos='N'/></li>
  </pattern>
  <template>아 오키ㅋㅋ 이제 기억할게! <think><set key='username'><blank/></set></think></template>
</case>
```

<br>

마찬가지로 KomlBot 을 실행할 때 CustomBag 에 정의한 함수를 넣어서 실행해주세요.

```python
from koml import KomlBot, CustomBag

bag = CustomBag(funcs={'know': know})

bot = KomlBot(bag)
bot.learn(['custom_function.xml'])
bot.converse()
```
<br>

다음과 같은 결과를 확인할 수 있어요.

```
<< 너 내 이름이 뭔지 알아?
>> 아니.. 뭔데?
<< 홍길동
>> 아 오키ㅋㅋ 이제 기억할게! 
<< 너 내 이름 뭔지 알아?
>> 응ㅋㅋ 알지
<< 뭐야
>> 홍길동이잖아ㅋㅋ 날 뭘로 보고
```
