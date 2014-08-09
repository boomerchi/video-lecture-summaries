import re
import string

class Sentence:
    def __init__(self, content, startt, endt):
        self.content = content
        self.startt = startt
        self.endt = endt        
        for c in string.punctuation:
            content = content.replace(c, '')
        self.words = re.split(r'\s', content)
        
    def numwords(self):
        return len(words)

class Word:
    def __init__(self, original_word, aligned_word, startt, endt, line_idx, speaker):
        self.original_word = word
        self.aligned_word = aligned_word
        self.startt = float(startt)
        self.endt = float(endt)
        self.line_idx = int(line_idx)
        self.speaker = speaker
        self.issilent = (word == "{p}")
        self.duration = self.endt - self.startt
        