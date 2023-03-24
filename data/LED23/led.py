import rdflib
import os
import random
import hashlib

# Function that replaces comment notes, "__" with ""


def preprocess(filename):
    with open(filename, "r") as file:
        content = file.read()
        content = content.replace("--", "")

    with open(filename, "w") as file:
        file.write(content)


# Function that hash literals and urn: from the triples in a file named "led23.nt" and convert them to "s", "p", "o", then delete the original file and rename the new file to the original file name

def hash_literals(filename):
    g = rdflib.Graph()
    g.parse(filename, format='nt')
    t = rdflib.Graph()
    for s, p, o in g:
        if isinstance(o, rdflib.term.Literal) or str(o).startswith('urn:'):
            hash_value = hashlib.shake_128(str(type(o)).encode(
                'UTF-8') + str(o).encode('UTF-8')).hexdigest(13)
            o_uri = rdflib.URIRef(f"http://led.kmi.open.ac.uk/23/{hash_value}")
            t.add((s, p, o_uri))
        else:
            t.add((s, p, o))
    t.serialize(destination="led23.nt", format="nt")

# Function to hash triples that has more that 510 tokens


def hashing_longtriples(filename):
    g = rdflib.Graph()
    g.parse(filename, format='nt')
    t = rdflib.Graph()
    for s, p, o in g:
        if len(s) > 150:
            s_hash = hashlib.shake_128(str(type(s)).encode(
                'UTF-8') + str(s).encode('UTF-8')).hexdigest(13)
            s_uri = rdflib.URIRef(f"http://led.kmi.open.ac.uk/24/{s_hash}")
            t.add((s_uri, p, o))
        else:
            t.add((s, p, o))
        if len(p) > 150:
            p_hash = hashlib.shake_128(str(type(p)).encode(
                'UTF-8') + str(p).encode('UTF-8')).hexdigest(13)
            p_uri = rdflib.URIRef(f"http://led.kmi.open.ac.uk/24/{p_hash}")
            t.add((s, p_uri, o))
        else:
            t.add((s, p, o))
        if len(o) > 150:
            o_hash = hashlib.shake_128(str(type(o)).encode(
                'UTF-8') + str(o).encode('UTF-8')).hexdigest(13)
            o_uri = rdflib.URIRef(f"http://led.kmi.open.ac.uk/24/{o_hash}")
            t.add((s, p, o_uri))
        else:
            t.add((s, p, o))
    t.serialize(destination="led23.nt", format="nt")


# Function to create dev, train and test datasets


def split_triples(filename):
    # create the dev.tsv, train.tsv and test.tsv files
    dev_file = open("dev.tsv", "w")
    train_file = open("train.tsv", "w")
    test_file = open("test.tsv", "w")

    # Read the led23.nt file
    graph = rdflib.Graph()
    result = graph.parse(filename, format="nt")
    triples = list(graph)

    # Ensure the list index is not out of range
    if len(triples) == 0:
        print("No triples found in led23.nt")
    else:
        # Split triples into 70% for train.tsv, 15% for dev.tsv and 15% for test.tsv
        random.shuffle(triples)
        split_1 = int(len(triples) * 0.7)
        split_2 = int(len(triples) * 0.15) + split_1

        train_triples = triples[:split_1]
        dev_triples = triples[split_1:split_2]
        test_triples = triples[split_2:]

        # Write the triples to their respective files
        for triple in train_triples:
            s = triple[0].n3()
            p = triple[1].n3()
            o = triple[2].n3()
            train_file.write(s + "\t" + p + "\t" + o + "\n")

        for triple in dev_triples:
            s = triple[0].n3()
            p = triple[1].n3()
            o = triple[2].n3()
            dev_file.write(s + "\t" + p + "\t" + o + "\n")

        for triple in test_triples:
            s = triple[0].n3()
            p = triple[1].n3()
            o = triple[2].n3()
            test_file.write(s + "\t" + p + "\t" + o + "\n")

    # Close the files
    dev_file.close()
    train_file.close()
    test_file.close()


# Function to create entity.txt and relations.txt

def create_entities_and_relations_files():
    # Read the led23.nt file
    graph = rdflib.Graph()
    result = graph.parse("led23.nt", format="nt")

    # Get all the entities and relations in led23.nt
    entities = set()
    relations = set()
    for s, p, o in graph:
        entities.add(s.n3())
        relations.add(p.n3())
        entities.add(o.n3())

    # Write the entities and relations to their respective files
    with open("entities.txt", "w") as entities_file:
        for entity in entities:
            entities_file.write(f"{entity}\n")

    with open("relations.txt", "w") as relations_file:
        for relation in relations:
            relations_file.write(f"{relation}\n")


# Create the entity2text.txt and relation2text.txt
def create_entity2text_and_relation2text_files():
    # # Read the led23.nt file
    graph = rdflib.Graph()
    result = graph.parse("led23.nt", format="nt")

    # Get all the entities and relations in led23.nt
    entities = set()
    relations = set()
    entity_ids = {}
    relation_ids = {}
    for s, p, o in graph:
        s_str = s.n3()
        p_str = p.n3()
        o_str = o.n3()
        entities.add(s_str)
        relations.add(p_str)
        entities.add(o_str)

        if s_str not in entity_ids:
            s_parts = str(s).split("/")
            s_value = s_parts[-2] if s_parts[-1] == "" else s_parts[-1]
            entity_ids[s_str] = s_value
        if o_str not in entity_ids:
            o_parts = str(o).split("/")
            o_value = o_parts[-2] if o_parts[-1] == "" else o_parts[-1]
            entity_ids[o_str] = o_value

        # Get the unique identifiers for the relations
        if p_str not in relation_ids:
            relation_ids[p_str] = str(p).split("/")[-1]

    # Write the entities and their unique identifiers to entity2text.txt
    with open("entity2text.txt", "w") as entity2text_file:
        for entity in entities:
            entity_id = entity_ids.get(entity, entity)
            entity2text_file.write(f"{entity}\t{entity_id.split('/')[-1]}\n")

    # Write the relations and their unique identifiers to relation2text.txt
    with open("relation2text.txt", "w") as relation2text_file:
        for relation in relations:
            relation_id = relation_ids.get(relation, relation)
            relation2text_file.write(
                f"{relation}\t{relation_id.split('/')[-1]}\n")


def run_led23cleaning_process():
    filename = "led23.nt"
    preprocess(filename)
    hash_literals(filename)
    hashing_longtriples(filename)
    split_triples(filename)
    create_entities_and_relations_files()
    create_entity2text_and_relation2text_files()


if __name__ == "__main__":
    run_led23cleaning_process()
