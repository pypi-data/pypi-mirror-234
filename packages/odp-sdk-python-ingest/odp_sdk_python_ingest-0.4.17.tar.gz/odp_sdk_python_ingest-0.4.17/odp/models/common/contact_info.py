from pydantic import BaseModel


class Contact(BaseModel):
    contact: str
    organisation: str
