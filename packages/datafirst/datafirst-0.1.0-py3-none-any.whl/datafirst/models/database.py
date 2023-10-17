from typing import Optional, Union

from dataclasses import dataclass
from enum import Enum

from dataclass_wizard import JSONWizard

from datafirst.constants import FALL, SPRING, SUMMER, WINTER
from datafirst.utils import people_name_to_directory_name


@dataclass
class Award(JSONWizard):
    name: str
    id: Optional[int] = None
    description: Optional[str] = None


@dataclass
class SkillOrSoftware:
    name: str
    type: str
    id: Optional[int] = None


@dataclass
class Topic:
    name: str
    id: Optional[int] = None


@dataclass
class Student:
    id: int
    name: str
    url_name: Union[str, None] = None
    email: Optional[str] = None
    semesters_participated: Optional[list[str]] = None
    degree_program: Optional[str] = None
    school: Optional[str] = None

    def __post_init__(self):
        self.url_name = people_name_to_directory_name(self.name)


@dataclass
class Advisor:
    id: str
    name: str
    email: Optional[str] = None
    organization: Optional[str] = None
    semesters_participated: Optional[list[str]] = None
    title: Optional[str] = None
    primary_school: Optional[str] = None

    def __post_init__(self):
        self.url_name = people_name_to_directory_name(self.name)


@dataclass
class Project(JSONWizard):
    name: str
    semester: str
    year: int
    project_overview: str
    id: str
    skill_required: Optional[list[SkillOrSoftware]] = None
    awards: Optional[list[Award]] = None
    topics: Optional[list[Topic]] = None
    students: Optional[list[Student]] = None
    final_presentation: Optional[str] = None
    advisors: Optional[list[Advisor]] = None
    student_learning: Optional[str] = None


class Semesters(Enum):
    FALL = FALL
    WINTER = WINTER
    SPRING = SPRING
    SUMMER = SUMMER


@dataclass
class Edition:
    semester: str
    year: int
