import pprint
from collections import Counter

import spacy
from executeQuery import executeQuery

if __name__ == "__main__":

    # executa a query e retorna todas linhas em array
    exec = executeQuery()
    rows = exec.query()

    # carrega o dicionario contino no spacy para português
    nlp = spacy.load('pt')
    wordx = []

    '''
        Caso queira utilizar o agrupamento com radical da palavra
        substituir .text por .lemma_
    '''

    # vare as tuplas e apos vare as strings
    for r in rows:
        for row in r:
            texto = nlp(row.lower())

            # for para transformar o texto em palavras = tokenization
            for token in texto:

                # se a palavra atual for um substantivo
                if token.dep_ != 'nmod' and  token.pos_ == 'NOUN':

                    # se for adjetivo e nao estiver na raiz e na folha
                    if token.doc[token.i+1].pos_ == 'ADJ':
                        # se for verbo e nao estiver na raiz
                        if token.dep_ != 'ROOT' and token.doc[token.i+1].pos_ != 'PUNCT' and token.doc[token.i+2].pos_ == 'VERB':
                            wordx.append(token.doc[token.i-1].text +' '+ token.text +' '+ token.doc[token.i+1].text+
                                                ' '+token.doc[token.i+2].text+' '+ token.doc[token.i+3].text)
                        else:
                            wordx.append(token.doc[token.i-1].text+' '+ token.text+' '+ token.doc[token.i+1].text)

                    # se for verbo
                    if token.doc[token.i+1].pos_ == 'VERB':

                        if token.doc[token.i+2].pos_ == 'DET':

                            if token.doc[token.i+3].pos_ == 'PUNCT':
                                wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text
                                      +' '+token.doc[token.i+3].text)

                            elif token.doc[token.i+4].pos_ == 'PUNCT':
                                wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text
                                             +' '+token.doc[token.i + 3].text+' '+token.doc[token.i + 4].text)

                            elif token.doc[token.i+5].pos_ == 'PUNCT':
                                wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text
                                             +' '+token.doc[token.i + 3].text+' '+token.doc[token.i + 4].text
                                             +' '+token.doc[token.i + 5].text)

                            elif token.doc[token.i+6].pos_ == 'PUNCT':
                                wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text
                                             +' '+token.doc[token.i + 3].text+' '+token.doc[token.i + 4].text
                                             +' '+token.doc[token.i + 5].text+' '+token.doc[token.i+6].text)

                            elif token.doc[token.i+7].pos_ == 'PUNCT':
                                wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text
                                             +' '+token.doc[token.i + 3].text+' '+token.doc[token.i + 4].text
                                             +' '+token.doc[token.i + 5].text+' '+token.doc[token.i+6].text
                                             +' '+token.doc[token.i+7].text)

                            elif token.doc[token.i+8].pos_ == 'PUNCT':
                                wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text
                                             +' '+token.doc[token.i + 3].text+' '+token.doc[token.i + 4].text
                                             +' '+token.doc[token.i + 5].text+' '+token.doc[token.i+6].text
                                             +' '+token.doc[token.i+7].text+' '+token.doc[token.i+8].text)

                        if token.doc[token.i+2].pos_ == 'ADP':
                            if token.doc[token.i+3].pos_ != 'PUNCT':
                                wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text
                                    +' '+token.doc[token.i+3].text)

                            else:
                                wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text
                                    +' '+token.doc[token.i+3].text+' '+token.doc[token.i+4].text+' '+token.doc[token.i+5].text)

                    if token.doc[token.i+1].pos_ == 'DET' and token.doc[token.i-1].pos_ == 'ADJ':
                        wordx.append(token.doc[token.i-1].text+' '+token.text+' '+token.doc[token.i+1].text
                                     +' '+token.doc[token.i+2].text)

                    if token.doc[token.i-1].pos_ == 'VERB' and token.doc[token.i-2].pos_ == 'ADV':
                        if token.doc[token.i+1].pos_ == 'PUNCT':
                            wordx.append(token.doc[token.i - 2].text+' '+token.doc[token.i - 1].text+' '+token.text
                                         +' '+token.doc[token.i + 1].text)

                        else:
                            wordx.append(token.doc[token.i-2].text+' '+token.doc[token.i-1].text+' '+token.text
                                         +' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text)

                    if token.doc[token.i+1].pos_ == 'AUX':
                        if token.doc[token.i+2].pos_ == 'PUNCT':
                            wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text)

                        elif token.doc[token.i+3].pos_ == 'PUNCT':
                            wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text
                                +' '+token.doc[token.i+3].text)

                        elif token.doc[token.i+4].pos_ == 'PUNCT':
                            wordx.append(token.text+' '+token.doc[token.i + 1].text+' '+token.doc[token.i + 2].text
                                         +' '+token.doc[token.i + 3].text+' '+token.doc[token.i + 4].text)

                        elif token.doc[token.i+5].pos_ == 'PUNCT':
                            wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text
                                +' '+token.doc[token.i+3].text+' '+token.doc[token.i + 4].text+' '+token.doc[token.i + 5].text)

                    if token.doc[token.i+1].pos_ == 'ADP':
                        wordx.append(token.text+' '+token.doc[token.i+1].text+' '+token.doc[token.i+2].text)

                    if token.doc[token.i+1].pos_ == 'ADV' and token.doc[token.i+2].pos_ == 'VERB':
                        wordx.append(token.text+' '+token.doc[token.i + 1].text+' '+token.doc[token.i + 2].text
                                     +' '+token.doc[token.i + 3].text)
    # printa as palavras
    print(wordx)

    # conta frequencia das palavras e printa
    word_freq = Counter(wordx)
    print(word_freq)

    # conta as 5 mais frequentes e printa
    common_words = word_freq.most_common(10)
    print(common_words)