import json
from typing import List
from collections import defaultdict
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

@dataclass
class Lemma:
    lemma: str 
    pos: str
    frequency: int
    word_forms: dict

@dataclass
class Token:
    id: str
    text: str
    lemma: str
    pos: str
    pos_finegrained: str
    feats: str | None
    start_char: str
    end_char: str

@dataclass
class Sentence:
    sentence_text: str
    tokens: List[Token]


if __name__ == '__main__':
    f = open('sample_parsed_sentences.json')
    #f = open('test.json')
    data = json.load(f)
    sentences = data['sentences']
    lemmas = {}

    for sentence in sentences:
        print(f'sentence is: {sentence["sentence_text"]}')
        sentence = Sentence(**sentence)
        for token in sentence.tokens:
            lemma_text = token.lemma
            if lemma_text in lemmas:
                lemma = lemmas[lemma_text]
                lemma.frequency += 1
                word_form = token.text
                if word_form in lemma.word_forms:
                    lemma.word_forms[word_form] += 1
                else:
                    lemma.word_forms[word_form] = 1
            else:
                lemmas[lemma_text] = Lemma(lemma = lemma_text, pos = token.pos, frequency = 1, word_forms = {token.text : 1})

    print(f'Unique lemmas: {len(lemmas)}')
    print(lemmas)

