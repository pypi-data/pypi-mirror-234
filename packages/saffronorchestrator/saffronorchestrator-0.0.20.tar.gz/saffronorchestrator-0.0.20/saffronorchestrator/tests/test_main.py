import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'/saffronorchestrator')
from pymongo import MongoClient
from searchdatamodels import Candidate, WorkExperience, create_embedding, SearchTemplate
from fastapi.encoders import jsonable_encoder
from rankexpansion import generate_mongo_query_from_template_and_embedding
import unittest
import random
import string
from orchestration import candidate_search_flow
from unittest.mock import patch
import time

class BehaviorTest(unittest.TestCase):
    def setUp(self):
        ATLAS_URI='mongodb+srv://james2:vatVRC5XhsRL6KPV@cluster0.lh8qz.mongodb.net/?retryWrites=true&w=majority'
        client = MongoClient(ATLAS_URI)
        self.collection=client['test_db'].get_collection('unittest_candidate_collection')
        self.user_query="banker at goldman sachs"
        
        self.search_template=SearchTemplate(company=["goldman sachs"], title=["banker"])
        self.candidate_list=[
            Candidate(Name=''.join(random.choices(string.ascii_uppercase,k=4)), 
                      WorkExperienceList=[WorkExperience(Specialization="banker", Institution="goldman sachs")],
                      Sources=[''.join(random.choices(string.ascii_uppercase,k=20))]) for _ in range(10)
        ]
        self.embedding=create_embedding(self.user_query)
        n_deleted=self.collection.delete_many({})
        self.mongo_query=generate_mongo_query_from_template_and_embedding(self.embedding,10,self.search_template)
        time.sleep(3) #mongo can have race conditions with deleting/adding
    
    @patch('orchestration.run_external_web_sweeper')
    def test_database_complete(self,external_web_sweep_mock):
        '''
        GIVEN a user_query, and a mongoDB query_document, and a mongo db collection n_queries=10, and 10 candidates that match the mongodb query
        WHEN the 10 candidates are put into the collection, and we call candidate_search_flow
        THEN we should return the 10 candidates and NOT have called external_web_sweep
            and the candidates should be in the database but with different IDs
        '''
        #given
        external_web_sweep_mock.side_effect=Exception("should NOT have called external_web_sweep!!!")
        #when
        inserted_id_list=[self.collection.insert_one(jsonable_encoder(c)).inserted_id for c in self.candidate_list ]
        time.sleep(3)
        returned_candidate_list=candidate_search_flow(self.user_query, self.mongo_query, self.collection, 10)
        #then
        returned_candidate_name_set=set([c.Name for c in returned_candidate_list])
        candidate_name_set=set([c.Name for c in self.candidate_list])
        self.assertEqual(len(returned_candidate_name_set), len(candidate_name_set))
        for c_name in candidate_name_set:
            self.assertIn(c_name, returned_candidate_name_set)
        
        #cleanup
        for name in returned_candidate_name_set:
            self.collection.delete_one({"Name":name})
        return
    
    @patch('orchestration.run_external_web_sweeper')
    def test_database_incomplete(self,external_web_sweep_mock):
        '''
        GIVEN an user_query, and a mongoDB query_document, and a collection, n_queries=10, and 9 candidates that match the mongodb query
            and we have set a mock so basilsearchsweeper.external_web_sweep returns [candidate X]
        WHEN the 9 candidates are put into the database, and we call candidate_search_flow
        THEN we should return the 9 candidates + candidate X, and candidate X should be inserted into the collection
        ''' 
        external_web_sweep_mock.return_value=[self.candidate_list[0]]
        #when
        inserted_id_list=[self.collection.insert_one(jsonable_encoder(c)).inserted_id for c in self.candidate_list[1:] ]
        time.sleep(3)
        returned_candidate_list=candidate_search_flow(self.user_query, self.mongo_query, self.collection, 10)
        #then
        returned_candidate_name_set=set([c.Name for c in returned_candidate_list])
        candidate_name_set=set([c.Name for c in self.candidate_list])
        self.assertEqual(len(returned_candidate_name_set), len(candidate_name_set))
        for c_name in candidate_name_set:
            self.assertIn(c_name, returned_candidate_name_set)
        
        #cleanup
        for name in returned_candidate_name_set:
            self.collection.delete_one({"Name":name})
        return
    
    @patch('orchestration.run_external_web_sweeper')
    def test_database_empty(self,external_web_sweep_mock):
        '''
        GIVEN an user_query, and a mongoDB query_document, and a collection, n_queries=10, and 10 candidates
            and we have set a mock so basilsearchsweeper.external_web_sweep returns the 10 candidates
        WHEN we call candidate_search_flow
        THEN we should return the 10 candidates, and they should be inserted into the collection
        ''' 
        external_web_sweep_mock.return_value=self.candidate_list
        #when
        returned_candidate_list=candidate_search_flow(self.user_query, self.mongo_query, self.collection, 10)
        #then
        returned_candidate_name_set=set([c.Name for c in returned_candidate_list])
        candidate_name_set=set([c.Name for c in self.candidate_list])
        self.assertEqual(len(returned_candidate_name_set), len(candidate_name_set))
        for c_name in candidate_name_set:
            self.assertIn(c_name, returned_candidate_name_set)
        
        #cleanup
        for name in returned_candidate_name_set:
            self.collection.delete_one({"Name":name})
        return
    
    @patch('orchestration.run_external_web_sweeper')
    def test_database_incomplete_with_redundancy(self,external_web_sweep_mock):
        '''
        GIVEN an user_query, and a mongoDB query_document, and a collection, n_queries=20, and 10 candidates
            and we have set a mock so basilsearchsweeper.external_web_sweep returns the 10 candidates
        WHEN the 10 candidates have been put into the collection and we call candidate_search_flow
        THEN we should return the 10 candidates (redundant ones should have been removed)
        '''
        #given
        external_web_sweep_mock.return_value=self.candidate_list
        
        #when
        inserted_id_list=[self.collection.insert_one(jsonable_encoder(c)).inserted_id for c in self.candidate_list ]
        time.sleep(3)
        returned_candidate_list=candidate_search_flow(self.user_query, self.mongo_query, self.collection, 20)
        returned_candidate_list=[c for c in returned_candidate_list if c.IsDuplicate is False]
        
        #then
        returned_candidate_name_set=set([c.Name for c in returned_candidate_list])
        candidate_name_set=set([c.Name for c in self.candidate_list])
        self.assertEqual(len(returned_candidate_name_set), len(candidate_name_set))
        for c_name in candidate_name_set:
            self.assertIn(c_name, returned_candidate_name_set)
        
        #cleanup
        for name in returned_candidate_name_set:
            self.collection.delete_one({"Name":name})
        return
    
if __name__=='__main__':
    unittest.main()