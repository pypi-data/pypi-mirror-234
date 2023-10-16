import os
import sys
sys.path.append(os.getcwd())
from talentiumkg import KnowledgeGraph
import openai
from searchdatamodels import SearchTemplate
from typing import List
try:
    # Trying to find module in the parent package
    from .extraction_utils import *
    from .ranking_system import *
except ImportError:
    print('Relative import failed')

try:
    # Trying to find module on sys.path
    from extraction_utils import *
    from ranking_system import *
except ModuleNotFoundError:
    print('Absolute import failed')

if "OPENAI_API_KEY" in os.environ:
    openai.api_key = os.environ["OPENAI_API_KEY"]
    #for local testing, add the openai api_key to your env
    #otherwise make sure that you set your openai api_key before you use this library
INSTITUTION='Institution'
SPECIALIZATION="Specialization"
knowledge_graph=KnowledgeGraph()

# generate a set of queries similar to the original
def generate_expanded_queries(query: str, num_queries: int = 5) -> List[str]:
    '''The `generate_expanded_queries` function takes a user's search query and generates a list of similar
    queries that are relevant to the original context, such as similar job titles, nearby locations, and
    similar skills.
    
    Parameters
    ----------
    query : str
        The `query` parameter is a string that represents the user's search query. It is the original query
    for which we want to generate similar queries.
    num_queries : int, optional
        The `num_queries` parameter specifies the number of similar queries that should be generated. By
    default, it is set to 5, but you can change it to any positive integer value.
    
    Returns
    -------
        The function `generate_expanded_queries` returns a list of similar queries that are relevant to the
    original query context. The list includes `num_queries` similar queries, as well as the original
    query itself.
    
    '''
    prompt = (
        f"Given a user's search query, generate a list of {num_queries} similar queries that are relevant to the original context [similar job title, nearby location, similar skills].\n\n"
        "Examples:\n"
        "1. Input Query: \"Software engineer in New York\"\n"
        "   [\"Software Development Engineer in New York\", \"Software developer in New York\", \"SDE in Jersey City\" ]\n\n"
        "2. Input Query: \"Remote Data Scientist\"\n"
        "   [\"Remote Data Science Engineer\", \"Work from home Data Scientist\"]\n\n"
        "3. Input Query: \"Entry-level software developer\"\n"
        "   [\"Software engineering intern\", \"Junior software engineer\"]\n\n"
        "4. Input Query: \"Experienced software engineer\"\n"
        "   [\"Senior software engineer\", \"Software Architect\"]\n\n"
        "5. Input Query: \"Software development careers\"\n"
        "   [\"Software engineering job paths\", \"Career options in software development\"]\n\n"
        f"Input Query: \"{query}\"\n"
    )

    
    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=prompt,
        max_tokens=200,
        stop=None,
        temperature=0,
        n=num_queries,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )

    expanded_text = response.choices[0]['text']
    print(expanded_text)

    # Find the start index of the list
    result_list_start = expanded_text.index("[")  

    # Find the end index of the list
    result_list_end = expanded_text.index("]")  

    # extract the result
    result_list_str = expanded_text[result_list_start:result_list_end+1] 
    result_list = eval(result_list_str) 

    # add original query as well
    result_list.append(query)

    return result_list


def get_search_template_from_query(user_query:str) -> SearchTemplate:
    '''The function extracts information from a user query to create a search template for employment and
    education.
    
    Parameters
    ----------
    user_query : str
        The user_query parameter is a string that represents the user's search query. It is the input
    provided by the user when they are searching for something.
    

    Returns
    -------
    SearchTemplate
        an instance of the SearchTemplate class properly formatted
    '''
    employment_dict=extract_employment(user_query)
    title_list=[]
    company_list=[]
    if INSTITUTION in employment_dict:
        company_list=employment_dict[INSTITUTION]
    if SPECIALIZATION in employment_dict:
        title_list=employment_dict[SPECIALIZATION]
    
    education_dict=extract_education(user_query)
    school_list=[]
    major_list=[]
    if INSTITUTION in education_dict:
        school_list=education_dict[INSTITUTION]
    if SPECIALIZATION in education_dict:
        major_list=education_dict[SPECIALIZATION]
    location_list=extract_location_mentions_llm(user_query)
    skill_list=extract_skills(user_query)

    return SearchTemplate(location=location_list, 
                          skill=skill_list, title=title_list, 
                          company=company_list, 
                          school=school_list, 
                          major=major_list)



def expand_search_template_with_kg(search_template: SearchTemplate) -> SearchTemplate:
    knowledge_graph=KnowledgeGraph()
    new_skill_set=set(search_template.skill)
    for single_skill in search_template.skill:
        new_skill_set.update(knowledge_graph.infer_similar_skill(single_skill))
    new_title_set=set(search_template.title)
    for single_title in search_template.title:
        new_title_set.update(knowledge_graph.infer_similar_job_title(single_title))
    search_template.skill=[s for s in new_skill_set]
    search_template.title=[t for t in new_title_set]
    return search_template


def generate_mongo_query_from_template_and_embedding(embedding: list[float],k:int,template: SearchTemplate=None)->dict:
    '''The function generates a MongoDB query based on a given template and embedding.
    
    Parameters
    ----------
    embedding : list[float]
        The `embedding` parameter is a list of floats representing a vector embedding of a document or
    query. It is used to find similar documents based on their embeddings.
    template : SearchTemplate
        The `template` parameter is an instance of the `SearchTemplate` class. It contains the search
    criteria for the query, such as titles, locations, skills, and majors.
    
    Returns
    -------
        a dictionary that represents a MongoDB query.
    
    '''
    if template == None or (template.title==[] and template.location==[] and template.skill==[] and template.major==[]):
        res = {"$search":{
        "index": "default",
        "knnBeta": {
        "vector": embedding,
        "path": "Embedding",
        "k": k,
        }}}
    else:
        can_filter = {"compound":{}}
        can_filter["compound"]["must"] = []
        if len(template.title) > 0:
            can_filter["compound"]["must"].append({"compound": {"should": []}})
        for title in template.title:
            can_filter['compound']['must'][-1]['compound']['should'].append({
                  "phrase": {
                    "path": ["WorkExperienceList.Specialization", "Summary.Text"],
                    "query": title,
                  }
                })
        if len(template.location) > 0:
            can_filter["compound"]["must"].append({"compound": {"should": []}})
        for location in template.location:
            can_filter['compound']['must'][-1]['compound']['should'].append({
                  "phrase": {
                    "path": "Location",
                    "query": location,
                  }
                })
        if len(template.skill) > 0:
            can_filter["compound"]["must"].append({"compound": {"should": []}})
        for skill in template.skill:
            can_filter['compound']['must'][-1]['compound']['should'].append({
                  "phrase": {
                    "path": ["Skills", "Summary.Text"],
                    "query": skill,
                  }
                })
        if len(template.major) > 0:
            can_filter["compound"]["must"].append({"compound": {"should": []}})
        for major in template.major:
            can_filter['compound']['must'][-1]['compound']['should'].append({
                  "phrase": {
                    "path": ["EducationExperienceList.Specialization", "Summary.Text"],
                    "query": major,
                  }
                })
        res = {"$search":{
        "index": "default",
        "knnBeta": {
        "vector": embedding,
        "path": "Embedding",
        "k": k,
        "filter": can_filter
          }}}
    return res