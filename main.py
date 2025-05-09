
import sqlalchemy as sa
from sqlalchemy.orm import Session, mapped_column, Mapped
import datetime
import pathlib
import json
import os
import argparse
import sys

import queries
from src.db_schema import Base, Student, Test, TutoringSession
    
def parser_fcn(args):
    parser = argparse.ArgumentParser(
        prog='Tutoring Tracker',
        description='Manage students and sessions using Tutoring Tracker',
        epilog='Thanks for using Tutoring Tracker!')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Positional args

    # POST
    post_parser = subparsers.add_parser('post', help='Post new data')
    post_parser.add_argument('--target', choices=['student', 'session', 'test'])
    post_parser.add_argument('--files', nargs='+', help='JSON files to add')

    get_parser = subparsers.add_parser('get', help='Get existing data from DB')
    get_parser.add_argument('--target', choices=['student', 'session', 'test'])
    get_parser.add_argument('--files', nargs='*', help='names of elements to get')

    update_parser = subparsers.add_parser('post', help='Update existing data')
    update_parser.add_argument('--target', choices=['student', 'session', 'test'])
    update_parser.add_argument('--files', nargs='+', help='names of elements to update')

    reset_parser = subparsers.add_parser('reset', help='Reset DB')
    # reset_parser.add_argument('--files', nargs='+', help='names of elements to reset')

    # Optional args
    parser.add_argument('-v','--verbose',action='store_true', help='Perform actions in verbose mode')
    parser.add_argument('--limit', type=int,default=10, help='Update any number of test JSON files')
    

    return parser.parse_args()


def main(args):
    script_path = os.path.dirname(os.path.realpath('__file__'))
    print(args)

    engine = sa.create_engine("sqlite:///tutoring_tracker.db", echo=args.verbose) # Set echo to false for quiet output
    # metadata = sa.MetaData()
    # metadata.reflect(bind=engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        # if len(args) < 1:
        #     print("Please enter a command.")

        tbls = session.execute(sa.text("""PRAGMA table_info(tests_table); """))
        print(tbls)

        if args.command == 'reset':
            ans = input("Are you sure you want to reset the database? ")
            if ans.lower() == 'yes':
                statement = sa.select(Student)
                objects = session.scalars(statement).all()
                for obj in objects:
                    session.delete(obj)

        elif args.command == 'post':
            print("Adding student...") # Need to check if element exists first
            for element in args.files:
                name_split = element.lower().split(' ')
                name = '_'.join(name_split)

                fpth = os.path.join(script_path,"./data",f"{args.target}_data/",f"{name}.json")
                with open(fpth,'r') as file:
                    student_dt = json.load(file)

                    # need query stmt to check if user with same email is already in database. if not, add them. if so, indicate they already exist

                    insert_stmt = sa.insert(Student).values(student_dt)
                    session.execute(insert_stmt)

        elif args.command == 'get': # use queries.py
            if args.target == 'student':
                student_dt = queries.get_students(session, args)
            elif args.target == 'session':
                session_dt = queries.get_elements(session,args,TutoringSession)
            elif args.target == 'test':
                test_dt = queries.get_elements(session,args,Test)
            else:
                print('invalid element')

        elif len(args) > 1 and args[1] == "queryconnect":
            stmt = sa.text('''SELECT * FROM students_table
            WHERE name = :name''')
            students = session.execute(stmt, {"name": "First Last"})
            for student in students:
                print(student)

        session.commit()

if __name__ == "__main__":
    args = parser_fcn(sys.argv[1:])
    main(args)