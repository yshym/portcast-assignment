from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Container(SQLModel, table=True):
    number: Optional[str] = Field(default=None, primary_key=True)
    pol: Optional[str]
    pod: Optional[str]
    eta: Optional[str]

    bol_number: Optional[str] = Field(default=None, foreign_key="bol.number")
    bol: Optional["BOL"] = Relationship(back_populates="containers")


class BOL(SQLModel, table=True):
    number: Optional[str] = Field(default=None, primary_key=True)
    pol: Optional[str]
    pod: Optional[str]
    eta: Optional[str]

    containers: List[Container] = Relationship(back_populates="bol")
