import json
from typing import List
from collections import defaultdict
from pydantic import RootModel
from pydantic.dataclasses import dataclass

@dataclass
class Lemma:
    lemma: str 
    pos: str
    frequency: int
    wordform_freq: dict
    feats: set

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
    f.close()
    sentences = data['sentences']
    lemmas = {}

    for sentence in sentences:
        #print(f'sentence is: {sentence["sentence_text"]}')
        sentence = Sentence(**sentence)
        for token in sentence.tokens:
            key = token.lemma + '_' + token.pos
            #lemma_text = token.lemma
            if key in lemmas:
                lemma = lemmas[key]
                lemma.frequency += 1
                lemma.feats.add(token.feats)
                word_form = token.text
                #lemma.pos.add(token.pos)
                if word_form in lemma.wordform_freq:
                    lemma.wordform_freq[word_form] += 1
                else:
                    lemma.wordform_freq[word_form] = 1
            else:
                lemmas[key] = Lemma(lemma = token.lemma, pos = token.pos, frequency = 1, wordform_freq = {token.text : 1}, feats = set())
                if token.feats is not None:
                    lemmas[key].feats.add(token.feats)

    print(f'Unique lemmas: {len(lemmas)}')

    output_filename = 'lemma_lexicon.json'
    with open(output_filename, 'w') as outfile:
        lemma_list = lemmas.values()
        outfile.write(RootModel[List[Lemma]](lemma_list).model_dump_json(indent=2))
        #for key in lemmas:
        #    lemma = lemmas[key]
        #    outfile.write(RootModel[Lemma](lemma).model_dump_json(indent=2))
        #    print(lemma)

    

