# -*- coding: utf-8 -*-critiques = db(db.post.image_id==image.id).select()

def index():
    '''This is intended to display problems in groups as chapters'''
    problems = db(db.problem.status=='active').select(db.problem.id,db.problem.title)
    username = get_username()
    return dict(problems=problems, username=username)

def edit_critique():
    critique = db.progress(request.args(0,cast=int))
    form = SQLFORM(db.progress, critique)
    if form.process().accepted:
        response.flash = 'your feedback is posted'
    return dict(form=form)

def critique_list():
    critiques = db().select(db.progress.ALL)
    return dict(critiques=critiques)

@auth.requires_login()
def add_subject():
    """Adds a subject."""
    form = SQLFORM(db.subject)
    if form.process().accepted:
        redirect(URL('default', 'subject_list'))
    return dict(form=form)

@auth.requires_login()
def add_problem():
    """Adds a problem"""
    form = SQLFORM(db.problem)
    if form.process().accepted:
        redirect(URL('default', 'index'))
    return dict(form=form)

def edit():
    problem = db.problem(request.args(0))
    form = SQLFORM(db.problem, problem)
    if form.process().accepted:
        redirect(URL('default', 'index'))
    return dict(form=form, problem=problem)

@auth.requires_login()
def show():
    problem = db.problem(request.args(0,cast=int)) or redirect(URL('index'))
    db.progress.problem_id.default = problem.id
    username=get_username()
    form = SQLFORM(db.progress)
    if form.process().accepted:
        response.flash = 'your feedback is posted'
    critiques = db(db.progress.problem_id==problem.id).select()
    #efforts = db(db.effort.problem_id==problem.id).select()
    return dict(problem=problem, username=username, critiques=critiques, form=form)

def subject_list():
	subjects = db().select(db.subject.id,db.subject.title)
	username=get_username()
	return dict(subjects=subjects, username=username)
	
def show_subject():
    sub_q = db.subject(request.args(0,cast=int)) or redirect(URL('subject_list'))
    db.note.subject_id.default = subject.id
    username=get_username()
    form = SQLFORM(db.note)
    if form.process().accepted:
        response.flash = 'your note is posted'
    note_q = db(db.note.note_id==note.id).select()
    return dict(sub_q=sub_q, username=username, note_q=note_q, form=form)

def download():
    return response.download(request,db)

def link():
    return response.download(request,db,attachment=False)
'''
@auth.requires_login()
def found_group():
    image_form = FORM(
        INPUT(_name='image_title',_type='text'),
        INPUT(_name='image_file',_type='file')
        )

    if image_form.accepts(request.vars,formname='image_form'):
        image = db.image.file.store(image_form.vars.image_file.file, image_form.vars.image_file.filename)
        id = db.image.insert(file=image,title=image_form.vars.image_title)
        images = db().select(db.image.ALL)
        return dict(images=images)
'''
@auth.requires_login()
def critique():
    '''either effort or critique, it's done here'''
    form = SQLFORM(db.progress).process(next=URL('index'))
    return dict(form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())