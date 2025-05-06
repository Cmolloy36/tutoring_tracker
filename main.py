
import sqlalchemy as sa
from sqlalchemy.orm import Session, mapped_column, Mapped
import datetime
import pathlib
import json
import os
import argparse
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
    actual_SAT: Mapped[int] = mapped_column(nullable=True,default=None)
    actual_ACT: Mapped[int] = mapped_column(nullable=True,default=None)
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
    f"Student(id={self.id!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r}, "
    f"name={self.name!r}, email={self.email!r}, parent={self.parent!r}, "
    f"taking_SAT={self.taking_SAT!r}, taking_ACT={self.taking_ACT!r}, "
    f"target_SAT={self.target_SAT!r}, target_ACT={self.target_ACT!r}, "
    f"actual_SAT={self.actual_SAT!r}, actual_ACT={self.actual_ACT!r}, "
    f"active_student={self.active_student!r}, num_sessions={self.num_sessions!r})"
    )
        
class TutoringSession(Base):
    __tablename__ = 'sessions_table'

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.Sequence('id_seq'), primary_key=True)
    fk_students: Mapped[int] = mapped_column(sa.ForeignKey(Student.id))

    def __repr__(self) -> str:
        return (
    f"Session(id={self.id!r}, student_id={self.fk_students!r}"
)
        

# Consider using click or argparse to specify out commands
    
def parser_fcn(args):
    parser = argparse.ArgumentParser(
        prog='Tutoring Tracker',
        description='Manage students and sessions using Tutoring Tracker',
        epilog='Thanks for using Tutoring Tracker!')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Positional args

    # POST
    post_parser = subparsers.add_parser('post', help='Post new data')
    post_parser.add_argument('target', choices=['students', 'sessions', 'tests'])
    post_parser.add_argument('files', nargs='+', help='JSON files to add') # restructure like this


    parser.add_argument('post_students', nargs='*', help='Add any number of student JSON files')
    parser.add_argument('--post_sessions', nargs='*', help='Add any number of session JSON files')
    parser.add_argument('--post_tests', nargs='*', help='Add any number of test JSON files')

    parser.add_argument('get_students', nargs='*', help='Get any number of student JSON files')
    parser.add_argument('--get_sessions', nargs='*', help='Get any number of session JSON files')
    parser.add_argument('--get_tests', nargs='*', help='Get any number of test JSON files')

    parser.add_argument('--update_students', nargs='+', help='Update any number of student JSON files')
    parser.add_argument('--update_sessions', nargs='+', help='Update any number of session JSON files')
    parser.add_argument('--update_tests', nargs='+', help='Update any number of test JSON files')

    parser.add_argument('--reset', help='Reset DB',action='store_true')

    # Optional args
    parser.add_argument('--limit', type=int,default=10, help='Update any number of test JSON files')
    parser.add_argument('-v','--verbose',action='store_true', help='Perform actions in verbose mode')

    return parser.parse_args()


def main(args):
    script_path = os.path.dirname(os.path.realpath('__file__'))

    engine = sa.create_engine("sqlite:///tutoring_tracker.db", echo=args.verbose) # Set echo to false for quiet output
    # metadata = sa.MetaData()
    # metadata.reflect(bind=engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        # if len(args) < 1:
        #     print("Please enter a command.")

        if args.reset:
            ans = input("Are you sure you want to reset the database? ")
            if ans.lower() == 'yes':
                statement = sa.select(Student)
                objects = session.scalars(statement).all()
                for obj in objects:
                    session.delete(obj)


        elif args.post_students:
            print(args.post_students)
            print("Adding student...") # Need to check if student exists first
            for student in args.post_students[1:]:
                fpth = os.path.join(script_path,"./data/student_data/",f"{student}.json")
                with open(fpth,'r') as file:
                    student_dt = json.load(file)

                    # need query stmt to check if user with same email is already in database. if not, add them. if so, indicate they already exist

                    insert_stmt = sa.insert(Student).values(student_dt)
                    session.execute(insert_stmt)

        elif args.get_students != None:
            print(args.get_students)
            limit = args.limit
            if args.get_students == []:
                students = session.query(Student).limit(limit)
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
    args = parser_fcn(sys.argv[1:])
    main(args)