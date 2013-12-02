# coding: utf8
#db = DAL('sqlite://storage.sqlite',pool_size=1)
db = DAL("sqlite://storage.sqlite")
'''
this table functions to retain both the problem text, likely 
accompanied by an image directly from the book, hand-out etc.
'''
db.define_table('problem',
    Field('title'),
    Field('chapter', 'integer'),
    Field('problem', 'integer'),
    Field('problem_image', 'upload'),
    Field('body', 'text'),
    Field('solution_image', 'upload'),
    Field('solution'),
    Field('status'),
    Field('origin'),
    Field('comments', 'text'),
    format = '%(problem)s')

#'''progress refers both to proposals and critiques'''
db.define_table('progress',
    Field('problem_id', 'reference problem'),
    Field('perspective'),
    Field('body', 'text'),
    Field('comments', 'text'),
    Field('created_by'),
    Field('created_on'))

'''this is my timer, reminder and monitor'''
db.define_table('crontime',
    Field('crontab'),
    format = '%(crontime)s')

db.define_table('snode',
    Field('parent_id', 'reference self'),
    Field('root', 'integer'),
    Field('title'),
    Field('body', 'text'))

db.problem.title.requires = IS_NOT_IN_DB(db, db.problem.title)
db.progress.problem_id.requires = IS_IN_DB(db, db.problem.id, '%(title)s')
db.problem.title.requires = IS_NOT_IN_DB(db, 'problem.title')
db.problem.body.requires = IS_NOT_EMPTY()
db.problem.solution.readable = db.problem.solution.writable = False
##db.problem.created_on.readable = db.page.created_on.writable = False

db.progress.body.requires = IS_NOT_EMPTY()
db.progress.problem_id.readable = db.progress.problem_id.writable = False
db.progress.created_by.readable = db.progress.created_by.writable = False
db.progress.created_on.readable = db.progress.created_on.writable = False

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)
