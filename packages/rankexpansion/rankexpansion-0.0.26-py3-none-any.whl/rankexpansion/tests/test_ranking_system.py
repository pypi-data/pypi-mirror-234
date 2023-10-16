import os
import sys
sys.path.append(os.getcwd())
from ranking_system import *
from searchdatamodels import *
import unittest
    

class RankingTest(unittest.TestCase):
    def setUp(self):
        self.location_query="who was in paris or rome"
    def test_rank_candidates(self):
        correct_name="Indiana Jones"
        candidate_list=[
            Candidate(Name="Rick Deckard", WorkExperienceList=[WorkExperience(Specialization="policeman", Institution="Los Angeles Police Department")] ),
            Candidate(Name=correct_name, WorkExperienceList=[WorkExperience(Specialization="history professor", Institution="University of Chicago")]),
            Candidate(Name="Han Solo", WorkExperienceList=[WorkExperience(Specialization="Smuggler", Institution="Self-Employed")])
        ]
        ranked_candidates= rank_candidates("professor", candidates=candidate_list)
        self.assertEqual(ranked_candidates[0].Name, correct_name.lower())

    def test_expand_locations_none(self):
        query_locations=["switzerland and canada"]
        expanded_locations=get_expanded_locations_geopy(query_locations)
        self.assertEqual(0, len(expanded_locations))

    def test_get_expanded_locations_geopy(self):
        query_locations=["zurich, switzerland"]
        expanded_locations=get_expanded_locations_geopy(query_locations)
        self.assertEqual(1, len(expanded_locations))

    def test_get_expanded_locations_llm(self):
        query_locations=["zurich"]
        expanded_locations=get_expanded_locations_llm(query_locations)
        self.assertTrue("Basel" in expanded_locations)

    def test_get_expanded_locations_llm_state(self):
        query_locations=["zurich"]
        expanded_locations=get_expanded_locations_llm(query_locations, include_state=True)
        self.assertTrue("Basel, Switzerland" in expanded_locations)

    def test_calculate_skill_match_score_same(self):
        skills=["dance"]
        score=calculate_skill_match_score(skills,skills)
        self.assertEqual(1, score)

    def test_calculate_skill_match_score(self):
        extracted_skills=["teaching", "writing"]
        good_candidate_skills=["education", "literature"]
        bad_candidate_skills=["marksmanship", "hunting"]
        good_score=calculate_skill_match_score(extracted_skills, good_candidate_skills)
        bad_score=calculate_skill_match_score(extracted_skills, bad_candidate_skills)
        self.assertGreater(good_score, bad_score)

    def test_calculate_location_match_score_same(self):
        locations=["madrid"]
        candidate_location='madrid'
        score=calculate_location_match_score(locations, locations, candidate_location)
        self.assertEqual(1, score)

    def test_calculate_location_match_score(self):
        query_location=["not real location"]
        good_locations=["amsterdam"]
        bad_locations=["berlin"]
        candidate_location='brussels'
        good_score=calculate_location_match_score(query_location, good_locations, candidate_location)
        bad_score=calculate_location_match_score(query_location, bad_locations, candidate_location)
        self.assertGreater(good_score, bad_score)

    def test_calculate_similarity_score(self):
        good_candidate=Candidate(Name="Jay Carter", WorkExperienceList=[WorkExperience(Specialization="Rapper")])
        bad_candidate=Candidate(Name="Jimmy Carter", WorkExperienceList=[WorkExperience(Specialization="President")])
        query="musician"
        good_score=calculate_similarity_score(query, good_candidate)
        bad_score=calculate_similarity_score(query, bad_candidate)
        self.assertGreater(good_score, bad_score)

    def test_calculate_total_score_no_location_no_skills(self):
        good_candidate=Candidate(Name="Jay Carter", WorkExperienceList=[WorkExperience(Specialization="Rapper")])
        bad_candidate=Candidate(Name="Jimmy Carter", WorkExperienceList=[WorkExperience(Specialization="President")])
        query="musician"
        good_score=calculate_total_score(query, good_candidate)
        bad_score=calculate_total_score(query, bad_candidate)
        self.assertGreater(good_score, bad_score)

    def test_calculate_total_score_no_location(self):
        good_candidate=Candidate(Name="Jay Carter", WorkExperienceList=[WorkExperience(Specialization="Rapper")], Skills=["singing", "dancing"])
        bad_candidate=Candidate(Name="Jimmy Carter", WorkExperienceList=[WorkExperience(Specialization="President")], Skills=["speaking"])
        query="musician skilled in singing"
        good_score=calculate_total_score(query, good_candidate)
        bad_score=calculate_total_score(query, bad_candidate)
        self.assertGreater(good_score, bad_score)

    def test_calculate_total_score_no_skills(self):
        good_candidate=Candidate(Name="Jay Carter", WorkExperienceList=[WorkExperience(Specialization="Rapper")], Location="New York City")
        bad_candidate=Candidate(Name="Jimmy Carter", WorkExperienceList=[WorkExperience(Specialization="President")], Location="Washington DC")
        query="musician located in manhattan"
        good_score=calculate_total_score(query, good_candidate)
        bad_score=calculate_total_score(query, bad_candidate)
        self.assertGreater(good_score, bad_score)

    def test_calculate_total_score(self):
        good_candidate=Candidate(Name="Jay Carter", WorkExperienceList=[WorkExperience(Specialization="Rapper")], Location="New York City",Skills=["singing", "dancing"])
        bad_candidate=Candidate(Name="Jimmy Carter", WorkExperienceList=[WorkExperience(Specialization="President")], Location="Washington DC",Skills=["speaking"])
        query="musician located in manhattan skilled in singing"
        good_score=calculate_total_score(query, good_candidate)
        bad_score=calculate_total_score(query, bad_candidate)
        self.assertGreater(good_score, bad_score)

    def test_get_top_candidates(self):
        correct_name="Indiana Jones"
        candidate_list=[
            Candidate(Name="Rick Deckard", WorkExperienceList=[WorkExperience(Specialization="policeman", Institution="Los Angeles Police Department")] ),
            Candidate(Name=correct_name, WorkExperienceList=[WorkExperience(Specialization="history professor", Institution="University of Chicago")]),
            Candidate(Name="Han Solo", WorkExperienceList=[WorkExperience(Specialization="Smuggler", Institution="Self-Employed")])
        ]
        ranked_candidates= get_top_candidates("professor", candidates=candidate_list,k=3)
        self.assertEqual(ranked_candidates[0].Name, correct_name.lower())


if __name__ =='__main__':
    unittest.main()