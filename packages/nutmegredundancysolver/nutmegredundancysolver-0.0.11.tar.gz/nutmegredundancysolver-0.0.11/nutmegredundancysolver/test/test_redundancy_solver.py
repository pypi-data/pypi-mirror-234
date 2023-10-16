import sys
import os
sys.path.append(os.getcwd())
from redundancy_solver import *
import unittest
from datetime import datetime
import string
import random
import mongomock
from fastapi.encoders import jsonable_encoder
import time


class RedundancySolverTest(unittest.TestCase):
    def test_merge_experiences_general(self):
        institution="apple"
        specialization="farmer"
        experience_0=GeneralExperience(Institution=institution, Specialization=specialization)
        experience_1=GeneralExperience(Institution=institution, Specialization=specialization)
        result_experience=merge_experiences(experience_0, experience_1, summary_name=LSA)
        self.assertEqual(result_experience.Institution, institution)
        self.assertEqual(result_experience.Specialization, specialization)

    def test_merge_experiences_education(self):
        institution="oxford university"
        specialization="history"
        degree="phd"
        education_0=EducationExperience(Degree=degree, Institution=institution, Specialization=specialization)
        education_1=EducationExperience(Degree=degree, Institution=institution, Specialization=specialization)
        result_education=merge_experiences(education_0, education_1, summary_name=LSA)
        self.assertEqual(result_education.Institution, institution)
        self.assertEqual(result_education.Specialization, specialization)
        self.assertEqual(result_education.Degree, degree)

    def test_merge_experiences_exception(self):
        institution="oxford university"
        specialization="history"
        degree="phd"
        experience_0=GeneralExperience(Institution="microsoft", Specialization="salesperson")
        education_0=EducationExperience(Degree=degree, Institution=institution, Specialization=specialization)
        with self.assertRaises(Exception):
            merge_experiences(experience_0, education_0)


    def test_merge_general_experience_list(self):
        general_experience_list=[GeneralExperience(Institution="apple", Specialization="farmer") for _ in range(3)]
        result_general_experience_list= merge_general_experience_list(general_experience_list, summary_name=LSA)
        self.assertEqual(len(result_general_experience_list),1)
    
    def test_merge_general_experience_list_not_eq(self):
        general_experience_list=[GeneralExperience(Institution="apple", Specialization="farmer"), 
                                 GeneralExperience(Institution="netflix", Specialization="watcher")]
        result_general_experience_list= merge_general_experience_list(general_experience_list, summary_name=LSA)
        self.assertEqual(len(result_general_experience_list),2)

    def test_merge_redundant_candidates_different(self):
        candidate_list=[Candidate(Name=''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=10))) for x in range(3)]
        result_candidate_list=merge_redundant_candidates(candidate_list, LSA)
        self.assertEqual(len(result_candidate_list),3)

    def test_merge_redundant_candidates_by_sources(self):
        source_list=["linkedin.com/joebiden", "indeed.com/joebiden"]
        candidate_list=[Candidate(Name=''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=10)), Sources=source_list) for x in range(3) ]
        result_candidate_list=merge_redundant_candidates(candidate_list, LSA)
        self.assertEqual(len(result_candidate_list),1)

    def test_merge_redundant_candidates_by_summaries(self):
        name_list=['joe biden', 'joseph biden']
        candidate_list=[Candidate(Name=name_list[x]) for x in range(2)]
        result_candidate_list=merge_redundant_candidates(candidate_list, LSA)
        self.assertEqual(len(result_candidate_list),2)

        work_experience_list=[WorkExperience(Institution="United States", Specialization="President"),
                              WorkExperience(Institution="Congress", Specialization="Senator")]
        candidate_list=[
            Candidate(Name=name_list[x], WorkExperienceList=work_experience_list)
            for x in range(2)]
        result_candidate_list=merge_redundant_candidates(candidate_list, LSA)
        self.assertEqual(len(result_candidate_list),1)

    def test_delete_duplicates(self):
        '''
        GIVEN a collection with x quantity of candidates that should not be deleted and y candidates that should be deleted
        WHEN we run the delete_duplicates function
        THEN there should only be y candidates left in the DB
        '''
        collection=mongomock.MongoClient().db.collection
        x=10
        y=5
        good_candidate_list=[Candidate(Name=''.join(random.choices(string.ascii_letters, k=5)), IsDuplicate=True) for _ in range(x)]
        bad_candidate_list=[Candidate(Name=''.join(random.choices(string.ascii_letters, k=5)), IsDuplicate=False) for _ in range(y)]
        insert_list=[jsonable_encoder(cand) for cand in good_candidate_list+bad_candidate_list]
        collection.insert_many(insert_list)
        delete_duplicate_candidates(collection)
        self.assertEqual(y, collection.count_documents({}))
        return
    
    def test_merge_and_update_redundant_candidate_list(self):
        '''
        GIVEN a list of candidates that are equal, and one that is not (the special one)
        WHEN we call merge_and_update_redundant_candidate_list, 
        THEN we expect the newest one to have the values from the old ones and the older ones to have their IsDuplicate=True
        '''
        old_name="john"
        source="linkedin.com/xyz"
        collection=mongomock.MongoClient().db.collection
        collection.delete_many({})
        old_candidate_list=[
            Candidate(Name=old_name,Location="wrong place",Sources=[source]),
            Candidate(Name=old_name,Skills=["dance"], Sources=[source])
        ]
        old_insert_result=collection.insert_many([ jsonable_encoder(c) for c in old_candidate_list])
        special_name="thomas"
        special_insert_result=collection.insert_one(jsonable_encoder(Candidate(Name=special_name)))
        time.sleep(1) #just to super sure that the new candidate is newer than the old ones
        correct_place="correct"
        correct_name="correct name"
        new_candidate=Candidate(Name=correct_name,Location=correct_place,Sources=[source])
        new_insert_result=collection.insert_one(jsonable_encoder(new_candidate))
        returned_candidate_dict_list=[ c for c in collection.find({})]
        for returned_candidate in returned_candidate_dict_list:
            returned_candidate["Id"]=returned_candidate["_id"]
            del returned_candidate["_id"]
        returned_candidate_list=[Candidate(**c) for c in returned_candidate_dict_list]
        returned_candidate_list=merge_and_update_redundant_candidate_list(returned_candidate_list, collection, LSA)
        returned_id_list=[c.Id for c in returned_candidate_list]
        for id in old_insert_result.inserted_ids:
            self.assertNotIn(id, returned_id_list)
        for returned_cand in returned_candidate_list:
            if returned_cand.Id in old_insert_result.inserted_ids:
                self.assertTrue(returned_cand.IsDuplicate)
            elif returned_cand.Id == new_insert_result.inserted_id:
                self.assertGreater(len(returned_cand.Skills),0)
                self.assertEqual(returned_cand.Location, correct_place)
                self.assertEqual(correct_name, returned_cand.Name)
                self.assertFalse(returned_cand.IsDuplicate)
            elif returned_cand.Id==special_insert_result.inserted_id:
                self.assertFalse(returned_cand.IsDuplicate)
                self.assertEqual(special_name, returned_cand.Name)


if __name__ == '__main__':
    rt=RedundancySolverTest()
    rt.setUp()
    rt.test_merge_and_update_redundant_candidate_list()