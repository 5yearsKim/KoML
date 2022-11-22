# 전처리 

## 디버그 모드 

내가 입력한 말들의 품사가 어떻게 형성되는지 궁금하면 debug 모드를 켜고 대화를 진행해 볼 수 있어요.

```python
from koml import KomlBot

bot = KomlBot(debug=True)
bot.learn(['getting_started.xml'])
bot.converse()
```

```
<< 너는 이름이 뭐야?
[$너/NP, $는/JX, $_, $이름/NNG, $이/JKS, $_, $뭐/NP, $야[$이/VCP, $야/EF]/VCP+EF, $?/SF]
>> 내 이름은 코엠엘챗봇이야!
```

<br>
<br>

## Preprocessor
디버그 모드를 켜고 대화를 하다보면 패턴 매치를 하기 전에 특정한 방식으로 대화를 처리하고 싶을 수 있어요. 예를 들면 다음과 같은 경우를 고려해볼게요.

```xml
<case>
  <pattern>
    <li>너_j 여자친구 없_e_s</li>
    <li>너_j 여자친구 있_e_s</li>
  </pattern>
  <template>그건 뭐 쌈싸먹는거임?</template>
</case>
```

```
<< 너 여자친구 없어?
[$너/NP, $_, $여자/NNG, $친구/NNG, $_, $없/VA, $어/EF, $?/SF]
>> 그건 뭐 쌈싸먹는거임?

<< 너는 여자친구 진짜 없어?
[$너/NP, $는/JX, $_, $여자/NNG, $친구/NNG, $_, $진짜/MAG, $_, $없/VA, $어/EF, $?/SF]
>> None

<< 너 정말 여자친구 없어?
[$너/NP, $_, $정말/MAG, $_, $여자/NNG, $친구/NNG, $_, $없/VA, $어/EF, $?/SF]
>> None
```

<br>

다음과 같은 경우 \<pattern> 에 있는 대로 '너 여자친구 없어?' 라는 질문에는 잘 대답 하지만 '정말', '진짜' 같은 **부사**(MAG)가 들어가게 되면 효과적으로 잘 처리하지 못해요. 더군다나 부사는 문장의 어느 자리에 들어가도 자연스럽기 때문에 처리하기가 더 까다로워요. 
<br>
<br>
이를 해결하기 위해서 '진짜', '정말' 과 같은 부사를 패턴 매칭 하기 전에 모두 제거해줄 수 있어요.

```python
from koml import KomlBot, RemovePosPreprocessor, CustomBag

# 부사 제거 전처리
preprocessor = RemovePosPreprocessor(npos=['MAG'])
bag = CustomBag(preprocessor=preprocessor)

bot = KomlBot(bag, debug=True)
bot.learn(['preprocessor.xml'])
bot.converse()
```
<br>
다음과 같이 부사와 관계 없이 잘 매칭되는것을 확인할 수 있어요.
<br>

```
<< 너 진짜 여자친구 있어?
[$너/NP, $_, $진짜/MAG, $_, $여자/NNG, $친구/NNG, $_, $있/VA, $어/EF, $?/SF]
>> 그건 뭐 쌈싸먹는거임?

<< 진짜 너 여자친구 있어?
[$진짜/MAG, $_, $너/NP, $_, $여자/NNG, $친구/NNG, $_, $있/VA, $어/EF, $?/SF]
>> 그건 뭐 쌈싸먹는거임?

<< 너 여자친구 정말 있어?
[$너/NP, $_, $여자/NNG, $친구/NNG, $_, $정말/MAG, $_, $있/VA, $어/EF, $?/SF]
>> 그건 뭐 쌈싸먹는거임?
```

