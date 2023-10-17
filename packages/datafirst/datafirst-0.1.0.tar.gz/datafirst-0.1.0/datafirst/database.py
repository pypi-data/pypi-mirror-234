import sqlite3
from pathlib import Path

from datafirst.models.database import (
    Advisor,
    Award,
    Project,
    SkillOrSoftware,
    Student,
    Topic,
)


class Database:
    def __init__(self, database_file: Path):
        self.database_file = database_file
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_projects(self) -> list[Project]:
        projects: list[Project] = []
        self.cursor.execute("SELECT * FROM project")
        for row in self.cursor.fetchall():
            project = Project(
                id=row[0],
                name=row[1],
                semester=row[2],
                year=row[3],
                project_overview=row[4],
                final_presentation=row[5],
                student_learning=row[6],
            )
            students = self.get_students_by_project_id(project.id)
            advisors = self.get_advisors_by_project_id(project.id)
            topics = self.get_topics_by_project_id(project.id)
            awards = self.get_awards_by_project_id(project.id)
            skills = self.get_skills_by_project_id(project.id)
            project.topics = topics
            project.skill_required = skills
            project.awards = awards
            project.advisors = advisors
            project.students = students
            projects.append(project)
        return projects

    def get_skills_by_project_id(self, project_id: str) -> list[SkillOrSoftware]:
        skills: list[SkillOrSoftware] = []
        self.cursor.execute(
            "SELECT name, type FROM skill_or_software WHERE project_id = ?",
            (project_id,),
        )
        for row in self.cursor.fetchall():
            skill = SkillOrSoftware(name=row[0], type=row[1])
            skills.append(skill)
        return skills

    def get_topics_by_project_id(self, project_id: str) -> list[Topic]:
        topics: list[Topic] = []
        self.cursor.execute(
            "SELECT name FROM project_has_topic INNER JOIN topic ON topic.id = project_has_topic.topic_id WHERE project_id = ? ",
            (project_id,),
        )
        for row in self.cursor.fetchall():
            topic = Topic(name=row[0])
            topics.append(topic)
        return topics

    def get_awards_by_project_id(self, project_id: str) -> list[Award]:
        awards: list[Award] = []
        self.cursor.execute(
            "SELECT project_id, award FROM project_has_award WHERE project_id = ?",
            (project_id,),
        )
        for row in self.cursor.fetchall():
            award = Award(name=row[1])
            awards.append(award)
        return awards

    def get_students_by_project_id(self, project_id: str) -> list[Student]:
        students: list[Student] = []
        self.cursor.execute(
            "SELECT * FROM student WHERE student.id IN (SELECT student_id FROM project_has_student WHERE project_id = ?)",
            (project_id,),
        )
        for row in self.cursor.fetchall():
            semesters_participated = self.get_semesters_by_student_id(row[0])
            student = Student(
                id=row[0],
                name=row[1],
                email=row[2],
                degree_program=row[3],
                school=row[4],
                semesters_participated=semesters_participated,
            )
            students.append(student)
        return students

    def get_semesters_by_student_id(self, student_id: int):
        if student_id:
            semester_participated: list[str] = []
            for project in self.get_projects_by_student_id(student_id):
                semester = f"{project.semester} {project.year}"
                if semester not in semester_participated:
                    semester_participated.append(semester)

            return semester_participated

    def get_semester_advisor_by_id(self, advisor_id: str):
        if advisor_id:
            semester_participated: list[str] = []
            for project in self.get_projects_by_advisor_id(advisor_id):
                semester = f"{project.semester} {project.year}"
                if semester not in semester_participated:
                    semester_participated.append(semester)

            return semester_participated

    def get_advisors_by_project_id(self, project_id: str) -> list[Advisor]:
        advisors: list[Advisor] = []
        self.cursor.execute(
            "SELECT * FROM advisor WHERE advisor.id IN (SELECT advisor_id FROM project_has_advisor WHERE project_id = ?)",
            (project_id,),
        )
        for row in self.cursor.fetchall():
            advisor = Advisor(
                id=row[0],
                name=row[1],
                email=row[2],
                organization=row[3],
                primary_school=row[4],
            )
            advisor.semesters_participated = self.get_semester_advisor_by_id(advisor.id)
            advisors.append(advisor)
        return advisors

    def get_advisors(self) -> list[Advisor]:
        advisors: list[Advisor] = []
        self.cursor.execute("SELECT * FROM advisor")
        for row in self.cursor.fetchall():
            advisor = Advisor(
                id=row[0],
                name=row[1],
                email=row[2],
                organization=row[3],
                primary_school=row[4],
            )
            advisor.semesters_participated = self.get_semester_advisor_by_id(advisor.id)
            advisors.append(advisor)

        return advisors

    def get_students(self) -> list[Student]:
        students: list[Student] = []
        self.cursor.execute("SELECT * FROM student")
        for row in self.cursor.fetchall():
            semesters_participated = self.get_semesters_by_student_id(row[0])
            student = Student(
                id=row[0],
                name=row[1],
                email=row[2],
                degree_program=row[3],
                school=row[4],
                semesters_participated=semesters_participated,
            )
            students.append(student)
        return students

    def get_projects_by_student_id(self, student_id: int) -> list[Project]:
        projects: list[Project] = []
        self.cursor.execute(
            "SELECT * FROM project WHERE project.id IN (SELECT project_id FROM project_has_student WHERE student_id = ?)",
            (student_id,),
        )

        for row in self.cursor.fetchall():
            project = Project(
                id=row[0],
                name=row[1],
                semester=row[2],
                year=row[3],
                project_overview=row[4],
                final_presentation=row[5],
                student_learning=row[6],
            )
            projects.append(project)
        return projects

    def get_projects_by_advisor_id(self, advisor_id: str) -> list[Project]:
        projects: list[Project] = []
        self.cursor.execute(
            "SELECT * FROM project WHERE project.id IN (SELECT project_id FROM project_has_advisor WHERE advisor_id = ?)",
            (advisor_id,),
        )

        for row in self.cursor.fetchall():
            project = Project(
                id=row[0],
                name=row[1],
                semester=row[2],
                year=row[3],
                project_overview=row[4],
                final_presentation=row[5],
                student_learning=row[6],
            )
            projects.append(project)
        return projects
