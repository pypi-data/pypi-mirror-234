import os
import sys
sys.path.append(os.getcwd())
from description_synthesis import *
import unittest
import wandb
import os
import time
import evaluate

rouge = evaluate.load('rouge')

os.environ["WANDB_API_KEY"]="b735d9d48a34be4fddbf371c8615d3b9caeccd78"

class SummaryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        run = wandb.init(project="test_description_synthesis")

    @classmethod
    def tearDownClass(cls):
        wandb.finish()

    def setUp(self):
        self.text_list=[]
        with open('test/candidates.txt') as file:
            for line in file:
                self.text_list.append(line.strip())

    def test_extractive_summary_table(self):
        columns=["src","method","result","rouge1"]
        data=[]
        for text in self.text_list:
            for method in EXTRACTIVE_NAMES:
                result=extractive_summary(text, method, 2)
                rouge_1_score=str(rouge.compute(predictions=[result], references=[text])['rouge1'])
                data.append([text, method, result, rouge_1_score])
        table =  wandb.Table(data=data, columns=columns)
        wandb.log({"extractive examples": table})

    def test_abstractive_summary_table(self):
        columns=["src","method","result","time", "rouge1"]
        data=[]
        for text in self.text_list:
            for method in ABSTRACTIVE_NAMES:
                start = time.time()
                result=abstractive_summary(text, method)
                end=time.time()
                rouge_1_score=str(rouge.compute(predictions=[result], references=[text])['rouge1'])
                data.append([text,method, result,str(end-start), rouge_1_score])
        table=wandb.Table(data=data, columns=columns)
        wandb.log({"abstractive examples": table})

    def test_sentence_embedding_summary_table(self):
        columns=["src","method","result","time", "rouge1"]
        data=[]
        for text in self.text_list:
            for method in SENTENCE_EMBEDDING_MODELS:
                start=time.time()
                result=sentence_embedding_summary(text, method)
                end=time.time()
                rouge_1_score=str(rouge.compute(predictions=[result], references=[text])['rouge1'])
                data.append([text,method, result,str(end-start), rouge_1_score])
        table=wandb.Table(data=data, columns=columns)
        wandb.log({"sentence embedding examples": table})

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