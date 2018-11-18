# coding=UTF-8

import cherrypy
import codecs
import mysql.connector
import settings
import os, os.path
import types
import json

from Cheetah.Template import Template
from datetime import date
from datetime import datetime, timedelta
from copy import copy
from functools import partial


server_host = settings.server_host
server_port = settings.server_port


def login_page(message):
    login_page = os.path.join('html', 'login.html')
    f = codecs.open(login_page, encoding='utf-8')
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
            cnx = mysql.connector.connect(user=settings.user,
                                          password=settings.password,
                                          host=settings.host,
                                          database=settings.database)
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
                login_page1 = os.path.join('html', 'main.html')
                f = codecs.open(login_page1, encoding='utf-8')
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

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def room(self, id):
        cnx = mysql.connector.connect(user=settings.user,
                                      password=settings.password,
                                      host=settings.host,
                                      database=settings.database)
        return active_room_attributes(cnx, id)

    @cherrypy.expose
    def map(self):
        if 'sid' not in cherrypy.session:
            return login_page("init")
        try:
            cnx = mysql.connector.connect(user=settings.user,
                                          password=settings.password,
                                          host=settings.host,
                                          database=settings.database)
            cursor = cnx.cursor()
            query = "SELECT id_room, room_type FROM spa.rooms"
            cursor.execute(query)
            rows = cursor.fetchall()

            f = codecs.open('html/map.html', encoding='utf-8')
            temp = f.read()
            rend = Template(temp)
            rend.heading = u"База отдыха 'ПУНК'"
            rend.rooms = [x[0] for x in rows]
            return unicode(rend)
        except Exception, e:
            cherrypy.log("Root. Template Render Failure!", traceback=True)
            return error_page(str(e))
    
    @cherrypy.expose
    def submit_dates(self, room_id):
        #cherrypy.response.headers['Content-Type'] = 'application/json'
        id = int(room_id)
        try:
            cnx = mysql.connector.connect(user=settings.user,
                                          password=settings.password,
                                          host=settings.host,
                                          database=settings.database)
            cursor = cnx.cursor()
            query = ("SELECT id_room, start_date, end_date FROM spa.booking WHERE id_room = %d" % id)
            cursor.execute(query)
            rows = cursor.fetchall()
            format = "%Y-%m-%d"
            dates = []
            for x in rows:
                dates += [date.fromordinal(i).strftime(format) for i in range(x[1].toordinal(), x[2].toordinal() + 1)]
            message = { "dates" : dates }
            return json.dumps(message)
        except Exception, e:
            cherrypy.log("Some MySQL error", traceback=True)
            return json.dumps(dict(room_info="Error"))
    
    @cherrypy.expose
    def book_dates(self, room_id, start_date, end_date, name, phone_number):
        try:
            id = int(room_id)
            format = "%d/%m/%Y"
            values = (id, datetime.strptime(start_date, format).date(), datetime.strptime(end_date, format).date(), name, phone_number)
            cnx = mysql.connector.connect(user=settings.user,
                                          password=settings.password,
                                          host=settings.host,
                                          database=settings.database)
            cursor = cnx.cursor()
            insert = ("INSERT INTO spa.booking (id_room, start_date, end_date, FULL_NAME, PHONE_NUMBER) VALUES(%s, %s, %s, %s, %s)")
            cursor.execute(insert, values)
            cnx.commit()
            return json.dumps(dict(room_info="Success"))
        except Exception, e:
            cherrypy.log("MySQL insert problem", traceback = True)
            return error_page(str(e))

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': server_host, 'server.socket_port': server_port,})
    cherrypy.quickstart(Root(), '/', "app.conf")
