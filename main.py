
import sqlalchemy as sa
from sqlalchemy.orm import Session, mapped_column, Mapped
import datetime
import pathlib
import json
import os
import argparse
import sys

import command_queries
from src.db_schema import Base, Student, Test, TutoringSession
    
def parser_fcn(args):
    parser = argparse.ArgumentParser(
        prog='Tutoring Tracker',
        description='Manage students and sessions using Tutoring Tracker',
        epilog='Thanks for using Tutoring Tracker!')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Positional args

    # POST
    post_user_parser = subparsers.add_parser('post_user', help='Post user data to DB')
    post_user_parser.add_argument('--target', choices=['student', 'tutor'])
    post_user_parser.add_argument('--name', nargs='+', help='JSON files to add')

    post_element_parser = subparsers.add_parser('post_element', help='Get element data from DB')
    post_element_parser.add_argument('--target', choices=['sessions', 'tests'])
    post_element_parser.add_argument('--name', nargs=1, help='name of user to post elements to. encapsulate in ""')
    post_element_parser.add_argument('--files', nargs='*', help='name(s) of file(s) to post') #how should I name the files?

    get_user_parser = subparsers.add_parser('get_user', help='post user data to DB')
    get_user_parser.add_argument('--target', choices=['student', 'tutor'])
    get_user_parser.add_argument('--name', nargs='*', help='name(s) of user(s) to get. encapsulate in ""')
    
    get_element_parser = subparsers.add_parser('get_element', help='Get element data from DB')
    get_element_parser.add_argument('--target', choices=['sessions', 'tests'])
    get_element_parser.add_argument('--name', nargs='*', help='name(s) of user(s) to get elements from. encapsulate in ""')
    get_element_parser.add_argument('--test_type', choices=['ACT', 'SAT', 'PSAT'])

    update_user_parser = subparsers.add_parser('update_user', help='Update existing data')
    update_user_parser.add_argument('--target', choices=['student', 'tutor'])
    update_user_parser.add_argument('--name', nargs='+', help='names of users to update. encapsulate each in ""')

    update_element_parser = subparsers.add_parser('update_element', help='Get element data from DB') # is this useful? when would I use this?
    update_element_parser.add_argument('--target', choices=['sessions', 'tests'])

    delete_user_parser = subparsers.add_parser('delete_user', help='Update existing data')
    delete_user_parser.add_argument('--name', nargs='+', help='names of users to delete. encapsulate each in ""')
    
    delete_element_parser = subparsers.add_parser('delete_element', help='Update existing data')
    post_element_parser.add_argument('--files', nargs='*', help='name(s) of file(s) to post') #how should I name the files?

    reset_parser = subparsers.add_parser('reset', help='Reset DB')
    # reset_parser.add_argument('--name', nargs='+', help='names of elements to reset')

    # Optional args
    parser.add_argument('-v','--verbose',action='store_true', help='Perform actions in verbose mode')
    parser.add_argument('--limit', type=int,default=10, help='Set maximum number of results')
    

    return parser.parse_args()


def main(args):
    script_path = os.path.dirname(os.path.realpath('__file__'))
    if args.verbose:
        print(args)

    engine = sa.create_engine("sqlite:///tutoring_tracker.db", echo=args.verbose) # Set echo to false for quiet output
    # metadata = sa.MetaData()
    # metadata.reflect(bind=engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session, session.begin():
        # if len(args) < 1:
        #     print("Please enter a command.")

        if args.command == 'reset':
            ans = input("Are you sure you want to reset the database? ")
            if ans.lower() == 'yes':
                statement = sa.select(Student)
                objects = session.scalars(statement).all()
                for obj in objects:
                    session.delete(obj)

        elif args.command == 'post':
            if args.target == 'student':
                student_dt = command_queries.post_students(session, script_path, args)
            elif args.target == 'session':
                session_dt = command_queries.post_tutoring_sessions(session, script_path, args)
            elif args.target == 'test':
                test_dt = command_queries.post_tests(session,args, script_path, args)
            else:
                print('invalid element')
            

        elif args.command == 'get': # use command_queries.py
            if args.target == 'student':
                student_dt = command_queries.get_students(session, args)
            elif args.target == 'session':
                session_dt = command_queries.get_tutoring_sessions(session, args)
            elif args.target == 'test':
                test_dt = command_queries.get_tests(session, args)
            else:
                print('invalid element')

        session.commit()

if __name__ == "__main__":
    args = parser_fcn(sys.argv[1:])
    main(args)