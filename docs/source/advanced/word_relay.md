# 끝말잇기

KoML 의 기능들을 이용해서 끝말잇기를 만들어볼거에요.

```
<< 끝말잇기 하자
>> ㅋㅋㅋ 로봇인 나한테 끝말잇기로 덤비시겠다?
<< 응
>> 오키ㅋㅋ 그럼 너부터 시작해!
<< 고기
>> 기쁨
<< 쁨?
>> 뭐야 그건 너무 짧잖아 ㅋㅋ 너 졌어
<< 뭐야
>> ㅋㅋㅋㅋ억울하면 한 번 더 할래?
<< 아니
>> 싫으면 하지 마라ㅋㅋ 난 놀아줄라고 한건데
<< 끝말잇기 하자
>> ㅋㅋㅋ 로봇인 나한테 끝말잇기로 덤비시겠다?
<< 응
>> 오키ㅋㅋ 그럼 너부터 시작해!
<< 스트론튬
>> 앗.. 스트론튬은 이어지는 단어가 없는데ㅋㅋ 나의 패배다ㅠㅠ
<< ㅋㅋ
>> ㅋㅋㅋㅋ너 잘한다 한 번 더 할래?
<< 아니
>> 싫으면 하지 마라ㅋㅋ 난 놀아줄라고 한건데
```

<br>

## 끝말잇기 패키지 설치

끝말잇기 로직을 직접 구현해도 되지만 끝말잇기를 쉽게 할 수 있도록 도와주는 파이썬 패키지 [korean_word_relay](https://pypi.org/project/korean-word-relay/) 를 설치해주세요.

> pip install korean_word_relay

<br>

## 커스텀 함수 작성
끝말잇기를 하기위해 필요한 커스텀 함수를 작성해주세요.

```python
from korean_word_relay import WordRelay
from koml import Context
import re

word_relay = WordRelay()
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

def state_word_relay(word: str, context: Context|None=None) -> str:
    ''' 내 답안이 문제가 없는 답변안인지 확인 '''
    # 한글이 아닌 글자 모두 제거
    word = hangul.sub('', word)

    # 답변은 최소 2글자 이상!
    if len(word) < 2:
        return 'short'

    holder = []
    for item in context.history[:5]:
        holder.append(item.answer.strip())
        holder.append(item.question.strip())
    history = holder

    # 앞선 문맥에 중복된 단어 발견
    if word in history:
        return 'duplicated'

    # 앞에 단어와 내 답변이 끝말잇기 되지 않음
    if not history:
        return 'no_match'
    prev_word = hangul.sub('', history[0])

    is_start = '시작해' in prev_word
    is_continue = word_relay.check_continue(prev_word, word)
    if not is_start and not is_continue:
        return 'no_match'

    next_word = word_relay.get_next(word, log_history=False)
    # koml 봇이 대답할 수 있는 단어 찾음/못찾음
    if next_word:
        return 'found'
    else:
        return 'no_found'

def get_word_relay(word :str, context: Context|None=None) -> str:
    ''' koml 봇 끝말잇기 단어 리턴 '''
    word = hangul.sub('', word)
    next_word = word_relay.get_next(word, log_history=True)
    return next_word
```

<br>

## koml 작성
KoML의 기능들을 활용해서 끝말잇기 처리를 위한 case 들을 작성해주세요.

<br>

```xml
<!-- word_relay.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xml>
<koml>
  <case id='word_intro'>
    <pattern>
      <li>* 끝말잇기 할래_s</li>
      <li>끝말잇기 잘해_s</li>
      <li>끝말잇기 하자*</li>
    </pattern>
    <template>ㅋㅋㅋ 로봇인 나한테 끝말잇기로 덤비시겠다?</template>
  </case>

  <case>
    <follow cid='word_intro, word_user_lose, word_user_win'/>
    <pattern>
      <li>*싫은데?*</li>
      <li>* 아니 *</li>
      <li>* 싫어 *</li>
    </pattern>
    <template>싫으면 하지 마라ㅋㅋ 난 놀아줄라고 한건데</template>
  </case>

  <case id='word_1'>
    <follow cid='word_intro, word_user_lose, word_user_win'/>
    <pattern>
      <li>응 *</li>
      <li>*좋아*</li>
      <li>*하자*</li>
      <li>*그래*</li>
    </pattern>
    <template>오키ㅋㅋ 그럼 너부터 시작해!</template>
  </case>

  <case id='word_2'>
    <follow cid='word_1,word_2'/>
    <pattern><blank/></pattern>
    <template>
      <switch>
        <pivot><func name='state_word_relay'> <arg><blank/></arg> </func></pivot>
        <scase pivot='duplicated'>엥 그거 아까 나왔던 단어인데 ㅋㅋ 너 졌어</scase>
        <scase pivot='short'>뭐야 그건 너무 짧잖아 ㅋㅋ 너 졌어</scase>
        <scase pivot='no_match'>뭐야 <blank/>_eun 안이어지잖아ㅋㅋ 너 졌어</scase>
        <scase pivot='no_found'>앗.. <blank/>_eun 이어지는 단어가 없는데ㅋㅋ 나의 패배다ㅠㅠ</scase>
        <scase pivot='found'>
          <func name='get_word_relay'> <arg><blank/></arg> </func>
        </scase>
        <default>음.. 어렵네</default>
      </switch>
    </template>
  </case>

  <case id='word_user_lose'>
    <follow cid='word_2'>* 너 졌어</follow>
    <pattern>*</pattern>
    <template>ㅋㅋㅋㅋ억울하면 한 번 더 할래?</template>
  </case>

  <case id='word_user_win'>
    <follow cid='word_2'>* 나의 패배다ㅠㅠ</follow>
    <pattern>*</pattern>
    <template>ㅋㅋㅋㅋ너 잘한다 한 번 더 할래?</template>
  </case>
</koml>
```

<br>

## 실행
작성한 커스텀 함수와 함께 KomlBot 을 실행해주세요.

```python
from koml import KomlBot,  CustomBag

bag = CustomBag(funcs={'get_word_relay': get_word_relay, 'state_word_relay': state_word_relay})

bot = KomlBot(bag)
bot.learn(['word_relay.xml'])
bot.converse()
```

<br>

## 결과 확인
끝말잇기가 성공적으로 진행 되면 성공입니다 :)

<br>

```
<< 끝말잇기 하자
>> ㅋㅋㅋ 로봇인 나한테 끝말잇기로 덤비시겠다?
<< 응
>> 오키ㅋㅋ 그럼 너부터 시작해!
<< 고기
>> 기쁨
<< 쁨?
>> 뭐야 그건 너무 짧잖아 ㅋㅋ 너 졌어
<< 뭐야
>> ㅋㅋㅋㅋ억울하면 한 번 더 할래?
<< 아니
>> 싫으면 하지 마라ㅋㅋ 난 놀아줄라고 한건데
<< 끝말잇기 하자
>> ㅋㅋㅋ 로봇인 나한테 끝말잇기로 덤비시겠다?
<< 응
>> 오키ㅋㅋ 그럼 너부터 시작해!
<< 스트론튬
>> 앗.. 스트론튬은 이어지는 단어가 없는데ㅋㅋ 나의 패배다ㅠㅠ
<< ㅋㅋ
>> ㅋㅋㅋㅋ너 잘한다 한 번 더 할래?
<< 아니
>> 싫으면 하지 마라ㅋㅋ 난 놀아줄라고 한건데
```