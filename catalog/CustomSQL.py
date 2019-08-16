from django.db import connection
from collections import namedtuple
from catalog.models import  User

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def getResultsBySQL(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
    return dictfetchall(cursor)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def executeSQL(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
    return row

def checkUserExist(user_id):
    user=User.objects.raw("SELECT * FROM `user` WHERE user_id='"+user_id+"'")
    if len(list(user)) > 0:
        return True
    else:
        return False

