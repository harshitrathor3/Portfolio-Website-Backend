from pydantic import BaseModel

class PassengerData(BaseModel):
    pclass: int
    sex: str
    age: int
    sibsp: int
    parch: int
    embarked: str