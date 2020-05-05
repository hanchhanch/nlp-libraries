import re
import json
import spacy

TEXT = "Dopamine (DA, a contraction of 3,4-dihydroxyphenethylamine) is an organic chemical of the catecholamine and phenethylamine families. " + \
    "It functions both as a hormone and a neurotransmitter, and plays several important roles in the brain and body. "+ \
    "It is an amine synthesized by removing a carboxyl group from a molecule of its precursor chemical L-DOPA, "+ \
    "which is synthesized in the brain and kidneys. Dopamine is also synthesized in plants and most animals. "+ \
    "In the brain, dopamine functions as a neurotransmitter—a chemical released by neurons (nerve cells) to send signals "+ \
    "to other nerve cells. The brain includes several distinct dopamine pathways, one of which plays a major role in the motivational "+ \
    "component of reward-motivated behavior. The anticipation of most types of rewards increases the level of dopamine in the brain, "+ \
    "[2][failed verification] and many addictive drugs increase dopamine release or block its reuptake into neurons following release. "+ \
    "Other brain dopamine pathways are involved in motor control and in controlling the release of various hormones. " + \
    "These pathways and cell groups form a dopamine system which is neuromodulatory. "

model = "en_core_web_sm"

eng = spacy.load(model)
doc = eng(TEXT)

# tokens
print("tokens\n")
for token in doc:
    print("%s|\t, pos: %s, DEP: %s, ROOT: %s" % (token.text, token.pos_, token.dep_, token))

# entities
print("entities\n")
ents = [(e.text, e.label_, e.kb_id_) for e in doc.ents]
print(ents)

# noun chunks
for chunk in doc.noun_chunks:
    print("%s|\t ROOT: %s, DEP:%s, ROOT HEAD: %s" %(chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text))


def label_to_id(label):
    return re.sub('[^A-Za-z0-9_]+', '', label)

#Create a graph object
sent = next(doc.sents)
nodes = {}
edges = {}
for token in doc:
    if token.sent != sent:
        break

    #Creating the word instance
    node_id = str(token.idx)
    nodes[node_id] = {'data':{'label': str(token.text), 'id':node_id}}

    #Adding the lemma node if not existing
    lemma_id = label_to_id("_L_" + token.lemma_)
    if (lemma_id!="" and lemma_id not in nodes):
        nodes[lemma_id] = {'data':{'label': "[L]" + token.lemma_, 'id':lemma_id}}

    #edge between the tokens
    edge_id = label_to_id(str(token.head.idx)+"_"+ str(token.idx))
    if (edge_id not in edges):
        edges[edge_id] = {'data':{'id': edge_id, 'source': str(token.head.idx), 'target':str(token.idx), 'weight': 1 }}

    lemma_edge_id = label_to_id(token.head.lemma_+"_"+ token.lemma_)
    #edge between the lemmas
    if (lemma_edge_id in edges):
        updated_edge = edges[lemma_edge_id]
        updated_edge['data']['weight'] = updated_edge['data']['weight'] + 1
        edges[lemma_edge_id] = updated_edge
    else:
        source_id = label_to_id("_L_" + token.head.lemma_)
        target_id = label_to_id("_L_" + token.lemma_)
        edges[lemma_edge_id] = {'data':{'id': lemma_edge_id, 'source': source_id, 'target': target_id, 'weight': 1 }}

graph = list(nodes.values()) + list(edges.values())
with open(r'd:\temp\graph.json', 'w') as outfile:
    json.dump(graph, fp=outfile, indent=4)



