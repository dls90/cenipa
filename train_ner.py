#!/usr/bin/env python
# coding: utf8
"""Example of training spaCy's named entity recognizer, starting off with an
existing model or a blank model.
For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities
Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding

# training data
TRAIN_DATA = [
    (
    "após a arremetida, o piloto efetuou uma manobra não prevista para o tráfego visual, deixando de cumprir o perfil da vac prevista para o aeródromo. além disso, o piloto operou a aeronave sem estar devidamente habilitado, o que contribuiu para que cortasse o motor inadvertidamente.",
    {
        'entities': [(21, 28, "PERSON"), (7, 17, "EVENT"), (40, 84, "EVENT"), (190, 220, "EVENT"), (246, 280, "EVENT")]
    }),
    (
    "considerando que o piloto não estava habilitado para o voo, pode-se supor que não tenha tido o devido treinamento na aeronave.",
    {
        'entities': [(37,59, "EVENT"),(102,114, "EVENT")]
    }
    ),
    (
    "a deficiência da bateria determinou a impossibilidade de uma partida de emergência, após o corte involuntário dos motores.",
    {
        'entities': [(2,14, "EVENT"), (17,25, "EVENT")]
    }
    ),
    (
    "o piloto efetuou o corte dos motores, inadvertidamente, quando a intenção era apenas reduzir os motores para a aproximação para pouso.",
    {
        'entities': [(19,37, "EVENT")]
    }
    ),
    (
    "apesar de o manual de vôo da aeronave preconizar que a bomba elétrica de combustível deva permanecer ligada durante vôos a baixa altura, o piloto ignorou a recomendação, optando por desligá-la. com a bomba elétrica ligada, certamente o motor não teria falhado diante da falha da bomba mecânica.",
    {
        'entities': [(55,70, "EVENT"), (73,85, "EVENT"), (182,194, "EVENT")]
    }
    ),
    (
    "a bomba mecânica de combustível tem sido fabricada pela embraer/neiva, sob licença da lycoming, fabricante do motor. a bomba mecânica original foi alterada pela embraer para utilização com motores a álcool. inicialmente classificada como componente on-condition, a bomba mecânica não sofria ações de manutenção. com a implantação da diretriz de aeronavegabilidade – da nº 2008-04-01, vigente a partir de 30 abr 2008, a bomba mecânica passou a ser item controlado. portanto, torna-se evidente que os parâmetros inicialmente fixados pelo fabricante eram inadequados, configurando o projeto como fator contribuinte.",
    {
        'entities': [(265,280, "EVENT")]
    }
    ),
    (
    "compõe a cultura profissional dos pilotos agrícolas o entendimento de que a utilização continuada da bomba elétrica de combustível, conforme recomendado no manual de operação da aeronave para operações agrícolas, conduz ao desgaste e à sua falha. em decorrência deste pensamento, os pilotos usualmente desligam a bomba elétrica após a decolagem, executando o restante do vôo agrícola com ela desligada. no caso de falha da bomba mecânica de combustível, a bomba elétrica, quando ligada, tem a finalidade de manter a alimentação de combustível para o motor.",
    {
        'entities': [(101,116, "EVENT")]
    }
    ),
    (
    "o piloto apresentava invulnerabilidade, dimensionada pela excessiva confiança em si. informou não ter dúvidas quanto ao peso de decolagem, vento e combustível e sobre os procedimentos utilizados, alegando ter procedido de forma exata e dentro da experiência de voo que possuía.",
    {
        'entities': [(21,40, "EVENT")]
    }
    ),
    (
    "a falta de planejamento para voos no sentido da efetiva e normativa segurança, com falta de gerenciamento dos riscos dentro de uma dimensão abalizada, pode ter influenciado na ocorrência do acidente.",
    {
        'entities': [(92,117, "EVENT")]
    }
    ),
    (
    "houve falha de supervisão, visto que o piloto não estava habilitado para esse tipo de voo, necessitando acompanhamento de outro piloto habilitado durante os voos, o que não ocorreu.",
    {
        'entities': [(57,68, "EVENT")]
    }
    ),
    (
    "é possível que tenha havido uma aplicação inadequada dos comandos da aeronave ao reduzir o coletivo muito rápido para o pouso e na tentativa de contrariar a tendência de rolamento da aeronave com o cíclico.",
    {
        'entities': [(57,78, "EVENT")]
    }
    ),
    (
    "é possível que o piloto tenha se esquecido de destravar o sistema de fricção dos comandos de voo da aeronave, antes da decolagem.",
    {
        'entities': [(58,77, "EVENT"),(33,56, "EVENT")]
    }
    ),
    (
    "os meios disponíveis para o combate a incêndio do heliponto não eram adequados, o que permitiu que a aeronave fosse completamente destruída pelo fogo.",
    {
        'entities': [(28,47, "EVENT")]
    }
    ),
    (
    "o operador, em seu nível gerencial, alocou recursos humanos inadequados para a atividade de pilotagem, pois o piloto não estava habilitado para o voo em questão.",
    {
        'entities': [(36,60, "EVENT")]
    }
    )

]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print('Losses', losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
            print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == '__main__':
    plac.call(main)

    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]
