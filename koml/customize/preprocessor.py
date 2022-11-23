from abc import ABC, abstractmethod
from korean_rule_helper import KoreanSentence
from korean_rule_helper.parser import Tag as KTag

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

class FilterPreprocessor(Preprocessor):
    def __init__(self, filter_words: list[str]=[]) -> None:
        self.filter_words: list[str] = filter_words
        super().__init__()

    def process(self, sentence: KoreanSentence) -> KoreanSentence:
        # too short -> not processing
        if len(sentence.tags) <= 2:
            return sentence
        holder: list[KTag] = []
        for tag in sentence.tags:
            if holder and holder[-1].surface.isspace() and tag.surface.isspace():
                continue
            if tag.surface in self.filter_words:
                continue
            holder.append(tag)
        sentence.tags = holder
        print(holder)
        return sentence

