import os
import sys
sys.path.append(os.getcwd())
from extraction_utils import *
import unittest
from unittest.mock import patch
from munch import DefaultMunch

class OpenAIResponseMock:
    def __init__(self,text):
        self.choices=[DefaultMunch.fromDict({"text":text})]

class ExtractingTest(unittest.TestCase):
    def setUp(self):
        self.location_query="who was in paris or rome"
        self.bad_json_str="bad json string} ^[jkksd]\'__ 0"
        self.bad_openai_response=OpenAIResponseMock(self.bad_json_str)

    def test_extract_location_mentions_spacy(self):
        locations=extract_location_mentions_spacy(query=self.location_query)
        self.assertTrue("paris" in locations)
        self.assertTrue("rome" in locations)

    def test_extract_location_mentions_llm(self):
        locations=extract_location_mentions_llm(self.location_query)
        self.assertTrue("paris" in locations)
        self.assertTrue("rome" in locations)

    def test_extract_skills(self):
        query="find me someone proficient in metallurgy and welding"
        skills=extract_skills(query)
        self.assertTrue("metallurgy" in skills)
        self.assertTrue("welding" in skills)

    def test_extract_education_empty(self):
        query="hello"
        education=extract_education(query=query)
        self.assertEqual(0, len(education))

    def test_extract_education(self):
        degree_0="phd"
        degree_1="masters"
        major_0="chemistry"
        major_1="neuroscience"
        school_0="oxford university"
        school_1="cambridge university"
        target_list=[degree_0, degree_1, major_0, major_1, school_0, school_1]
        for x in range(len(target_list)):
            text="find me someone"
            if x>=0:
                text+=f" with a {degree_0}"
            if x>=1:
                text+=f" or a {degree_1}"
            if x>=2:
                text+=f" in {major_0}"
            if x>=3:
                text+=f" or {major_1}"
            if x>=4:
                text+=f" who attended {school_0}"
            if x>=5:
                text+=f" or {school_1}"
            with self.subTest(text=text):
                education_dict=extract_education(query=text)
                if x>=0:
                    self.assertIn("Degree", education_dict)
                    self.assertIn(degree_0, education_dict["Degree"])
                if x>=1:
                    self.assertIn(degree_1, education_dict["Degree"])
                if x>=2:
                    self.assertIn("Specialization", education_dict)
                    self.assertIn(major_0, education_dict["Specialization"])
                if x>=3:
                    self.assertIn(major_1, education_dict["Specialization"])
                if x>=4:
                    self.assertIn("Institution", education_dict)
                    self.assertIn(school_0, education_dict["Institution"])
                if x>=5:
                    self.assertIn(school_1, education_dict["Institution"])

    def test_extract_employment_empty(self):
        query="good afternoon"
        employment_dict=extract_employment(query)
        self.assertEqual(0, len(employment_dict))

    def test_extract_employment(self):
        title_0="engineer"
        title_1="developer"
        company_0="google"
        company_1="microsoft"
        target_list=[title_0, title_1, company_0, company_1]
        for x in range(len(target_list)):
            query="find me a person "
            if x>=0:
                query+=f" who worked as an {title_0}"
            if x>=1:
                query+=f" or a {title_1}"
            if x>=2:
                query+=f" at {company_0}"
            if x>=3:
                query+=f" or {company_1}"
            with self.subTest(query=query):
                employment_dict=extract_employment(query)
                if x>=0:
                    self.assertIn("Specialization", employment_dict)
                    self.assertIn( title_0,employment_dict["Specialization"])
                if x>=1:
                    self.assertIn(title_1,employment_dict["Specialization"])
                if x>=2:
                    self.assertIn("Institution", employment_dict)
                    self.assertIn(company_0,employment_dict["Institution"])
                if x>=3:
                    self.assertIn(company_1,employment_dict["Institution"])

    @patch("extraction_utils.openai.Completion.create")
    def test_extract_error(self,openai_Completion_create_mock):
        openai_Completion_create_mock.return_value=self.bad_openai_response
        for function in [extract_education, extract_employment]:
            with self.subTest(function=function):
                try:
                    function("any query")
                except Exception as exception:
                    self.assertIsInstance(exception, json.decoder.JSONDecodeError)
                    print(exception.msg)
                    self.assertNotEqual(-1, exception.msg.find(self.bad_json_str))




if __name__=='__main__':
    unittest.main()