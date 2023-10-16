import os
import sys
sys.path.append(os.getcwd())
from query_expansion import *
import unittest
from mongomock import MongoClient
import pymongo
import pprint
from searchdatamodels import *
from fastapi.encoders import jsonable_encoder
from unittest.mock import patch
import random

class QueryTest(unittest.TestCase):
    def test_generate_expanded_queries(self):
        user_query="fashion designer in paris"
        expanded_queries=generate_expanded_queries(user_query,5)
        print(expanded_queries)
        self.assertEqual(6, len(expanded_queries))

    def test_generate_expanded_queries_original(self):
        user_query = "data scientist in london"
        expanded_queries = generate_expanded_queries(user_query, 3)
        self.assertIn(user_query, expanded_queries)

    def test_generate_expanded_queries_unique(self):
        user_query = "civil engineer in berlin"
        expanded_queries = generate_expanded_queries(user_query, 4)
        self.assertEqual(len(expanded_queries), len(set(expanded_queries)))

    def test_get_search_template_from_query(self):
        '''
        GIVEN a user_query with location, school,major, title, company and skills
        WHEN we call get_search_template_from_query
        THEN we should get a SearchTemplate with the location, education, employment and skills
        '''
        location='san francisco'
        company='google'
        school='harvard'
        major='math'
        title='engineer'
        skill_0='java'
        skill_1='python'
        user_query=f"{title} at {company} who studied {major} at {school} located in {location}, skilled in {skill_0} and {skill_1}"
        search_template=get_search_template_from_query(user_query)
        self.assertIn(location, search_template.location)
        self.assertIn(company, search_template.company)
        self.assertIn(school, search_template.school)
        self.assertIn(major, search_template.major)
        self.assertIn(title, search_template.title)
        self.assertIn(skill_0, search_template.skill)
        self.assertIn(skill_1, search_template.skill)
        
    def test_expand_search_template_with_kg(self):
        '''
        GIVEN a search template with title, and skills already populated
        WHEN we call expand_search_template_with_kg
        THEN we should return a search template with title and skills expanded
        '''
        search_template=SearchTemplate(title=['software engineer'], skill=['coding'])
        expanded_search_template=expand_search_template_with_kg(search_template)
        print(expanded_search_template)
        self.assertLess(1, len(expanded_search_template.title))
        self.assertLess(1, len(expanded_search_template.skill))

    def test_generate_mongo_query_from_template_and_embedding(self):
        '''
        GIVEN an embedding and a search template
        WHEN we call generate_mongo_query_from_template_and_embedding
        THEN the function should return without error
        '''
        embedding=[random.random() for _ in range(384)]
        search_template=SearchTemplate(skill=["ballet","dance"])
        generate_mongo_query_from_template_and_embedding(embedding,5, search_template)

    def test_generate_mongo_query_from_none_and_embedding(self):
        '''
        GIVEN an embedding 
        WHEN we call generate_mongo_query_from_template_and_embedding without template
        THEN the function should return without error
        '''
        embedding=[random.random() for _ in range(384)]
        generate_mongo_query_from_template_and_embedding(embedding,5)

    def test_generate_mongo_query_from_empty_template_and_embedding(self):
        '''
        GIVEN an embedding and an empty search template
        WHEN we call generate_mongo_query_from_template_and_embedding
        THEN the function should return without error
        '''
        embedding=[random.random() for _ in range(384)]
        search_template=SearchTemplate()
        generate_mongo_query_from_template_and_embedding(embedding,5, search_template)


if __name__ =='__main__':
    unittest.main()
