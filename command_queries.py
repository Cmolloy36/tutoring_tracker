import sqlalchemy as sa
from sqlalchemy.orm import Session
import os
import json
import datetime

import helper_queries
from src.db_schema import Student, Test, TutoringSession, SAT, PSAT, ACT 

def get_students(session: Session, args):
    if args.name == None:
        students = session.execute(sa.select(Student).limit(args.limit)).all() # support "order by" functionality from CLI?
    else:
        student_names = args.name
        students = session.execute(sa.select(Student).where(Student.name.in_(student_names))).all()

    for s in students: # change to return data, print formatted returned data
        print(s)
    return students

def get_elements(session: Session, args):
    model_class = {"ACT": ACT, "SAT": SAT, "PSAT": PSAT, "sessions": TutoringSession, 'tests': Test}.get(args.target)

    if args.name == None:
        elements = session.execute(sa.select(model_class).limit(args.limit)).all()
    else:
        student_ids = helper_queries.get_student_ids(session, args)
        elements = session.execute(sa.select(model_class).where(model_class.fk_students.in_(student_ids))).all()

    if len(elements) == 0:
        print("no elements found")

    for e in elements: # change to return data, print formatted returned data
        print(e)
    return elements

def post_users(session: Session, script_path, args): # can i choose which DB to use without hardcoding? how?
    for element in args.name:
        print("Adding student...")
        name_split = element.lower().split(' ')
        name = '_'.join(name_split)

        fpth = os.path.join(script_path,"./data",f"{args.target}_data/",f"{name}.json")
        with open(fpth,'r') as file:
            user_dt = json.load(file)

            insert_stmt = ''
            if args.target == 'student':
                insert_stmt = sa.insert(Student).values(user_dt)
            # elif args.target == 'tutor':
            #     insert_stmt = sa.insert(Tutor).values(user_dt)
            session.execute(insert_stmt)

def post_elements(session: Session, script_path, args):
    student_id = helper_queries.get_student_ids(session, args)
    model_class = {"ACT": ACT, "SAT": SAT, "PSAT": PSAT, "sessions": TutoringSession}.get(args.target)

    for fnm in args.files:
        ed = 'test'
        if args.target == 'sessions':
            ed = 'session'
        fpth = os.path.join(script_path,"./data",f"{ed}_data",f"{fnm}.json")
        with open(fpth,'r') as file: 
            file_dt = json.load(file)
            y, m, d = map(int, file_dt['date_completed'].split('-'))
            file_dt['date_completed'] = datetime.date(y,m,d)
            file_dt['fk_students'] = student_id[0] # . or [] indexing?

            
            test_obj = model_class(**file_dt)
            session.add(test_obj)   

def delete_users(session: Session, args):
    student_ids = helper_queries.get_student_ids(session, args)
    # model_class = {"ACT": ACT, "SAT": SAT, "PSAT": PSAT, "sessions": TutoringSession}.get(args.target) #change to tutors and students

    stmt = sa.delete(Student).where(Student.id.in_(student_ids))
    session.execute(stmt)
    print("student deleted")

def delete_elements(session: Session, script_path, args):
    student_id = helper_queries.get_student_ids(session, args)
    model_class = {"ACT": ACT, "SAT": SAT, "PSAT": PSAT, "sessions": TutoringSession}.get(args.target)

    for fnm in args.files:
        ed = 'test'
        if args.target == 'sessions':
            ed = 'session'
        fpth = os.path.join(script_path,"./data",f"{ed}_data",f"{fnm}.json")
        with open(fpth,'r') as file: 
            file_dt = json.load(file)
            y, m, d = map(int, file_dt['date_completed'].split('-'))
            file_dt['date_completed'] = datetime.date(y,m,d)
            file_dt['fk_students'] = student_id[0] # . or [] indexing?

            
            stmt = sa.delete(Test).where(Test.test_type == model_class)
            session.execute(stmt)