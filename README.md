# KoML

<br>

## Introduction 

[AIML](https://en.wikipedia.org/wiki/Artificial_Intelligence_Markup_Language)은 누구나 쉽게 챗봇을 만들 수 있게끔 도와주는 언어에요. AIML을 이용한 챗봇은 [Loebner Prize](https://en.wikipedia.org/wiki/Loebner_Prize) 등 세계적인 챗봇 대회에서 우승을 하기도 했고 딥러닝 기반의 챗봇이 널리 쓰이는 요즘도 Rule-based 처리를 할 때 널리 사용되고 있어요.
<br>
하지만 string match 기반의 AIML로 한국어를 처리하기에는 어려움이 있었어요. 한국어는 영어와 달리 하나의 의미를 전달하는데 여러가지 경우의 수가 나올 수 있어서요. 예를 들어 '너'가 '점심'에 '무슨음식'을 '먹었냐' 라고 물어보고 싶을 때 영어로는 이렇게 물어보는 경우만 존재하지만
```
What did you eat for lunch?
```

한국어로는 표현할 수 있는 가짓수가 너무 많아요.
```
너 점심 뭐 먹었어?
너 점심 뭐 먹었니?
너 점심 뭐를 먹었니?
너 점심에 뭐를 먹었니?
너는 점심에 뭐를 먹었니?
.
.
```

<br>

**KoML** 을 이용해서 챗봇을 만들면 이렇게 만들수 있어요.

```xml
<koml>
  <case>
    <pattern>너_j 점심_j 뭐_j 먹었_e?</pattern>
    <template>로봇이 밥을 왜먹음</template>
  </case>
<koml>
```
```
<< 너는 점심에 뭐 먹었니?
>> 로봇이 밥을 왜먹음
```

<br>

## Installation

```
pip install koml
```

<br>

## Test
```xml
<!-- koml_test.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xml>
<koml>
  <case>
    <pattern>너_j 점심_j 뭐_j 먹었_e?</pattern>
    <template>로봇이 밥을 왜먹음</template>
  </case>
</koml>
```
```python
# main.py
from koml import KomlBot

bot = KomlBot()
bot.learn(['getting_started.xml'])
bot.converse()
```
<br>

### 결과
```
<< 너는 점심에 뭐 먹었니?
>> 로봇이 밥을 왜먹음
```

<br>

## Usage

[**공식문서**](https://koml-docs.readthedocs.io/en/latest/) 를 참조해주세요!

URL: https://koml-docs.readthedocs.io/en/latest/
