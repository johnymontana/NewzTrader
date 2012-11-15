# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
from lxml import etree
import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil.parser import parse

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "Welcome to web2py!"
    todaysNews = get_headlines(date.today())
    return dict(news=todaysNews)
    
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
def only_alphanum(s):
    #s = unicode(s, "utf-8")
    return ' '.join(c for c in s.split() if c.isalnum())
def only_alpha(s):
    return ' '.join(c for c in s.split() if c.isalpha())
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def get_headlines(newsDate):
    
    news={}
    year = newsDate.year
    month = newsDate.month
    day = newsDate.day
    news[newsDate]=[]
    path = "http://api.newscred.com/articles?access_key=c4bcc3f7c9bf9ec159f51da0a86ca658&sources=104afa30d811d37a5582a39e1662a311&pagesize=99&from_date=%d-%d-%d&to_date=%d-%d-%d 23:59:59" % (year, month, day, year, month, day)
    while True:
        try:
            root = etree.parse(path)
            break
        except XMLSyntaxError:
            pass
    myRoot = root.getroot()

    #news[date(year, month, day)]=[]
    #descs[date(year, month, day)]=[]
    for element in myRoot.iter("article"):
        #for item in element.iter("description"):
         #   desc = item.text
        for item in element.iter("title"):
            title = item.text
        for item in element.iter("created_at"):
            pubDate = parse(item.text)
    
        news[pubDate.date()].append(only_alphanum(removeNonAscii(title)))
    return news
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


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
