from pydantic import BaseModel


class TestimonialFormat(BaseModel):
    name: str
    designation: str
    company: str
    feedback: str
