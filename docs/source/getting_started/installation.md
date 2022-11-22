

# 시작하기

파이썬 **3.10 이상**을 지원해요. 파이썬 환경을 맞추어 주세요.


<br>

## 설치하기
```
pip install koml
```
<br>

## 테스트해보기
1. 작업 폴더에 koml.xml 파일을 만들고 아래와 같이 적어주세요.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xml>
<koml>
  <case>
    <pattern>너_j 이름_j 뭐야?</pattern>
    <template>내 이름은 코엠엘챗봇이야!</template>
  </case>
</koml>
```
2. 같은 폴더 내에 main.py 파일을 아래와 같이 적어주세요.

```python
# main.py
from koml import KomlBot

bot = KomlBot()
bot.learn(['koml.xml'])
bot.converse()
```

3. 코엠엘챗봇의 이름을 확인하면 성공입니다 :)
```
<< 너 이름이 뭐야?
>> 내 이름은 코엠엘챗봇이야!
```



