# python code that will iterate over led23.nt file and create the follwing files dev.tsv,
# entities.txt, entity2text.txt, entity2txtlong.txt, relation2text.txt, relations.txt, text.tsv, train.tsv

# import os


# def write_to_file(file_path, data, mode='w'):
#     with open(file_path, mode):
#         f.write(data)


# def get_entities_and_relations(nt_file):
#     entities = set()
#     relations = set()
#     with open(nt_file, 'r'):
#         for line in f:
#             subj, rel, obj = line.strip().split()
#             entities.add(subj)
#             entities.add(obj)
#             relations.add(rel)
#     return entities, relations


# def create_entity2text(entities, entity2text_file):
#     with open(entity2text_file, 'w') as f:
#         for entity in entities:
#             f.write(f"{entity}\t{entity}\n")


# def create_relation2text(relations, relation2text_file):
#     with open(relation2text_file, 'w') as f:
#         for rel in relations:
#             f.write(f"{rel}\t{rel}\n")


# def create_dev_train_text(nt_file, dev_file, train_file, text_file):
#     with open(nt_file, 'r') as f:
#         with open(dev_file, 'w') as dev:
#             with open(train_file, 'w') as train:
#                 with open(text_file, 'w') as text:
#                     for i, line in enumerate(f):
#                         subj, rel, obj = line.strip().split()
#                         if i % 10 == 0:
#                             dev.write(f"{subj}\t{rel}\t{obj}\n")
#                         else:
#                             train.write(f"{subj}\t{rel}\t{obj}\n")
#                         text.write(f"{subj}\t{rel}\t{obj}\n")


# if __name__ == '__main__':
#     nt_file = "led23.nt"
#     dev_file = "dev.tsv"
#     train_file = "train.tsv"
#     text_file = "text.tsv"
#     entities_file = "entities.txt"
#     entity2text_file = "entity2text.txt"
#     entity2txtlong_file = "entity2txtlong.txt"
#     relation2text_file = "relation2text.txt"
#     relations_file = "relations.txt"

#     entities, relations = get_entities_and_relations(nt_file)
#     write_to_file(entities_file, "\n".join(entities))
#     write_to_file(relations_file, "\n".join(relations))
#     create_entity2text(entities, entity2text_file)
#     write_to_file(entity2txtlong_file, "")
#     create_relation2text(relations, relation2text_file)
#     create_dev_train_text(nt_file, dev_file, train_file, text_file)


import os


def get_entities_and_relations(nt_file):
    entities = set()
    relations = set()
    with open(nt_file, 'r') as f:
        for line in f:
            subject, relation, object_ = line.strip().split()
            entities.add(subject)
            entities.add(object_)
            relations.add(relation)
    return entities, relations


def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        for line in data:
            f.write(line + '\n')


def create_files(nt_file):
    entities, relations = get_entities_and_relations(nt_file)
    entities = list(entities)
    relations = list(relations)

    write_to_file('entities.txt', entities)
    write_to_file('relations.txt', relations)
    write_to_file('entity2text.txt', entities)
    write_to_file('entity2txtlong.txt', entities)
    write_to_file('relation2text.txt', relations)

    texts = []
    train_lines = []
    dev_lines = []
    for i, entity in enumerate(entities):
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
