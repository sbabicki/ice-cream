from fuzzywuzzy import fuzz
import numpy as np
import pandas as pd
import os

MAX_PER_CATEGORY = 5

pickle_dict = {}
unique_index = {}
filtered = ["filtered_adds", "filtered_ents", "filtered_peos"]
unfiltered = ["unfiltered_adds", "unfiltered_ents", "unfiltered_peos"]
canlii = ["canlii_party"]

for d in filtered + unfiltered + canlii:
    pickle_dict[d] = pd.read_pickle(os.path.join("data", "processed", d+".pickle"))
    unique_index[d] = np.array(pickle_dict[d].name.unique())
    print(f"{d} has {unique_index[d].size} unique entries")
    
def fuzzy_match(search, search_crit, base_fuzz=fuzz.ratio):
    search_df = pickle_dict[search_crit]
    scores = np.vectorize(lambda x : base_fuzz(x, search))(unique_index[search_crit])
    ind = np.argpartition(scores, -MAX_PER_CATEGORY)[-MAX_PER_CATEGORY:]
    ind = ind[np.argsort(-scores[ind])]
    return dict(zip(unique_index[search_crit][ind], scores[ind]))

def fuzzy_search(search, search_crit, base_fuzz=fuzz.ratio):
    scores = fuzzy_match(search, search_crit, base_fuzz=base_fuzz)
    search_df = pickle_dict[search_crit].set_index("name").loc[scores.keys()]
    search_df = search_df[:MAX_PER_CATEGORY]
    search_df["scores"] = scores.values()
    return search_df

def offshore_leaks_search_address(address):
    offshore_df = fuzzy_search(address, search_crit="filtered_adds")
    return offshore_df

def canlii_search_address(address):
    canlii_df = fuzzy_search(address, search_crit="canlii_party")
    return canlii_df

def offshore_leaks_search_entity(entity):
    offshore_df = pd.concat([fuzzy_search(entity, search_crit="filtered_ents"),
                             fuzzy_search(entity, search_crit="unfiltered_ents")],
                            axis=0).drop_duplicates()
    canlii_df = fuzzy_search(entity, search_crit="canlii_party")

    return offshore_df

def canlii_search_entity(entity):
    canlii_df = fuzzy_search(entity, search_crit="canlii_party")
    return canlii_df

def offshore_leaks_search_people(people):
    offshore_df = pd.concat([fuzzy_search(people, search_crit="filtered_peos"),
                             fuzzy_search(people, search_crit="unfiltered_peos")],
                            axis=0).drop_duplicates()
    canlii_df = fuzzy_search(people, search_crit="canlii_party")
    return offshore_df

def canlii_search_people(people):
    canlii_df = fuzzy_search(people, search_crit="canlii_party")
    return canlii_df
