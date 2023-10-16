import os
import sys
sys.path.append(os.getcwd())
from description_synthesis import *
import unittest
import os
import time
import evaluate

rouge = evaluate.load('rouge')

class SummaryTest(unittest.TestCase):

    def setUp(self):
        self.text_list=[]
        with open('test/candidates.txt') as file:
            for line in file:
                self.text_list.append(line.strip())

    def test_sentence_embedding_summary_education(self):
        edu_1=EducationExperience(Degree="phd", Specialization="mathematics", Institution="harvard university")
        edu_0=EducationExperience(Degree="phd", Specialization="math", Institution="harvard university")
        edu_str_0=NAME_TOKEN+ str(edu_0)
        edu_str_1=NAME_TOKEN+ str(edu_1)
        education_summary=sentence_embedding_summary(edu_str_0+'. '+edu_str_1, MINI_LM_12)
        print(education_summary)
        self.assertEqual(1, education_summary.count('harvard'))

    def test_sentence_embedding_summary_education_different(self):
        edu_1=EducationExperience(Degree="bachelors", Specialization="math", Institution="harvard university")
        edu_0=EducationExperience(Degree="phd", Specialization="math", Institution="princeton university")
        edu_str_0=NAME_TOKEN+ str(edu_0)
        edu_str_1=NAME_TOKEN+ str(edu_1)
        education_summary=sentence_embedding_summary(edu_str_0+'. '+edu_str_1, MINI_LM_12)
        print(education_summary)
        self.assertEqual(2, education_summary.count('math'))



class MergeTest(unittest.TestCase):
    def test_merge_descriptions(self):
        with open('test/horse_wikipedia.txt') as file:
            text=file.read()
        description_list=[DescriptionModel(Text=text) for _ in range(3)]
        result_description_list=merge_descriptions(description_list)
        self.assertTrue(len(result_description_list)==1)

    def test_merge_descriptions_not(self):
        with open('test/horse_wikipedia.txt') as file:
            horse_text=file.read()
        with open('test/cat_wikipedia.txt') as file:
            cat_text=file.read()
        description_list=[DescriptionModel(Text=cat_text), DescriptionModel(Text=horse_text)]
        result_description_list=merge_descriptions(description_list)
        self.assertTrue(len(result_description_list)==2)


if __name__=='__main__':
    #SummaryTest().test_sentence_embedding_summary_education_different()
    unittest.main()