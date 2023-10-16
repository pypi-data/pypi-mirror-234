import sys
import os
sys.path.append(os.getcwd())
from searchdatamodels.search_classes import *
import unittest
from datetime import datetime

class DescriptionEntityTest(unittest.TestCase):
    def test_eq_with_self(self):
        desc=DescriptionModel(Text="abc")
        self.assertTrue(desc==desc)

    def test_not_eq_wrong_type(self):
        desc=DescriptionModel(Text="abc")
        timefrm=TimeframeModel(Start=datetime(2015, 8, 5), End=datetime(2019, 8, 5))
        self.assertFalse(desc==timefrm)

    def test_eq_same_text(self):
        desc=DescriptionModel(Text="abc")
        desc_1=DescriptionModel(Text="abc")
        self.assertTrue(desc==desc_1)

    def test_eq_embedding(self):
        desc=DescriptionModel(Embedding=[1,1,1])
        desc_1=DescriptionModel(Embedding=[1,1,0.9])
        self.assertTrue(desc==desc_1)

    def test_not_eq_embedding(self):
        desc=DescriptionModel(Embedding=[1,1,1])
        desc_1=DescriptionModel(Embedding=[-1,-1,-1])
        self.assertFalse(desc==desc_1)

    def test_eq_languages(self):
        desc_en=DescriptionModel(Text="hello")
        desc_fr=DescriptionModel(Text="bonjour")
        self.assertEqual(desc_en, desc_fr)

class TimeframeModelTest(unittest.TestCase):
    def test_could_overlap(self):
        start_date_0 = datetime(2023, 8, 5)
        end_date_0 = datetime(2023, 8, 15)
        start_date_1 = datetime(2023, 8, 1)
        end_date_1 = datetime(2023, 8, 10)
        tfm_0 = TimeframeModel(Start=start_date_0, End=end_date_0)
        tfm_1= TimeframeModel(Start= start_date_1, End= end_date_1)
        self.assertTrue(tfm_0.could_overlap(tfm_1))

    def test_could_not_overlap(self):
        start_date_0 = datetime(2023, 8, 5)
        end_date_0 = datetime(2023, 8, 15)
        start_date_1 = datetime(2023, 9, 1)
        end_date_1 = datetime(2023, 9, 10)
        tfm_0 = TimeframeModel(Start=start_date_0, End=end_date_0)
        tfm_1= TimeframeModel(Start= start_date_1, End= end_date_1)
        self.assertFalse(tfm_0.could_overlap(tfm_1))

    def test_could_overlap_missing_start(self):
        end_date_0 = datetime(2023, 8, 15)
        start_date_1 = datetime(2023, 8, 1)
        end_date_1 = datetime(2023, 8, 10)
        tfm_0 = TimeframeModel(End=end_date_0)
        tfm_1= TimeframeModel(Start= start_date_1, End= end_date_1)
        self.assertTrue(tfm_0.could_overlap(tfm_1))

    def test_could_overlap_missing_end(self):
        start_date_0 = datetime(2023, 8, 5)
        start_date_1 = datetime(2023, 8, 1)
        end_date_1 = datetime(2023, 8, 10)
        tfm_0 = TimeframeModel(Start=start_date_0)
        tfm_1= TimeframeModel(Start= start_date_1, End= end_date_1)
        self.assertTrue(tfm_0.could_overlap(tfm_1))

    def test_could_not_overlap_missing_start(self):
        end_date_0 = datetime(2023, 8, 15)
        start_date_1 = datetime(2023, 9, 1)
        end_date_1 = datetime(2023, 9, 10)
        tfm_0 = TimeframeModel(End=end_date_0)
        tfm_1= TimeframeModel(Start= start_date_1, End= end_date_1)
        self.assertFalse(tfm_0.could_overlap(tfm_1))

    def test_could_not_overlap_missing_end(self):
        start_date_0 = datetime(2023, 10, 5)
        start_date_1 = datetime(2023, 9, 1)
        end_date_1 = datetime(2023, 9, 10)
        tfm_0 = TimeframeModel(Start=start_date_0)
        tfm_1= TimeframeModel(Start= start_date_1, End= end_date_1)
        self.assertFalse(tfm_0.could_overlap(tfm_1))

class GeneralExperienceTest(unittest.TestCase):
    def test_init(self):
        general_experience=GeneralExperience(Institution="google", Specialization="accountant")
        self.assertIsNotNone(general_experience.SpecializationDescription)
        self.assertIsNotNone(general_experience.InstitutionDescription)
        self.assertIsNotNone(general_experience.Tagline)

    def test_str(self):
        instit='harvard'
        special='gender studies'
        exp=GeneralExperience(Institution=instit, Specialization=special)
        self.assertTrue(str(exp)=='{} at {}'.format(special, instit))

    def test_eq(self):
        instit='harvard'
        special='gender studies'
        self.assertTrue(GeneralExperience(Institution=instit, Specialization=special)==GeneralExperience(Institution=instit, Specialization=special))

    def test_not_eq(self):
        instit='harvard'
        special='gender studies'
        diff_special="chemistry"
        self.assertFalse(GeneralExperience(Institution=instit, Specialization=diff_special)==GeneralExperience(Institution=instit, Specialization=special))

class EducationExperienceTest(unittest.TestCase):
    def test_eq(self):
        instit='harvard'
        special='gender studies'
        degree_0='masters'
        degree_1='bachelors'
        education_0=EducationExperience(Institution=instit, Degree=degree_0, Specialization=special)
        education_1=EducationExperience(Institution=instit, Degree=degree_1, Specialization=special)
        self.assertFalse(education_0==education_1)

class WorkExperienceTest(unittest.TestCase):

    def setUp(self):
        self.institution='goldman sachs'
        self.specialization='banker'
        self.start_date=datetime(2020,1,1)
        self.end_date=datetime(2022,1,1)

    def test_str_only_start(self):
        work_experience=WorkExperience(Institution=self.institution, Specialization=self.specialization, Start=self.start_date)
        self.assertFalse(str(work_experience).count('ending')>0)
        self.assertTrue(str(work_experience).count('starting')>0)
        self.assertTrue(str(work_experience).count('January')>0)

    def test_str_only_end(self):
        work_experience=WorkExperience(Institution= self.institution, Specialization=self.specialization, End=self.end_date)
        self.assertTrue(str(work_experience).count('ending')>0)
        self.assertFalse(str(work_experience).count('starting')>0)
        self.assertTrue(str(work_experience).count('January')>0)

    def test_str(self):
        work_experience=WorkExperience(Institution= self.institution, Specialization=self.specialization, End=self.end_date, Start=self.start_date)
        print(str(work_experience))
        self.assertTrue(str(work_experience).count('ending')>0)
        self.assertTrue(str(work_experience).count('starting')>0)
        self.assertTrue(str(work_experience).count('January')>0)
        self.assertTrue(str(work_experience).count('2 years')>0)


        



class CandidateTest(unittest.TestCase):
    def test_init(self):
        skill_list=["dance", "ballet"]
        workplace="American Ballet Theatre"
        school="julliard"
        work_experience_list=[WorkExperience(Institution=workplace, Specialization="Dancer")]
        education_experience_list=[EducationExperience(Institution=school, Specialization="classical ballet")]
        name="Misty Copeland"
        uuid="abcxyz"
        cand=Candidate(
                       Name=name, 
                       WorkExperienceList=work_experience_list,
                       EducationExperienceList=education_experience_list,
                       Skills=skill_list)
        self.assertIsNotNone(cand.Summary)
        summary_text=cand.Summary.Text
        self.assertNotEqual(len(summary_text),0)
        self.assertNotEqual(summary_text.find(workplace.lower()), -1)
        self.assertNotEqual(summary_text.find(school), -1)
        
    def test_eq_from_sources(self):
        source_list=["linkedin.com/jacobsmith", "github.com/jakegithubuser"]
        cand_0=Candidate(Name="jake smith",Sources=source_list)
        cand_1=Candidate(Name="jacob smith", Sources=source_list)
        self.assertTrue(cand_0==cand_1)

    def test_init_from_external_summary_str(self):
        external_summary_str="this person is a great hard worker"
        cand=Candidate(Name="person", ExternalSummaryStr=external_summary_str)
        embedding=create_embedding(external_summary_str)
        self.assertEqual(cand.Embedding, embedding)


if __name__ =='__main__':
    #WorkExperienceTest().test_str_only_start()
    unittest.main()