# python code that will iterate over led23.nt file and create the files need for the KGC task

import os
from rdflib import Graph
import html5lib


def get_entities_and_relations(file):
    entities = set()
    relations = set()
    g = Graph()
    g.parse(file)
    for subj, pred, obj in g:
        entities.add(subj)
        entities.add(obj)
        relations.add(pred)
    return entities, relations


def write_to_file(file_name, data):
    if not data:
        return
    try:
        with open(file_name, 'w') as f:
            for line in data:
                f.write(f"{line}\n")
    except Exception as e:
        print(f"Error writing to file {file_name}: {e}")


def create_files(nt_file):
    entities, relations = get_entities_and_relations(nt_file)
    write_to_file('entities.txt', list(entities))
    write_to_file('relations.txt', list(relations))
    write_to_file('entity2text.txt', list(entities))
    write_to_file('entity2txtlong.txt', list(entities))
    write_to_file('relation2text.txt', list(relations))

    texts = []
    train_lines = []
    dev_lines = []
    for i, entity in enumerate(list(entities)):
        texts.append(f'{i}\t{entity}')
        if i % 10 == 0:
            dev_lines.append(f'{i}\t{entity}')
        else:
            train_lines.append(f'{i}\t{entity}')

    write_to_file('text.tsv', texts)
    write_to_file('train.tsv', train_lines)
    write_to_file('dev.tsv', dev_lines)


if __name__ == '__main__':
    nt_file = 'led23.nt'
    create_files(nt_file)
