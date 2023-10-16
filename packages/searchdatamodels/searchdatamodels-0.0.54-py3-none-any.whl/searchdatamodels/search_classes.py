from pydantic import validator
from typing import List, Optional
from datetime import date
import numpy as np
from scipy.spatial.distance import euclidean,cosine
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from .tagline_embedding import *
import os

DOT_PRODUCT='dot_product'
EUCLIDEAN='euclidean'
COSINE='cosine'
NAME_TOKEN='this person' #for semantic similarity matching, it's best to have names be identical

DEFAULT_DISTANCE_METRIC=COSINE
DEFAULT_DISTANCE_THRESHOLD=0.025 #if distance metric>= DISTANCE_THRESHOLD then two Descriptions are considered semantically different

normalized_levenshtein = NormalizedLevenshtein() #difference metric between strings used to see if two names are the same
NORMALIZED_LEVENSHTEIN_THRESHOLD=0.1

from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel): #solving this issue: https://github.com/pydantic/pydantic/issues/3320
    class Config:
        arbitrary_types_allowed = True

def same_string(str_0: str, str_1:str) -> bool:
    '''The function checks if two strings are the same by comparing their normalized Levenshtein distance
    and checking if one string is a substring of the other.
    
    Parameters
    ----------
    str_0 : str
    str_1 : str
    
    Returns
    -------
        a boolean value. If the two input strings are the same or similar enough based on the normalized
    Levenshtein distance, it returns True. Otherwise, it returns False.
    
    '''
    if str_0.find(str_1)!=-1 or str_1.find(str_0)!=-1:
        return True
    if normalized_levenshtein.distance(str_0, str_1) >= NORMALIZED_LEVENSHTEIN_THRESHOLD:
        return False
    return True

class DescriptionModel(BaseModel): #text description + embedding
    Text: Optional[str]= None
    Embedding: Optional[List[float]]=None #if there is a text description, we can compute the vector embedding
    DistanceMetric: str = DEFAULT_DISTANCE_METRIC
    DistanceThreshold: float = DEFAULT_DISTANCE_THRESHOLD

    @validator("DistanceMetric")
    def validate_distance_metric(cls, value):
        assert value in [DOT_PRODUCT, EUCLIDEAN, COSINE]
        return value
    
    @validator("Text")
    def translate_to_english_validator(cls, text_value):
        if text_value:
            return translate_to_english(text_value)
        return text_value

    def __eq__(self, __value: object) -> bool:
        if id(__value)==id(self): #check if its a reference to the same object
            return True
        if not isinstance(__value, type(self)): #check if the objects are the same class
            return False
        if self.Text!=None or __value.Text!=None:
            if self.Text==__value.Text: #check if the objects have identical text
                return True
        if self.Embedding!=None and __value.Embedding !=None: #compare embeddings
            if self.DistanceMetric == EUCLIDEAN:
                distance=euclidean(self.Embedding, __value.Embedding)
            elif self.DistanceMetric == COSINE:
                distance= cosine(self.Embedding, __value.Embedding)
            elif self.DistanceMetric==DOT_PRODUCT:
                distance= np.dot(self.Embedding, __value.Embedding) * cosine(self.Embedding, __value.Embedding)
            if distance<= self.DistanceThreshold:
                return True
            else:
                return False
        return False
        
class TimeframeModel(BaseModel): #this can be anything that could have a start and/or end date and description
    Start: Optional[date]=None
    End: Optional[date]=None
    Description: Optional[DescriptionModel]=None

    def could_overlap(self, _timeframe_model)-> bool:
        if self.Start != None and self.End != None and _timeframe_model.Start != None and _timeframe_model.End != None:
            return self.End > _timeframe_model.Start and _timeframe_model.End >self.Start
        elif self.End != None and _timeframe_model.Start != None:
            return self.End > _timeframe_model.Start
        elif self.Start != None and _timeframe_model.End != None:
            return _timeframe_model.End > self.Start
        return True


class GeneralExperience(TimeframeModel): #this class will serve as both jobs and education
    Institution: str=None #company/school
    InstitutionDescription: DescriptionModel=None
    Specialization: str=None #role/field of study
    SpecializationDescription: DescriptionModel=None
    Tagline: DescriptionModel=None #"job at company", "major at school"

    def __init__(self, Institution=None, Specialization=None, search=False, **kwargs):
        super().__init__(**kwargs)
        if Institution!=None:
            self.Institution=Institution.lower()
        if Specialization:
            Specialization=translate_to_english(Specialization)
            self.Specialization=Specialization
        text=self.__str__()
        if search:
            self.Tagline = DescriptionModel(Text=text)
        else:
            embedding = create_embedding(text)
            self.Tagline=DescriptionModel(Text=text, Embedding=embedding)
        if self.Institution is not None and self.InstitutionDescription is None:
            if search:
                self.InstitutionDescription = DescriptionModel(Text=self.Institution)
            else:
                self.InstitutionDescription=DescriptionModel(Text=self.Institution, Embedding=create_embedding(self.Institution))
        if self.Specialization is not None and self.SpecializationDescription is None:
            if search:
                self.SpecializationDescription = DescriptionModel(Text=self.Specialization)
            else:
                self.SpecializationDescription=DescriptionModel(Text=self.Specialization, Embedding=create_embedding(self.Specialization))

    def __str__(self):
        if self.Institution!=None and self.Specialization!=None:
            return '{} at {}'.format(self.Specialization, self.Institution)
        elif self.Institution!=None:
            return self.Institution
        elif self.Specialization != None:
            return self.Specialization
        return ''

    def __eq__(self, __value: object) -> bool:
        if not self.could_overlap(__value): #if the timeframes cant match up then these are different things
            return False
        if self.Institution !=None and self.Specialization !=None and __value.Institution != None and __value.Specialization != None:
            return self.Tagline==__value.Tagline
        elif self.Institution !=None and __value.Instutution != None:
            return self.InstitutionDescription==__value.InstitutionDescription
        elif self.Specialization !=None and __value.Specialization != None:
            return self.SpecializationDescription==__value.SpecializationDesciption
        return True

class WorkExperience(GeneralExperience):
    def __str__(self):
        if self.Institution!=None and self.Specialization!=None:
            str_representation= ' worked as {} at {}'.format(self.Specialization, self.Institution)
        elif self.Institution!=None:
            str_representation= 'worked at '+self.Institution
        elif self.Specialization != None:
            str_representation= 'worked as '+self.Specialization
        else:
            return ''
        if self.Start !=None and self.End !=None:
            str_representation+=', for {} years'.format(int(self.End.year-self.Start.year))
        if self.Start!=None:
            str_representation+=', starting in {} {}'.format(self.Start.strftime("%B"), self.Start.year)
        if self.End !=None:
            str_representation+=', ending in {} {}'.format(self.End.strftime("%B"), self.End.year)
        return str_representation+'.'
    

class ContactInfo(BaseModel):
    Type: str=None #phone, email, telegram, facebook, etc
    Value: str=None #phone number, email address, etc

    def __init__(self, Type=None, Value=None, **kwargs):
        super().__init__(**kwargs)
        self.Type=Type
        self.Value=Value

    def __hash__(self):
        """Implement the __hash__ method for the set() usage below"""
        return hash(self.Value)

    def __eq__(self, other: object):
        """
        Implement the __eq__ method to ignore the type, because for equality the value what matters.
        """
        if isinstance(other, ContactInfo):
            return self.Value == other.Value
        else:
            return False

    
class EducationExperience(GeneralExperience):
    Degree: Optional[str]=None #masters, bachelors, phD

    def __init__(self, Degree=None,**kwargs):
        super().__init__(**kwargs)
        if Degree!=None:
            self.Degree=Degree.lower()
    
    def __eq__(self, __value: object) -> bool:
        if self.Degree!=None and __value.Degree!=None:
            return same_string(self.Degree, __value.Degree)
        return super().__eq__(__value)


    def __str__(self):
        if self.Degree==None:
            _degree=''
        else:
            _degree=' '+self.Degree
        if self.Institution!=None and self.Specialization!=None:
            return ' has a{} degree in {} from {}.'.format(_degree,self.Specialization, self.Institution)
        elif self.Institution!=None:
            return ' has a{} degree from {}.'.format(_degree, self.Institution)
        elif self.Specialization != None:
            return ' has a{} degree in {}.'.format(_degree, self.Specialization)
        return ''

class Candidate(BaseModel):
    Name: str
    Location: Optional[str]=None
    Picture: Optional[str]=None
    Summary: Optional[DescriptionModel]=None
    Skills: Optional[List[str]]=[]
    WorkExperienceList: Optional[List[WorkExperience]]=[]
    EducationExperienceList: Optional[List[EducationExperience]]=[]
    ContactInfoList: Optional[List[ContactInfo]]=[]
    Tags: Optional[List[str]]=[]
    Sources: Optional[List[str]]=[]
    ExternalSummaryStr: Optional[str]=''  # this is the summary the user provides about themselves
    ProjectList: Optional[List[DescriptionModel]]=None
    RankScore: Optional[float]=0.0
    Embedding: Optional[List[float]]=[]
    Id: Optional[object]=None
    IsDuplicate: Optional[bool]=False
    score: Optional[float]=0.0

    def __init__(self, search=False, **kwargs):
        try:
            kwargs['ExternalSummaryStr'] = translate_to_english(kwargs['ExternalSummaryStr'])
        except KeyError:
            pass
        super().__init__(**kwargs)
        if self.Location:
            self.Location = self.Location.lower()
        if self.Summary is None or len(self.Summary.Text)==0:
            summary_text=''
            if len(self.WorkExperienceList)>0:
                summary_text+='. '.join([self.Name + str(work) for work in self.WorkExperienceList])+'. '
            if len(self.EducationExperienceList)>0:
                summary_text+='. '.join([self.Name + str(edu) for edu in self.EducationExperienceList])+'. '
            if self.Skills and len(self.Skills)>0:
                summary_text+=self.Name+" is skilled in "+" and ".join(self.Skills)
            if len(summary_text)>0: #len(summary_text)==0 should not happen outside of testing
                if search:
                    self.Summary = DescriptionModel(Text=summary_text)
                else:
                    summary_embedding=create_embedding(summary_text)
                    self.Summary=DescriptionModel(Text=summary_text, Embedding=summary_embedding)
                    self.Embedding=summary_embedding
            elif self.ExternalSummaryStr and len(self.ExternalSummaryStr)>0:
                if not search:
                    self.Embedding=create_embedding(self.ExternalSummaryStr)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            if set(self.Sources).intersection(set(__value.Sources)):
                # if two candidates link to one another then it's the same person
                return True
            if set(self.ContactInfoList).intersection(set(__value.ContactInfoList)):
                # if two candidates share some contact info then it's the same person
                return True
            if self.Summary is not None and __value.Summary and self.Summary == __value.Summary:
                # if two candidates have super similar summaries then it's probably the same person
                return True
            return False
        else:
            return False
    
class CandidateListModel(BaseModel): #used for sending to/from services
    CandidateList: List[Candidate]


class SearchTemplate(BaseModel):
    location: Optional[List[str]]=[]
    skill: Optional[List[str]]=[]
    seniority: Optional[List[str]]=[]
    title: Optional[List[str]]=[]
    company: Optional[List[str]]=[]
    experience: Optional[List[str]]=[]
    school: Optional[List[str]]=[]
    major: Optional[List[str]]=[]

class ChatEndpointBody(BaseModel): #used for sending to pepper
    UserQuery: str
    CandidateList: list[Candidate]
    ConversationHistory: list[list]
    SearchTemplate: SearchTemplate
    LLMName: str
    NQuery:int

class Workplace(BaseModel): #companies and organizations where people worked
    Name: str
    Size: int
    Sources: list[str]
    Embedding: list[float]
    Description: str
    #we might want some more attributes for example: https://data.crunchbase.com/docs/organizationsummary
