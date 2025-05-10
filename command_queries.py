import sqlalchemy as sa
from sqlalchemy.orm import Session
import os
import json

import helper_queries
from src.db_schema import Student, Test, TutoringSession

def get_students(session: Session, args):
    if args.names == None:
        students = session.execute(sa.select(Student).limit(args.limit)) # support "order by" functionality from CLI?
    else:
        student_names = args.names
        students = session.execute(sa.select(Student).where(Student.name.in_(student_names)))

    for s in students:
        print(s)
    return students

def get_tutoring_sessions(session: Session, args):
    if args.names == None:
        sessions = session.execute(sa.select(TutoringSession).limit(args.limit))
    else:
        student_names = args.names
        student_fks = session.execute(sa.select(Student.id).where(Student.name.in_(student_names)))
        sessions = session.execute(sa.select(TutoringSession).where(TutoringSession.student_fk.in_(student_fks)))

    for s in sessions:
        print(s)
    return sessions

def post_students(session: Session, script_path, args):
    for element in args.names:
        print("Adding student...")
        name_split = element.lower().split(' ')
        name = '_'.join(name_split)

        fpth = os.path.join(script_path,"./data",f"{args.target}_data/",f"{name}.json")
        with open(fpth,'r') as file:
            student_dt = json.load(file)

            insert_stmt = sa.insert(Student).values(student_dt)
            session.execute(insert_stmt)


def post_tutoring_sessions(session: Session, script_path, args):
    student_id = helper_queries.get_student_ids(session, args)

    for element in args.names:
        print("Adding session...")
        name_split = element.lower().split(' ')
        name = '_'.join(name_split)

        fpth = os.path.join(script_path,"./data",f"{args.target}_data/",f"{name}.json")
        with open(fpth,'r') as file:
            student_dt = json.load(file)

            insert_stmt = sa.insert(Student).values(student_dt)
            session.execute(insert_stmt)