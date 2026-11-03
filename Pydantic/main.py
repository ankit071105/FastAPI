
from pydantic import BaseModel, EmailStr , AnyUrl, Field, field_validator,model_validator , computed_field
from typing import List, Dict , Optional,Annotated

class Patient(BaseModel):
    
    # all field is required by default
    name: str = Annotated[str, Field(min_length=3, title='Name of the patient',description='Fill the Name under 50 characters',examples=['ankit','aman','himanshu'], max_length=50)] # name should be minimum 3 and maximum 50 characters
    
    @field_validator('name',mode='before')
    @classmethod
    def validate_name(cls, value):
        return value.upper()  # Convert name to uppercase
    
    # email: EmailStr # @ symbol should be there in email address
    email: EmailStr
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        v=['hdfc.com','sbi.com','icici.com']
        d=value.split('@')[-1]
        if d not in v:
            raise ValueError('Email must not be from the domain hdfc.com, sbi.com, icici.com')
        return value
    
    linkedin_url: AnyUrl #http url should be only valid
    
    age: int 
    # @field_validator('age',mode='before')
    # @classmethod
    # def validate_age(cls, value):
    #     if 0 <value<100:
    #         return value
    #     else:
    #         raise ValueError('Age must be between 0 and 100')
    
    @model_validator(mode='after')
    @classmethod
    def validate_emergency_contact(cls, values):
        if values.age >60 and 'emergency' not in values.contact:
            raise ValueError('Emergency contact is required for patients above 60 years old')
        return values
    
    weight:Annotated[float,Field(gt=0, lt=150 ,strict=True)] # weight should be greater than 0 and less than 150
    height:Annotated[float,Field(gt=0, lt=250 ,strict=True)]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height **2), 2)
    
    
    marry:Annotated[bool, Field(default=False, description='Marry status of the patient', examples=[True, False])] # marry status should be true or false
    
    allergies:Optional[List[str]] = Field(default=None, max_length=5) # two level validation with optional which is not required 
    
    

    contact:Dict[str, str] # two level validation 

def insert_patient(patient: Patient):
     print(patient) # print all the details of the patient

def update_patient(patient: Patient):
     print("Name of the patient ", patient.name, " Age is ", patient.age, " Weight is ", patient.weight, " Marry status is ", patient.marry, " Allergies are ", patient.allergies, " Contact details are ", patient.contact, " BMI is ", patient.bmi) #calling all details of the patient

p = {'name': "Ankit", 'email': 'ankit@sbi.com', 'linkedin_url': 'https://www.linkedin.com/in/ankit071105', 'age': 80, 'weight': 50, 'height': 1.72, 'marry': 'true',  'contact': {'phone':'+92992002002', 'emergency':'+9032881991'}} # smart enough to convert string to int

p1 = Patient(**p)
insert_patient(p1)

# update_patient(p1)