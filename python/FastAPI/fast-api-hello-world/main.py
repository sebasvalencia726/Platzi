#!/usr/bin/env python3

# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
# from pydantic import HttpUrl

# FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path

app = FastAPI()


# Models

class HeirColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="In"
        )
    state: str = Field(
        min_length=1,
        max_length=50,
        example="MiddeOf"
        )
    country: str = Field(
        min_length=1,
        max_length=50,
        example="Nowhere"
        )


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Piter"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Toro"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
        )
    hair_color: Optional[HeirColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr = Field(..., example="pitertoro@example.com")
    # website_url: Optional[HttpUrl] = Field(default=None)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Sebastián",
    #             "last_name": "Valencia",
    #             "age": 35,
    #             "hair_color": "black",
    #             "is_married": False,
    #             "email": "sebasvalencia726@gmail.com"
    #         }
    #     }


@app.get("/")
def home():
    return {"Hello": "World"}


# Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


# Validations: Query parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name."
        "It's between 1 and 50 characters."
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required."
    )
):
    return {name: age}


# Validations: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person Id",
        description="This is the person identification. It's required."
    )
):
    return {person_id: "It exists!"}


# Validations: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person Id",
        description="This is the person id.",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
    # return person
