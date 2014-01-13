from datetime import datetime

def get_username():
    if auth.user:
        return auth.user.username
    else:
        return 'None'

def nadmin():
    if (get_username()=='jeanpaulsc'):
        return 1
    else:
        return 'None'

def get_email():
    if auth.user:
        return auth.user.email
    else:
        return 'None'

def get_user_id():
    if auth.user:
        return auth.user.id
    else:
        return 'None'

@auth.requires_login()
db.define_table('subject',
    Field('user_id', default=get_user_id),
    Field('neophyte', default=get_username()),
    Field('title'),
    format = '%(subject)s')

db.define_table('note',
    Field('subject_id', 'reference subject'),
    Field('title'),
    Field('body', 'text'),
    Field('created_by', default=get_username()),
    Field('created_on', 'datetime', default=datetime.utcnow()),
    format = '%(note)s')

'''
this table functions to retain both the problem text, likely
accompanied by an image directly from the book, hand-out etc.
'''
db.define_table('problem',
    Field('subject_id', 'reference subject'),
    Field('neophyte', default=get_username()),
    Field('title'),
    Field('problem_image', 'upload'),
    Field('solution_image', 'upload'),
    Field('status', default='active'),
    Field('critiques', 'text'),
    format = '%(problem)s')

db.define_table('effort',
    Field('problem_id', 'reference problem'),
    Field('body', 'text'),
    Field('tex', 'text'),
    format = '%(effort)s')

#'''progress refers both to proposals and critiques'''
db.define_table('progress',
    Field('problem_id', 'reference problem'),
    Field('critique', 'text'),
    Field('created_by', default=get_username()),
    Field('created_on', 'datetime', default=datetime.utcnow()))

db.problem.title.requires = IS_NOT_IN_DB(db, db.problem.title)
db.progress.problem_id.requires = IS_IN_DB(db, db.problem.id, '%(title)s')
db.problem.title.requires = IS_NOT_IN_DB(db, 'problem.title')
db.progress.created_on.readable = db.progress.created_on.writable = False
db.progress.critique.requires = IS_NOT_EMPTY()
db.progress.problem_id.readable = db.progress.problem_id.writable = False
db.progress.created_by.readable = db.progress.created_by.writable = False
db.progress.created_on.readable = db.progress.created_on.writable = False

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)
