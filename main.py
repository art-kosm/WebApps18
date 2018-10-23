# coding=UTF-8

import cherrypy
import codecs
import mysql.connector
import settings
import os, os.path
import types
import room_types

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


def active_room_attributes(cnx, active_room):
    if not active_room:
        return None
    active_room = int(active_room)
    if type(active_room) != int:
        raise Exception

    cursor = cnx.cursor()

    query = "SELECT id, name, cost FROM spa.room_type"
    cursor.execute(query)
    room_types = {i: (name, cost) for i, name, cost in cursor.fetchall()}

    query = "SELECT room_type, number_of_windows FROM spa.rooms WHERE id = {};".format(active_room)
    cursor.execute(query)
    rows = cursor.fetchall()

    if len(rows) != 1:
        raise Exception

    for room_type, number_of_windows in rows:
        room = {}
        room['number'] = str(active_room)
        room['room_type_name'] = room_types[room_type][0]
        room['room_type_cost'] = room_types[room_type][1]

    return room


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
                login_page = os.path.join('html', 'main.html')
                f = codecs.open(login_page, encoding='utf-8')
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
    def map(self, active_room=None):
        if 'sid' not in cherrypy.session:
            return login_page("init")
        try:
            cnx = mysql.connector.connect(user=settings.user,
                                          password=settings.password,
                                          host=settings.host,
                                          database=settings.database)
            cursor = cnx.cursor()
            query = "SELECT id, room_type, number_of_windows, x, y FROM spa.rooms"
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                return error_page("Ошибка, карта базы не обнаружена!")

            areas = []
            for identificator, room_type, number_of_windows, x, y in rows:
                COEF = 6
                x1 = x * room_types.COEF
                y1 = y * room_types.COEF
                x2, y2 = room_types.NEXT_CORNER[room_type](x, y)

                areas.append('<area  class="room_area" shape="rect" id=' + str(identificator)
                    + ' title="room '
                    + str(identificator)
                    + '" alt="room '
                    + str(identificator)
                    + '" coords="'
                    + ','.join(map(str, [x1, y1, x2, y2]))
                    + '">')

            f = codecs.open('html/map.html', encoding='utf-8')
            temp = f.read()
            rend = Template(temp)
            rend.heading = u"База отдыха 'ПУНК'"
            rend.map = 'png/map.png'
            rend.areas = '\n\t\t'.join(areas)
            rend.rooms = {120, 230, 390}
            # rend.active = active_room_attributes(cnx, active_room)
            return unicode(rend)
        except Exception, e:
            cherrypy.log("Root. Template Render Failure!", traceback=True)
            return error_page(str(e))

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': server_host, 'server.socket_port': server_port,})
    cherrypy.quickstart(Root(), '/', "app.conf")
