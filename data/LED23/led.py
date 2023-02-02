# python code that will iterate over led23.nt file and create the files need for the KGC task


# creating entities.txt
# import rdflib
# import html5lib
# import os

# g = rdflib.Graph()

# #parse the led23.nt file
# result = g.parse("led23.nt", format="nt")

# #create a set to store unique entities
# entities = set()

# #iterate over all triples in the graph
# for s, p, o in g:
#     try:
#         #add the subject to the set of entities
#         entities.add(s)
#         #add the object to the set of entities
#         # entities.add(o)
#     except html5lib.html5parser.ParseError:
#         #skip the comment nodes as they can cause errors
#         continue
#     except IndexError:
#         #skip the triple if the list index is out of range
#         continue

# #open the entities.txt file in write mode
# with open("entities.txt", "w") as f:
#     #write each entity in a new line in the entities.txt file
#     for entity in entities:
#         f.write("%s\n" % entity)

# #close the entities.txt file
# f.close()

# creating entity2text
# import rdflib
# import html5lib
# import os

# g = rdflib.Graph()

# #parse the led23.nt file
# result = g.parse("led23.nt", format="nt")

# #create a dictionary to store entities and their names
# entity2text = {}

# #open the entity2text.txt file in write mode
# with open("entity2text.txt", "w") as f:
#     #iterate over all triples in the graph
#     for s, p, o in g:
#         try:
#             #check if the subject and object are not already in the dictionary
#             if s not in entity2text:
#                 entity2text[s] = s.toPython()
#             # if o not in entity2text:
#             #     entity2text[o] = o.toPython()
#         except html5lib.html5parser.ParseError:
#             #skip the comment nodes as they can cause errors
#             continue
#         except IndexError:
#             #skip the triple if the list index is out of range
#             continue

#     #write all entities and their names in the entity2text.txt file
#     for entity, name in entity2text.items():
#         f.write("%s\t%s\n" % (entity, name))

# #close the entity2text.txt file
# f.close()

# entity2txtlong
# import os
# import rdflib

# # create the entity2txtlong.txt file
# entity_file = open("entity2txtlong.txt", "w")

# # Read the led23.nt file
# graph = rdflib.Graph()
# result = graph.parse("led23.nt", format="nt")
# triples = list(graph)

# # Ensure the list index is not out of range
# if len(triples) == 0:
#     print("No triples found in led23.nt")
# else:
#     entities = {}

#     # Extract the entities and their descriptions
#     for triple in triples:
#         subject = str(triple[0])
#         predicate = str(triple[1])
#         obj = str(triple[2])

#         if predicate == "http://www.w3.org/2000/01/rdf-schema#comment":
#             entities[subject] = obj

#     # Write the entities and their descriptions to the file
#     for entity, description in entities.items():
#         entity_file.write(f"{entity}\t{description}\n")

# # Close the file
# entity_file.close()


# Relation2text
# import rdflib
# import html5lib
# import os

# g = rdflib.Graph()

# # parse the led23.nt file
# result = g.parse("led23.nt", format="nt")

# # create a dictionary to store relations and their attributes
# relation2text = {}

# # iterate through all the triples in the graph
# for subject, predicate, obj in g:
#     try:
#         # check if the predicate is not already in the dictionary
#         if predicate not in relation2text:
#             # add the predicate and its attribute to the dictionary
#             relation2text[predicate] = obj
#     except html5lib.html5parser.ParseError:
#         # skip the comment nodes as they can cause errors
#         continue
#     except IndexError:
#         # skip the triple if the list index is out of range
#         continue

# # open the relation2text.txt file in write mode
# with open("relation2text.txt", "w") as f:
#     # write all relations and their attributes in the relation2text.txt file
#     for relation, attribute in relation2text.items():
#         f.write("%s\t%s\n" % (relation, attribute))

# # close the relation2text.txt file
# f.close()

# Relation
# import rdflib
# import html5lib
# import os

# g = rdflib.Graph()

# #parse the led23.nt file
# result = g.parse("led23.nt", format="nt")

# #create a set to store all the relations found in led23.nt
# relations = set()

# #iterate through all the triples in the graph
# for s, p, o in g:
#     try:
#         #add the predicate (relation) to the set
#         relations.add(p)
#     except html5lib.html5parser.ParseError:
#         #skip the comment nodes as they can cause errors
#         continue
#     except IndexError:
#         #skip the triple if the list index is out of range
#         continue

# #open the relations.txt file in write mode
# with open("relations.txt", "w") as f:
#     #write all the relations in the relations.txt file
#     for relation in relations:
#         f.write("%s\n" % relation)

# #close the relations.txt file
# f.close()

# Creating dev,train, and test .tsv
import os
import random
import rdflib
#import html5lib

# create the dev.tsv, train.tsv and test.tsv files
dev_file = open("dev.tsv", "w")
train_file = open("train.tsv", "w")
test_file = open("test.tsv", "w")

# Read the led23.nt file
graph = rdflib.Graph()
result = graph.parse("led23.nt", format="nt")
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
        train_file.write(f"{s}\t{p}\t{o}\n")

    for triple in dev_triples:
        s = triple[0].n3()
        p = triple[1].n3()
        o = triple[2].n3()
        dev_file.write(f"{s}\t{p}\t{o}\n")

    for triple in test_triples:
        s = triple[0].n3()
        p = triple[1].n3()
        o = triple[2].n3()
        test_file.write(f"{s}\t{p}\t{o}\n")

# Close the files
dev_file.close()
train_file.close()
test_file.close()
