from searchdatamodels import Candidate
from pymongo.collection import Collection
from basilsweepercrawler.web_sweepers import run_external_web_sweeper
from nutmegredundancysolver import merge_and_update_redundant_candidate_list, LSA
from fastapi.encoders import jsonable_encoder
from rankexpansion import rank_candidates

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
    cursor=mongo_collection.aggregate([mongo_query])
    raw_mongo_candidate_list=list(cursor)
    old_id_list=[raw_mongo_candidate["_id"] for raw_mongo_candidate in raw_mongo_candidate_list]
    for raw_mongo_candidate in raw_mongo_candidate_list:
        raw_mongo_candidate["Id"]=raw_mongo_candidate["_id"]
        del raw_mongo_candidate["_id"]
    candidate_list=[Candidate(**raw_mongo_candidate) for raw_mongo_candidate in raw_mongo_candidate_list]
    if len(candidate_list) < n_queries:
        external_candidate_list=run_external_web_sweeper([user_query], allowed_sites=["linkedin", "github"])
        for external_candidate in external_candidate_list:
            if external_candidate.Id ==None:
                insert_result=mongo_collection.insert_one(jsonable_encoder(external_candidate))
                external_candidate.Id=insert_result.inserted_id
        candidate_list+=external_candidate_list
    candidate_list=merge_and_update_redundant_candidate_list(candidate_list,mongo_collection, LSA)
    return rank_candidates(user_query, candidate_list)
    