from app import db
import json, os


def get_all(table):
    results = None
    try:
        db.execute("SELECT * FROM "+table)
        results = db.fetchall()
    except Exception as e:
        return str(e)
    else:
        return results


def get_by_id(table, field= None, value= None):
    results = list()
    try:
        db.execute("SELECT * FROM "+table+" WHERE "+field+"=%s",(value,))
        results = db.fetchall()
    except Exception as e:
        raise e
    else:
        return results


def insert(table, data = None):
    returning = ""
    if os.getenv('DB_DRIVER') == 'cockroachdb' or os.getenv('DB_DRIVER') == 'postgresql':
        returning = "RETURNING *"
    value = ''
    column = ''
    for row in data:
        column += row+","
        value += "'"+str(data[row]+"',")
    column = "("+column[:-1]+")"
    value = "("+value[:-1]+")"
    try:
        db.execute("INSERT INTO "+table+" "+column+" VALUES "+value+" "+returning)
        status = True
    except Exception as e:
        raise e
    else:
        return status

def update(table, data = None):
    value = ''
    rows = data['data']
    for row in rows:
        value += row+"='"+str(rows[row]+"',")
    set = value[:-1]
    field = list(data['where'].keys())[0]
    status = None
    try:
        db.execute("UPDATE "+table+" SET "+set+" WHERE "+field+"="+data['where'][field])
        status = True
    except Exception as e:
        status = e
    else:
        return status


def delete(table, field = None, value = None):
    rows_deleted = 0
    try:
        db.execute("DELETE FROM "+table+" WHERE "+field+" ="+value)
        rows_deleted = db.rowcount
    except Exception as error:
        raise error
    else:
        return rows_deleted

def query(q):
    try:
        db.execute(q)
        return db
    except Exception as e:
        raise e

