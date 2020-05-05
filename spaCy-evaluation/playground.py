
import spacy
from spacy import displacy

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
for token in doc:
    print("text: %s, pos: %s, dep: %s" % (token.text, token.pos_, token.dep_))

# entities
for ent in doc.ents:
    print("text: %s, desc: %s" % (ent.text, ent.desc))


with open(r"d:\temp\temp.svg", "w") as f:
    f.write(displacy.render(next(doc.sents), style='dep'))
    
displacy.serve(next(doc.sents), style='dep')



