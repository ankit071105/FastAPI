from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: str
    email: str
    age: int
    gender: str ='Male'
    contact: dict
    address: Address  # Nested model for address
    
address_data = {
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zip_code": "12345"
}
a1=Address(**address_data)
patient_data = {
    "name": "John Doe",
    "email": "john@gmail.com",
    "age": 30,
    "contact": {
        "phone": "123-456-7890",
        "emergency": "987-654-3210"
    },
    "address": a1
    }# Pass the nested model as a dictionary
p1=Patient(**patient_data)

# model_dump_json(include=['',''] ,exclude={'address': {'state'}}) -> json , model_dump -> dict
t=p1.model_dump_json(exclude_unset=True ,exclude={'address': {'state'}}) # exclude zip_code from address
print(t) #exclude state from address
print(type(t))