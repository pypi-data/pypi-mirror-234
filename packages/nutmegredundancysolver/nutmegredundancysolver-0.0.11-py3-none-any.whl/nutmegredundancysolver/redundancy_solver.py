from searchdatamodels import *
try:
    # Trying to find module in the parent package
    from .description_synthesis import *
except ImportError:
    print('Relative import failed')

try:
    # Trying to find module on sys.path
    from description_synthesis import *
except ModuleNotFoundError:
    print('Absolute import failed')

from typing import List
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from pymongo.collection import Collection
from fastapi.encoders import jsonable_encoder


def merge_experiences(experience_0:GeneralExperience, experience_1: GeneralExperience, summary_name: str) -> GeneralExperience:
    '''The function `merge_experiences` takes two experiences and a summary name as input, merges the
    experiences together, and returns a new experience with the merged information. raises error if not the same 
    type of experience
    
    Parameters
    ----------
    experience_0 : GeneralExperience
        The first experience to merge. It should be of type GeneralExperience or EducationExperience.
    experience_1 : GeneralExperience
        The parameter `experience_1` is an instance of the `GeneralExperience` or EducationExperience.
    summary_name : str
        The `summary_name` parameter is a string that represents the name of the summary you want to
    generate from the merged experiences.
    
    Returns
    -------
        The function `merge_experiences` returns a `GeneralExperience` object.
    
    '''
    if isinstance(experience_0, EducationExperience)!= isinstance(experience_0, EducationExperience):
        raise Exception("experiences are not same type! got types {} {}".format(type(experience_0), type(experience_1)))
    end=experience_0.End
    start=experience_0.Start
    institution=experience_0.Institution
    specialization=experience_0.Specialization
    if isinstance(experience_0, EducationExperience):
        degree=experience_0.Degree
    if end==None:
        end=experience_1.End
    if start==None:
        start=experience_1.Start
    if institution==None:
        institution=experience_1.Institution
    if specialization==None:
        specialization=experience_1.Specialization
    if isinstance(experience_1, EducationExperience) and degree is None:
        degree=experience_1.Degree
    description=None
    description_text=''
    if experience_0.Description != None:
        description_text+= experience_0.Description.Text
    if experience_1.Description!=None:
        description_text+=experience_1.Description.Text
    description_text=text_summary(text=description_text, summary_name=summary_name)
    if len(description_text)>0:
        description=DescriptionModel(Text=description_text)
    if isinstance(experience_1, EducationExperience):
        return EducationExperience(Institution=institution,
                                   Degree=degree,
                                        Specialization=specialization,
                                        End=end,
                                        Start=start,
                                        Description=description)
    else:
        return GeneralExperience(Institution=institution,
                                        Specialization=specialization,
                                        End=end,
                                        Start=start,
                                        Description=description)

    

def merge_general_experience_list(general_experience_list: List[GeneralExperience], summary_name: str)-> List[GeneralExperience]:
    '''The function `merge_general_experience_list` takes a list of `GeneralExperience` objects and merges
    any objects that have the same values for certain attributes, such as `End`, `Start`, `Institution`,
    and `Specialization`, by combining their `Description` attributes and returning the updated list.
    
    Parameters
    ----------
    general_experience_list : List[GeneralExperience]
        A list of GeneralExperience objects.
    summary_name : str
        The `summary_name` parameter is a string that represents the name of the summary method you want to
    generate. It is used in the `text_summary` function to generate a summary of the description text.
    
    Returns
    -------
        a list of GeneralExperience objects.
    
    '''
    if len(general_experience_list) <2:
        return general_experience_list
    j=0
    while j <len(general_experience_list):
        exper=general_experience_list[j]
        k=j+1
        while k < len(general_experience_list):
            next_exper=general_experience_list[k]
            if next_exper==exper:
                general_experience_list[j]=merge_experiences(exper, next_exper,summary_name=summary_name)
                exper=general_experience_list[j]
                general_experience_list.pop(k)
            else:
                k+=1
        j+=1
    return general_experience_list


def merge_and_update_redundant_candidate_list(candidate_list: list[Candidate],mongo_collection:Collection,summary_name: str)->list[Candidate]:
    '''The function `merge_and_update_redundant_candidate_list` takes a list of candidates, a MongoDB
    collection, and a summary name as input, merges redundant candidates in the list, updates their
    information in the MongoDB collection, and returns the updated candidate list.
    
    Parameters
    ----------
    candidate_list : list[Candidate]
        The `candidate_list` parameter is a list of `Candidate` objects. 
    mongo_collection : Collection
        The `mongo_collection` parameter is a MongoDB collection object.
    summary_name : str
        The `summary_name` parameter is a string that represents the name of the summary. It is used in the
    `merge_general_experience_list` function to merge the work and education experience lists.
    
    Returns
    -------
        a list of Candidate objects.
    
    '''
    if len(candidate_list)<2:
        return candidate_list
    candidate_list=sorted(candidate_list, key=lambda x: x.Id.generation_time, reverse=True)
    j=0
    while j <len(candidate_list):
        k=j+1
        cand=candidate_list[j]
        while k < len(candidate_list):
            next_cand=candidate_list[k]
            if cand==next_cand:
                candidate_list.pop(k)
                mongo_collection.update_one({"_id":next_cand.Id},{"$set":{"IsDuplicate":True}})
                if cand.Location == None or len(cand.Location)==0:
                    cand.Location=next_cand.Location
                if cand.Picture==None:
                    cand.Picture=next_cand.Picture
                if cand.ExternalSummaryStr==None or len(cand.ExternalSummaryStr)==0:
                    cand.ExternalSummaryStr=next_cand.ExternalSummaryStr
                cand.Skills=list(set(cand.Skills+next_cand.Skills))
                cand.Tags=list(set(cand.Tags+next_cand.Tags))
                cand.Sources=list(set(cand.Sources+next_cand.Sources))
                cand.ContactInfoList=list(set(cand.ContactInfoList+next_cand.ContactInfoList))
                cand.WorkExperienceList=merge_general_experience_list(cand.WorkExperienceList+next_cand.WorkExperienceList, summary_name=summary_name)
                cand.EducationExperienceList=merge_general_experience_list(cand.EducationExperienceList+next_cand.EducationExperienceList, summary_name=summary_name)
                cand.generate_summary()
                mongo_collection.update_one({"_id":cand.Id},{ "$set":{
                        "Location":cand.Location,
                        "Picture":cand.Picture,
                        "ExternalSummaryStr":cand.ExternalSummaryStr,
                        "Skills":cand.Skills,
                        "ContactInfoList": [ jsonable_encoder(contact_info) for contact_info in  cand.ContactInfoList],
                        "WorkExperienceList":[ jsonable_encoder(work_experience) for work_experience in cand.WorkExperienceList],
                        "EducationExperienceLis": [ jsonable_encoder(ed_experience) for ed_experience in  cand.EducationExperienceList],
                        "Embedding":cand.Embedding,
                        "Summary":jsonable_encoder(cand.Summary)
                    }
                })
            else:
                k+=1
        j+=1
    return candidate_list
    

                
                

    return candidate_list

def merge_redundant_candidates(candidate_list: List[Candidate], summary_name: str) -> List[Candidate]:
    '''The function `merge_redundant_candidates` takes a list of candidates and merges any redundant
    candidates based on their attributes, such as name, location, skills, tags, sources, and
    work/education experience.
    
    Parameters
    ----------
    candidate_list : List[Candidate]
        The `candidate_list` parameter is a list of `Candidate` objects. Each `Candidate` object represents
    a potential candidate for a job position and contains information such as name, location, summary,
    skills, work experience, education experience, and sources.
    summary_name : str
        The `summary_name` parameter is a string that represents the name of the summary method you want to
    generate. It is used in the `text_summary` function to generate a summary of the description text.
    
    Returns
    -------
        a list of candidates after merging redundant candidates.
    
    '''
    if len(candidate_list)<2:
        return candidate_list
    j=0
    while j < len(candidate_list):
        cand=candidate_list[j]
        k=j+1
        while k < len(candidate_list):
            next_cand=candidate_list[k]
            if next_cand==cand:
                Name=cand.Name
                Location=cand.Location
                if Location==None and next_cand.Location!=None:
                    Location=next_cand.Location
                Skills=list(set(cand.Skills+next_cand.Skills))
                Tags=list(set(cand.Tags+next_cand.Tags))
                Sources=list(set(cand.Sources+next_cand.Sources))
                ContactInfoList=list(set(cand.ContactInfoList+next_cand.ContactInfoList))
                WorkExperienceList=merge_general_experience_list(cand.WorkExperienceList+next_cand.WorkExperienceList, summary_name=summary_name)
                EducationExperienceList=merge_general_experience_list(cand.EducationExperienceList+next_cand.EducationExperienceList, summary_name=summary_name)
                vars(candidate_list[j]).update({
                    'Name': Name,
                    'Location': Location,
                    'Skills': Skills,
                    'Tags': Tags,
                    'WorkExperienceList': WorkExperienceList,
                    'EducationExperienceList': EducationExperienceList,
                    'ContactInfoList': ContactInfoList,
                    'Sources': Sources
                })
                cand=candidate_list[j]
                candidate_list.pop(k)
            else:
                k+=1
        j+=1
    return candidate_list

def delete_duplicate_candidates(collection):
    collection.delete_many({"IsDuplicate":True})