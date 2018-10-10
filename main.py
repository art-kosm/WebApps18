# coding=UTF-8

import cherrypy
import codecs
from Cheetah.Template import Template
import mysql.connector
import settings 
import os, os.path
from datetime import date
from datetime import datetime, timedelta

server_host = settings.server_host
server_port = settings.server_port

def login_page(message):
    f = codecs.open('html\login.html', encoding='utf-8')
    temp = f.read() 
    rend = Template(temp)
    rend.message = message
    return unicode(rend)

def error_page(message="Ошибка сервера. Обратитесь к администратору."):
    return message

class Root(object):
    @cherrypy.expose
    def checklogin(self, username, passwd, action):
        try:
            cnx = mysql.connector.connect(user=settings.user, password=settings.password, host=settings.host, database=settings.database)
            cursor = cnx.cursor()
            query = "SELECT password FROM spa.users WHERE user_name = %s "
            cursor.execute(query, [username])
            rows = cursor.fetchall()
            if len(rows) > 0:
                if (rows[0][0] == passwd):
                    cherrypy.session['sid'] = cherrypy.session.id
                    raise cherrypy.HTTPRedirect("/")
                else:
                    return login_page("Отказано в доступе!")
            else:
                return login_page("Отказано в доступе! " + cursor._last_executed)
        except cherrypy.HTTPRedirect:
            raise
        except Exception, e:
            return login_page("Отказано в доступе!")
            
    @cherrypy.expose
    def index(self):
        if 'sid' not in cherrypy.session:
            return login_page("init")
        else:
            try:
                f = codecs.open('html\main.html', encoding='utf-8')
                temp = f.read() 
                rend = Template(temp)
                rend.heading = u"База отдыха 'ПУНК'"
                return unicode(rend)
            except Exception, e:
                cherrypy.log("Root. Template Render Failure!", traceback=True)
                return error_page(str(e))

    @cherrypy.expose
    def logout(self):
        cherrypy.session.delete()
        return login_page("init")
            
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': server_host, 'server.socket_port': server_port,})
    cherrypy.quickstart(Root(), '/', "app.conf")
