import sqlalchemy as sa
from sqlalchemy.orm import Session
import os
import json
import datetime

import helper_queries
from src.db_schema import Student, Test, TutoringSession, SAT, PSAT, ACT 

def post_users(session: Session, script_path, args):
    # model_class = {'Student': Student, "Tutor": Tutor}.get(args.target) # replace once tutor db is added
    model_class = {'Student': Student}.get(args.target)
    
    ed = 'student'
    if args.target == 'tutor':
        ed = 'tutor'

    element_list = []

    for name in args.name:
        print(f"Adding {ed}...")
        name_split = name.lower().split(' ')
        name = '_'.join(name_split)
        fpth = os.path.join(script_path,"./data",f"{ed}_data",f"{name}.json")
        with open(fpth,'r') as file: 
            file_dt = json.load(file)

            test_obj = model_class(**file_dt)
            element_list.append(test_obj)
            # session.add(test_obj)
    
    session.add_all(element_list)
    return element_list

def post_elements(session: Session, script_path, args):
    student_id = helper_queries.get_student_ids(session, args)
    model_class = {"ACT": ACT, "SAT": SAT, "PSAT": PSAT, "sessions": TutoringSession}.get(args.target)
    
    ed = 'test'
    if args.target == 'sessions':
        ed = 'session'

    element_list = []

    for fnm in args.files:
        fpth = os.path.join(script_path,"./data",f"{ed}_data",f"{fnm}.json")
        with open(fpth,'r') as file: 
            file_dt = json.load(file)
            y, m, d = map(int, file_dt['date_completed'].split('-'))
            file_dt['date_completed'] = datetime.date(y,m,d)
            file_dt['fk_students'] = student_id[0]

            test_obj = model_class(**file_dt)
            element_list.append(test_obj)
            # session.add(test_obj)
    
    session.add_all(element_list)

    return element_list

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
    model_class = {"ACT": ACT, "SAT": SAT, "PSAT": PSAT, "sessions": TutoringSession, 'tests': Test}.get(args.target) # consider moving to main function

    if args.name == None:
        elements = session.execute(sa.select(model_class).limit(args.limit)).all()
    else:
        student_ids = helper_queries.get_student_ids(session, args)
        # line below has order_by param. consider if this is worth including
        # .order_by(model_class.fk_students.desc())
        elements = session.execute(sa.select(model_class).where(model_class.fk_students.in_(student_ids))).all()

    if len(elements) == 0:
        print("no elements found")

    for e in elements: # change to return data, print formatted returned data
        print(e)
    return elements

def delete_users(session: Session, args):
    student_ids = helper_queries.get_student_ids(session, args)
    # model_class = {"ACT": ACT, "SAT": SAT, "PSAT": PSAT, "sessions": TutoringSession}.get(args.target) #change to tutors and students

    stmt = sa.delete(Student).where(Student.id.in_(student_ids))
    session.execute(stmt)
    print("user deleted")

def delete_elements(session: Session, script_path, args):
    student_id = helper_queries.get_student_ids(session, args)[0]
    model_class = {"ACT": ACT, "SAT": SAT, "PSAT": PSAT, "sessions": TutoringSession}.get(args.target)

    stmt = sa.delete(model_class).where(model_class.fk_students == student_id, model_class.id.in_(args.files))
    session.execute(stmt)
    print("element deleted")