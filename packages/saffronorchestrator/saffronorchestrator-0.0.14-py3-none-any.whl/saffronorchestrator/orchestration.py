from searchdatamodels import Candidate
from pymongo.collection import Collection
from basilsweepercrawler.web_sweepers import run_external_web_sweeper
from nutmegredundancysolver import merge_redundant_candidates, LSA
from fastapi.encoders import jsonable_encoder
from rankexpansion import rank_candidates

import time


async def update_mongo(mongo_collection:Collection, candidate_list:list[Candidate], old_id_list:list[str]):
    for cand in candidate_list:
        mongo_collection.insert_one(jsonable_encoder(cand))
    for old_id in old_id_list:
        mongo_collection.update_one({"_id":old_id},{"$set":{"IsDuplicate": True}})
    print("Finished updating MongoDB at " + str(time.time()))


def candidate_search_flow(user_query:str, mongo_query:dict, mongo_collection:Collection, n_queries:int)-> list[Candidate]:
    '''The function `candidate_search_flow` takes a user query, a MongoDB query, a MongoDB collection, and
    the number of queries as input, and returns a list of ranked candidates based on the user query.
    
    Parameters
    ----------
    user_query : str
        The user's query, which is a string representing the search query entered by the user.
    mongo_query : dict
        The `mongo_query` parameter is a dictionary that specifies the query to be executed on the MongoDB
    collection. It is used to filter the candidates based on certain criteria.
    mongo_collection : Collection
        The `mongo_collection` parameter is an instance of the `Collection` class from the `pymongo`
    library. It represents a collection in a MongoDB database where candidate documents are stored.
    n_queries : int
        The parameter `n_queries` represents the desired number of candidates to be retrieved from the
    MongoDB collection. If the number of candidates retrieved from the collection is less than
    `n_queries`, additional candidates will be obtained through an external web sweep.
    
    Returns
    -------
        The function `candidate_search_flow` returns a list of ranked candidates.
    
    '''
    cursor=mongo_collection.aggregate([mongo_query, {
        "$project": {
          "Summary.Embedding":0,
          "score": { "$meta": "searchScore"}
        }
       },
       {"$sort": { "score": -1 }}])
    raw_mongo_candidate_list=list(cursor)
    print("Retrieved " + str(len(raw_mongo_candidate_list)) + " candidates from DB at " + str(time.time()))
    old_id_list=[raw_mongo_candidate["_id"] for raw_mongo_candidate in raw_mongo_candidate_list]
    print("Start extract candidate information at " + str(time.time()))
    for c in raw_mongo_candidate_list:
        print(c,['Name'], c['Summary'])
    candidate_list = []
    #for raw_mongo_candidate in raw_mongo_candidate_list:
    #    raw_mongo_candidate["_id"]=str(raw_mongo_candidate["_id"])
    #candidate_list=[Candidate(**raw_mongo_candidate) for raw_mongo_candidate in raw_mongo_candidate_list]
    print("Finished extract candidate information at " + str(time.time()))
    #if len(candidate_list) < n_queries:
    #    candidate_list+=run_external_web_sweeper([user_query], allowed_sites=["linkedin", "github"])
    #    candidate_list=merge_redundant_candidates(candidate_list,LSA)
    #    update_mongo(mongo_collection, candidate_list, old_id_list)
    print("Merged candidate list at " + str(time.time()))
    return candidate_list
    