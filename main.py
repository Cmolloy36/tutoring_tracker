
import sqlalchemy as sa
from sqlalchemy.orm import Session
import os
import argparse
import sys
import json

import command_queries
from export_json import AlchemyEncoder
from src.db_schema import Base, Student, Test, SAT, ACT, PSAT, TutoringSession
    
def parser_fcn(args):
    parser = argparse.ArgumentParser(
        prog='Tutoring Tracker',
        description='Manage students and sessions using Tutoring Tracker',
        epilog='Thanks for using Tutoring Tracker!')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Positional args

    # POST
    post_user_parser = subparsers.add_parser('post_user', help='Post user data to DB')
    post_user_parser.add_argument('--target', choices=['student', 'tutor']) #singular or plural?
    post_user_parser.add_argument('--name', nargs='+', help='JSON files to add')

    post_element_parser = subparsers.add_parser('post_element', help='Post element data to DB')
    post_element_parser.add_argument('--target', choices=['sessions', 'ACT', 'SAT', 'PSAT'])
    post_element_parser.add_argument('--name', nargs=1, help='name of user to post elements to. encapsulate in ""')
    post_element_parser.add_argument('--files', nargs='+', help='name(s) of file(s) to post') #how should I name the files?

    # GET
    get_user_parser = subparsers.add_parser('get_user', help='get user data from DB') #
    get_user_parser.add_argument('--target', choices=['student', 'tutor'])
    get_user_parser.add_argument('--name', nargs='*', help='name(s) of user(s) to get. encapsulate in ""')
    
    get_element_parser = subparsers.add_parser('get_element', help='Get element data from DB')
    get_element_parser.add_argument('--target', choices=['sessions', 'tests', 'ACT', 'SAT', 'PSAT'])
    get_element_parser.add_argument('--name', nargs='*', help='name(s) of user(s) to get elements from. encapsulate in ""')

    # PUT
    update_user_parser = subparsers.add_parser('update_user', help='Update existing data')
    update_user_parser.add_argument('--target', choices=['student', 'tutor'])
    update_user_parser.add_argument('--name', nargs='+', help='names of users to update. encapsulate each in ""')

    update_element_parser = subparsers.add_parser('update_element', help='Update element data in DB') # is this useful? when would I use this?
    update_element_parser.add_argument('--target', choices=['sessions', 'tests'])

    # DELETE
    delete_user_parser = subparsers.add_parser('delete_user', help='Update existing data')
    delete_user_parser.add_argument('--name', nargs='+', help='names of users to delete. encapsulate each in ""')
    
    delete_element_parser = subparsers.add_parser('delete_element', help='Update existing data')
    delete_element_parser.add_argument('--target', choices=['sessions', 'tests', 'ACT', 'SAT', 'PSAT'])
    delete_element_parser.add_argument('--name', nargs=1, help='name of user to delete elements from. encapsulate in ""') # the existence of this indicates I should name files with student name and date
    delete_element_parser.add_argument('--files', nargs='+', help='name(s) of file(s) to delete') #how should I name the files?

    reset_parser = subparsers.add_parser('reset', help='Reset DB')
    # reset_parser.add_argument('--name', nargs='+', help='names of elements to reset')

    # Optional args
    parser.add_argument('-v','--verbose',action='store_true', help='Perform actions in verbose mode')
    parser.add_argument('--limit', type=int,default=10, help='Set maximum number of results')
    parser.add_argument('-e', '--export',action='store_true', help='export queries recieved to the specified path')
    
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
        # session.execute(sa.text("DROP TABLE IF EXISTS _alembic_tmp_sessions_table"))

        if args.command == 'reset': # consider moving to command_queries.py
            ans = input("Are you sure you want to reset the database? ")
            if ans.lower() == 'yes':
                statement = sa.select(Student)
                objects = session.scalars(statement).all()
                for obj in objects:
                    session.delete(obj)

        elif args.command == 'post_user':
            if args.target.lower() == 'student' or 'tutor':
                pre_json_payload = command_queries.post_users(session, script_path, args)
            else:
                print('invalid user element')
            
        elif args.command == 'post_element':
            if args.target.lower() == 'tests' or 'sat' or 'act' or 'psat' or 'sessions':
                pre_json_payload = command_queries.post_elements(session, script_path, args)
            else:
                print('invalid element')

        elif args.command == 'get_user': # use command_queries.py
            if args.target == 'student':
                pre_json_payload = command_queries.get_students(session, args)
            # elif args.target == 'tutor':
            #     test_dt = command_queries.get_tutors(session, args)
            else:
                print('invalid element')

        elif args.command == 'get_element': # use command_queries.py
            if args.target.lower() == 'tests' or 'sat' or 'act' or 'psat' or 'sessions':
                pre_json_payload = command_queries.get_elements(session, args)
            else:
                print('invalid element')

        elif args.command == 'delete_user': # use command_queries.py
            if (args.name != [] or None):
                pre_json_payload = command_queries.delete_users(session, args)
            else:
                print('invalid element')

        elif args.command == 'delete_element': # use command_queries.py
            if (args.files != [] or None) and (args.target.lower() == 'tests' or 'sat' or 'act' or 'psat' or 'sessions'):
                pre_json_payload = command_queries.delete_elements(session, script_path, args)
            else:
                print('invalid element')

        if args.export:
            json_payload = json.dumps(pre_json_payload, cls=AlchemyEncoder)
            if args.verbose:
                print(json_payload) # do what with it? export to csv or something?

if __name__ == "__main__":
    args = parser_fcn(sys.argv[1:])
    main(args)