
import sqlalchemy as sa
from sqlalchemy.orm import Session, mapped_column, Mapped
import datetime
import pathlib
import json
import os
from enum import Enum

import sys

class Base(sa.orm.DeclarativeBase):
    pass

class Student(Base):
        __tablename__ = 'students_table'

        # This creates an __init__ method with each param as an optional input
        id: Mapped[int] = mapped_column(sa.Sequence('id_seq'), primary_key=True)
        created_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
        updated_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
        name: Mapped[str] = mapped_column()
        email: Mapped[str] = mapped_column(unique=True)
        parent: Mapped[str] = mapped_column()
        taking_SAT: Mapped[bool]
        taking_ACT: Mapped[bool]
        target_SAT: Mapped[int] = mapped_column(nullable=True,default=None)
        target_ACT: Mapped[int] = mapped_column(nullable=True,default=None)
        active_student: Mapped[bool] = mapped_column(default=True)
        num_sessions: Mapped[int] = mapped_column(default=0)

        # def __init__(self,created_at,updated_at,name,parent,taking_SAT,taking_ACT,target_SAT,target_ACT,active_student,num_sessions):
        #     self.created_at = created_at
        #     self.updated_at = updated_at
        #     self.name = name
        #     self.parent = parent
        #     self.taking_SAT = taking_SAT
        #     self.taking_ACT = taking_ACT
        #     self.target_SAT = target_SAT
        #     self.target_ACT = target_ACT
        #     self.active_student = active_student
        #     self.num_sessions = self.num_sessions

        def __repr__(self) -> str:
            return (
        f"Student(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at}, "
        f"name={self.name!r}, email={self.email!r}, parent={self.parent!r}, "
        f"taking_SAT={self.taking_SAT}, taking_ACT={self.taking_ACT}, "
        f"target_SAT={self.target_SAT}, target_ACT={self.target_ACT}, "
        f"active_student={self.active_student}, num_sessions={self.num_sessions})"
    )
        

# Consider using click or argparse to specify out commands


def main():
    args = sys.argv

    script_path = os.path.dirname(os.path.realpath('__file__'))

    engine = sa.create_engine("sqlite:///tutoring_tracker.db", echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        if len(args) < 1:
            print("Please enter a command.")

        if args[1] == "reset":
            ans = input("Are you sure you want to reset the database?")
            if ans.lower() == 'yes':
                statement = sa.select(Student).all()
                objects = session.execute(statement).all()
                for obj in objects:
                    session.delete(obj)


        elif args[1] == "add_student":
            print("Adding student...") # Need to check if user exists first
            fpth = os.path.join(script_path,"./data/student_data/",f"{args[2]}.json")
            with open(fpth,'r') as file:
                student_dt = json.load(file)

                insert_stmt = sa.insert(Student).values(student_dt)
                session.execute(insert_stmt)

        elif args[1] == "get_students":
            students = session.query(Student).all()
            for s in students:
                print(s)

        elif len(args) > 1 and args[1] == "queryconnect":
            stmt = sa.text('''SELECT * FROM students
            WHERE name = :name''')
            students = session.execute(stmt, {"name": "First Last"})
            for student in students:
                print(student)

        session.commit()

         



if __name__ == "__main__":
    main()