import re
import spacy

from itertools import chain
from bisect import bisect
from collections import Counter


def shrink_nonword_idx(entity_list, nonword_tokens):
    """Get entity position, discounting non-word tokens"""

    for i in entity_list:
        shrinkage = bisect(nonword_tokens, i["idx"])
        i["idx_n"] = i["idx"] - shrinkage


def ner_model(scraped_text, spacy_model="en_core_web_sm"):
    """Run NER model on text"""

    scraped_text = re.sub(r'\s+', ' ', scraped_text)    # sanitise whitespace characters
    
    nlp_model = spacy.load(spacy_model)
    doc = nlp_model(scraped_text)

    return doc


def collect_entities(doc):
    """Format entities data"""

    # Locate entities
    person_entities = [{"name": i.text.removesuffix("'s"), "idx": i.start} for i in doc.ents if i.label_ == "PERSON"]
    loc_entities = [{"name": i.text, "idx": i.start}  for i in doc.ents if i.label_ in ["LOC", "GPE", "FAC"]]

    nonword_tokens = [[j for j in i if j.is_space or j.is_punct] for i in doc.sents]
    nonword_tokens = [token.i for token in chain.from_iterable(nonword_tokens)]    # index for non-word tokens

    # Create formatted dict for entities
    if person_entities:
        shrink_nonword_idx(person_entities, nonword_tokens)

        # Count for person entities
        entity_dict = dict(Counter([i["name"] for i in person_entities]).most_common())
        entity_dict = {k: {"count": v, "associated_places": []} for k,v in entity_dict.items()}

        if loc_entities:
            shrink_nonword_idx(loc_entities, nonword_tokens)

            # Compare place name entities loc with person entities loc
            for person in person_entities:
                for place in loc_entities:
                    idx_diff = abs(person["idx_n"] - place["idx_n"])
                    if idx_diff <= 100:
                        entity_dict[person["name"]]["associated_places"].append(place["name"])

            # Format dict - with associated_places
            final_entity_dict = [{
                "name": k,
                "count": v["count"],
                "associated_places": dict(Counter(v["associated_places"]).most_common())
                } for k,v in entity_dict.items()]
            
            for entry in final_entity_dict:
                if entry["associated_places"]:
                    places_new = [{"name": k, "count": v} for k,v in entry["associated_places"].items()]
                    entry["associated_places"] = places_new
                else:
                    entry["associated_places"] = []
            
        else:
            # Format dict - without associated_places
            final_entity_dict = [{"name": k, "count": v["count"]} for k,v in entity_dict.items()]

        return final_entity_dict

    else:
        return []
    
    