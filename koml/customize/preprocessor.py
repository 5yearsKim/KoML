from abc import ABC, abstractmethod
from korean_rule_helper import KoreanSentence, Rule

class Preprocessor(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def process(self, sentence: KoreanSentence) -> KoreanSentence:
        pass

class DefaultPreprocessor(Preprocessor):
    def __init__(self) -> None:
        super().__init__()
    
    def process(self, sentence: KoreanSentence) -> KoreanSentence:
        return sentence

class RemovePosPreprocessor(Preprocessor):
    def __init__(self, npos: list[str]=[]) -> None:
        self.npos: list[str] = npos
        super().__init__()

    def process(self, sentence: KoreanSentence) -> KoreanSentence:
        rule = Rule(npos=self.npos)
        holder = []
        # too short -> not processing
        if len(sentence.tags) <= 2:
            return sentence
        for tag in sentence.tags:
            if tag.surface.isspace() and holder and holder[-1].surface.isspace():
                continue
            judge = rule.judge_tag(tag)
            if judge:
                holder.append(tag)
            # 왜 is an exception
            elif tag.surface == '왜':
                holder.append(tag)
        sentence.tags = holder
        return sentence

