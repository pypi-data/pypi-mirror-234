import os
import sys
sys.path.append(os.getcwd())
from sentence_transformers import SentenceTransformer
from talentiumkg import KnowledgeGraph
from typing import List
from searchdatamodels import Candidate, SearchTemplate
import spacy.cli
spacy.cli.download("en_core_web_sm")
import spacy

import re
import openai

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import numpy as np 

import math
from scipy import spatial

try:
    # Trying to find module in the parent package
    from .extraction_utils import *
except ImportError:
    print('Relative import failed')

try:
    # Trying to find module on sys.path
    from extraction_utils import *
except ModuleNotFoundError:
    print('Absolute import failed')

# Initialize the geocoder
geolocator = Nominatim(user_agent="location_expansion")

if "OPENAI_API_KEY" in os.environ:
    openai.api_key = os.environ["OPENAI_API_KEY"]

# Load the Sentence Transformers model for text embedding
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

# Load spaCy's English language model
nlp_spacy = spacy.load("en_core_web_sm")


knowledge_graph=KnowledgeGraph()

def cos_sim(embedding_0: list[float], embedding_1: list[float])->float:
    return 1- spatial.distance.cosine(embedding_0, embedding_1)

def rank_candidates(query: str, candidates: List[Candidate]) -> List[Candidate]:
    query_embedding = model.encode([query], convert_to_tensor=True)[0]

    for candidate in candidates:
        # Use the Summary embedding for comparison
        candidate_embedding = candidate.Summary.Embedding  
        if candidate_embedding is not None:
            # rank_score attribute should be addded to the candidate model
            similarity_score = cos_sim(query_embedding, candidate_embedding)
            candidate.RankScore = similarity_score
        else:
            # Set a default score for candidates without embeddings
            candidate.RankScore = 0.0  

    ranked_candidates = sorted(candidates, key=lambda c: c.RankScore, reverse=True)
    return ranked_candidates

# Get the top ranked candidates
def get_top_candidates(query: str, candidates: List[Candidate], k: int) -> List[Candidate]:
    
    # Calculate total scores for each candidate
    scored_candidates = [(candidate, calculate_total_score(query, candidate)) for candidate in candidates]

    # Sort the candidates based on their scores in descending order
    scored_candidates.sort(key=lambda x: x[1], reverse=True)
    
    # Return the top k candidates
    return [candidate for (candidate,_score) in scored_candidates[:k]]


# Define helper functions for the weighting algorithm

# Location expansion using geopy
def get_expanded_locations_geopy(query_locations: List[str], max_distance_km: float = 100.0) -> List[str]:
    '''The function `get_expanded_locations_geopy` takes a list of query locations and a maximum distance
    in kilometers, and for each query_location inn query_locations returns 
    the address of the query_location + sometimes other locations
    ex: ["london"] -> ["Westminster Muslim Cultural Centre, 30, Winchester Street, Pimlico, London, Greater London, England, SW1V 4ND, United Kingdom"]
    
    Parameters
    ----------
    query_locations : List[str]
        A list of locations for which you want to find nearby locations.
    max_distance_km : float
        The `max_distance_km` parameter is the maximum distance in kilometers within which nearby locations
    should be considered. Only locations within this distance from the query location will be added to
    the expanded list.
    
    Returns
    -------
        list of addresses.
    
    '''
    expanded_locations = []

    # Iterate through the query locations and find their coordinates
    for query_location in query_locations:
        location = geolocator.geocode(query_location)
        if location:
            query_coords = (location.latitude, location.longitude)

            # Find nearby locations; this usually just gets one location though
            nearby_locations = geolocator.reverse(query_coords, exactly_one=False)

            # Add the nearby locations within the specified distance to the expanded list
            for nearby_loc in nearby_locations:
                nearby_coords = (nearby_loc.latitude, nearby_loc.longitude)
                distance_km = geodesic(query_coords, nearby_coords).kilometers
                if distance_km <= max_distance_km:
                    expanded_locations.append(nearby_loc.address)

    return expanded_locations

# Location expansion using llm
def get_expanded_locations_llm(query_locations: List[str], max_distance_km: float = 100.0, max_limit: int = 5, include_state: bool = False) -> List[str]:
    '''takes a list of query locations and returns a list of
    major cities within a specified distance from each query location according to the text-davinci-003 model (GPT-3).
    
    Parameters
    ----------
    query_locations : List[str]
        A list of query locations for which you want to generate expanded locations.
    max_distance_km : float
        The `max_distance_km` parameter specifies the maximum distance in kilometers within which we want
    to find major cities. It is set to a default value of 100.0 kilometers.
    max_limit : int, optional
        The `max_limit` parameter determines the maximum number of expanded locations to include for each
    query location. By default, it is set to 5, meaning that the function will return up to 5 expanded
    locations for each query location.
    include_state : bool, optional
        The `include_state` parameter is a boolean flag that determines whether the expanded locations
    should include the state information or not. If `include_state` is set to `True`, the expanded
    locations will include both the city name and the state.
    
    Returns
    -------
        The function `get_expanded_locations_llm` returns a list of expanded locations.
    
    '''
    expanded_locations = []

    # Generate expanded locations for each query location
    for query_location in query_locations:
        # Keep it simple so that we remain at city level granularity
        prompt = f"Given the query location '{query_location}', provide a list of major cities within {max_distance_km} km radius.\n\nList:"

        # Generate the expanded locations using the OpenAI API
        response = openai.Completion.create(
            temperature=0,
            engine="text-davinci-003",  
            prompt=prompt,
            max_tokens=50,  
            stop=None  
        )

        # Parse the generated response to extract the expanded locations
        expanded_locations_query = response.choices[0].text.strip().split("\n")[:max_limit]
        
        # Remove numbering from the generated locations
        expanded_locations_query = [re.sub(r'^\d+\.\s*', '', location) for location in expanded_locations_query]
        
        # Extract only the city name before the first comma
        if not include_state:
          expanded_locations_query = [location.split(',')[0].strip() for location in expanded_locations_query]

        expanded_locations.extend(expanded_locations_query)

    return expanded_locations



# Calculate the skill match score between the required skills and candidate skills
def calculate_skill_match_score(extracted_skills: List[str], candidate_skills: List[str]) -> float:
    '''calculates a skill match score between two lists of skills by considering both direct
    matches and cosine similarities between skill embeddings.
    
    Parameters
    ----------
    extracted_skills : List[str]
        A list of skills extracted from a job description or a candidate's profile.
    candidate_skills : List[str]
        The parameter "candidate_skills" represents a list of skills possessed by a candidate. These skills
    are typically mentioned in a resume or job application.
    
    Returns
    -------
        returns a float value representing the total match score
    between the extracted skills and candidate skills.
    
    '''

    # Calculate direct match score
    direct_match_score = len(set(extracted_skills).intersection(candidate_skills)) / len(extracted_skills)

    # Encode the skill lists into embeddings
    extracted_skills_embeddings = model.encode(extracted_skills, convert_to_tensor=True)
    candidate_skills_embeddings = model.encode(candidate_skills, convert_to_tensor=True)

    # Calculate all possible cosine similarities between candidate and extracted query skills
    expanded_match_scores = []
    for extracted_embedding in extracted_skills_embeddings:
        for candidate_embedding in candidate_skills_embeddings:
            expanded_match_scores.append(cos_sim(extracted_embedding, candidate_embedding))
   
    # Calculate the average cosine similarity
    avg_expanded_match_score = np.mean(expanded_match_scores)

    # Calculate total match score as a weighted sum of direct and expanded match scores
    # Weights can be modified
    total_match_score = 0.6 * direct_match_score + 0.4 * avg_expanded_match_score

    return total_match_score

    
# Calculate the location match score
def calculate_location_match_score(query_location: List[str], expanded_locations: List[str], candidate_location: str) -> float:
    '''The function calculates a location match score based on the query location, expanded locations, and
    candidate location, taking into account direct matches and proximity to expanded locations.
    
    Parameters
    ----------
    query_location : List[str]
        A list of strings representing the locations specified in the query. For example, if the query is
    "restaurants in New York", the query_location would be ["New York"].
    expanded_locations : List[str]
        A list of nearby locations that have been expanded from the original query location via LLM.
    candidate_location : str
        The candidate_location parameter is the location that you want to calculate the match score for. It
    is a string representing the candidate's location.
    
    Returns
    -------
        the total score
    
    '''
    # Initialize the geolocator
    geolocator = Nominatim(user_agent="location_match_score")
    
    # Get the coordinates of the candidate's location
    candidate_coords = geolocator.geocode(candidate_location) if candidate_location else None
    
    # Calculate direct match score
    direct_match_score = 1.0 if candidate_location in query_location else 0.0
    
    # Initialize closest_distance with a high value
    closest_distance = float("inf")
    
    # Calculate the closest distance between candidate location to expanded locations
    for expanded_loc in expanded_locations:
        expanded_coords = geolocator.geocode(expanded_loc)
        if expanded_coords and candidate_coords:
            distance = geodesic(candidate_coords.point, expanded_coords.point).kilometers
            closest_distance = min(closest_distance, distance)
    
    # Initialize expanded location score
    expanded_location_score = 0.0
    
    # Calculate expanded location score if candidate_coords is available and distance is within 300 km
    # the score decreases exponentially as we move away from the exact location,
    # and drops down to 0 after 300 km
    if candidate_coords and closest_distance <= 300.0:
        expanded_location_score = math.exp(-0.01 * closest_distance)
    
    # Calculate total score using a weighted combination of direct and expanded scores
    total_score = 0.7 * expanded_location_score + 0.3 * direct_match_score
    return total_score
    

# Calculate the extent of relevance between the query and a candidate's profile
def calculate_similarity_score(query: str, candidate: Candidate) -> float:
    '''The function encodes the provided text (query and candidate's summary) into embeddings using a 
    pre-trained model. Then, the cosine similarity between these embeddings is computed to determine
    the relevance or similarity between the query and the candidate's profile summary.

    Parameters
    ----------
    query : str
        A text string representing the query or the reference text against which the similarity 
        is to be computed.

    candidate : Candidate
        An object representing the candidate's profile. The profile includes a summary, which
        contains both the text and its corresponding embedding. If the embedding is not available,
        the summary text is encoded to produce it.

    Returns
    -------
    float
        The cosine similarity score between the query embedding and the candidate's summary embedding. 
        The score ranges between -1 (completely dissimilar) and 1 (completely similar). 

    '''
    if candidate.Summary.Embedding is None:
        # Encode the candidate's summary
        candidate_embedding = model.encode([candidate.Summary.Text], convert_to_tensor=True)[0]
        candidate.Summary.Embedding = candidate_embedding
    
    # Encode the query
    query_embedding = model.encode([query], convert_to_tensor=True)[0]
    
    # Calculate the cosine similarity score between query and candidate embeddings
    similarity_score = cos_sim(query_embedding, candidate.Summary.Embedding)
    
    return similarity_score



# Final score calculation
def calculate_total_score(query: str, candidate: Candidate) -> float:
    '''The function calculates the total score for a candidate based on the similarity score, location
    match score, and skill match score (if applicable).
    
    Parameters
    ----------
    query : str
        The query parameter is a string that represents the search query. It is used to
    find the similarity between the query and the candidate's profile.
    candidate : Candidate
        The `candidate` parameter is an object of the `Candidate` class. It likely contains information
    about a candidate for a job position, such as their skills, location, and other relevant details.
    
    Returns
    -------
        a float value representing the total score calculated based on the similarity score, location match
    score, and skill match score.
    
    '''
    # Calculate similarity score
    similarity_score = calculate_similarity_score(query, candidate)
    
    # Extract query locations and expanded locations
    # Include query_locations within query_expanded_locations as well
    query_locations = extract_location_mentions_spacy(query)
    query_expanded_locations = get_expanded_locations_llm(query_locations)
    
    # Calculate location match score
    if len(query_locations)>0 and candidate.Location is True:
        location_match_score = calculate_location_match_score(query_locations, query_expanded_locations, candidate.Location)

    
    # Extract query skills

    query_skills = extract_skills(query)
    
    # Calculate skill match score
    if len(query_skills)>0 and len(candidate.Skills)>0:
        skill_match_score = calculate_skill_match_score(query_skills, candidate.Skills)
    
    # Define weights for each component
    similarity_weight = 0.4
    location_weight = 0.3
    skill_weight = 0.3
    
    # Calculate total score
    # Weights can be adjusted
    if len(query_skills)>0 and len(candidate.Skills)>0 and len(query_locations)>0 and candidate.Location is True:
        total_score = similarity_weight * similarity_score + location_weight * location_match_score + skill_weight * skill_match_score
    elif len(query_skills) > 0 and len(candidate.Skills) > 0:
        total_score = (similarity_weight * similarity_score + skill_weight * skill_match_score)/(similarity_weight+ skill_weight)
    elif len(query_locations)>0 and candidate.Location is True:
        total_score =(similarity_weight * similarity_score + location_weight * location_match_score)/(similarity_weight+ location_weight)
    else:
        total_score=similarity_weight * similarity_score
    
    return total_score


def calculate_total_score_kg(query: str, template: SearchTemplate, candidate: Candidate) -> float:
    if len(template.skill) == 0:
        return calculate_total_score(query, candidate)

    similarity_score = calculate_similarity_score(query, candidate)
    skill_score = knowledge_graph.compute_skill_score(template.skill, candidate.Skills)

    # Define weights for each component
    similarity_weight = 0.5
    skill_weight = 0.5

    return similarity_score * similarity_weight + skill_score * skill_weight