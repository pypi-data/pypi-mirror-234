#!/usr/bin/env python3
import psycopg2
import json
import psycopg2.extras
from datetime import datetime
from typing import Dict
from typing import Union

"""
Db
"""


# cursor.insertBatch('prices', rows, 'time,code')
def insertBatch(cursor, table, rows, onConflictKeys=None)->int:
    if len(rows) <= 0:
        return
    if str(type(rows)) == "<class 'pandas.core.frame.DataFrame'>":
        keys = list(rows.keys())
        values = rows.values
    else:
        keys = list(rows[0].keys())
        values = [list(row.values()) for row in rows]

    key_fields = ",".join(keys)
    value_format = ",".join(["%s"] * len(keys))

    sql = f"insert into {table}({key_fields}) values({value_format})"
    if onConflictKeys:
        update_keys = set(keys) - set(onConflictKeys.split(","))
        if len(update_keys) > 0:
            sql += f" ON CONFLICT({onConflictKeys})"
            sql += f" DO UPDATE set " + ",".join(
                [key + "=EXCLUDED." + key for key in keys]
            )
        else:
            sql += f" ON CONFLICT DO NOTHING"
    # print(sql, values)
    try:
        values = [[json.dumps(d) if type(d)==dict else d for d in row] for row in values]
        cursor.executemany(sql, values)
        return cursor.rowcount
    except Exception as e:
        print("bad sql:",cursor.query)
        raise e



# onConflictKeys="key1,key2"
def insertUpdate(cursor, table, row, onConflictKeys='', returnId=False)->int:
    keys = tuple(row.keys())
    values = tuple(row.values())

    key_fields = ",".join(keys)
    value_format = ",".join(["%s"] * len(keys))
    conflictKeys= onConflictKeys.split(",")

    sql = f"insert into {table}({key_fields}) values({value_format})"
    if onConflictKeys:
        update_keys = set(keys) - set(onConflictKeys.split(","))
        if len(update_keys) > 0:
            sql += f" ON CONFLICT({onConflictKeys})"
            sql += f" DO UPDATE set " + ",".join(
                [key + "=EXCLUDED." + key for key in keys]
            )
        else:
            sql += f" ON CONFLICT DO NOTHING"
    if returnId:
        sql += f" RETURNING id"
    # print(sql, values)
    try:
        values = [json.dumps(d) if type(d)==dict else d for d in values]
        cursor.execute(sql, values)
        if returnId:
            return cursor.fetchone()[0]
    except psycopg2.errors.UniqueViolation as e:
        if not onConflictKeys:
            print("bad sql:",cursor.query)
            raise e
        # conflictKeys += uk

        sql = f'update {table} set'
        set_keys = ','.join([f'"{k}"=%s' for k in keys])
        where_keys = ' and '.join([f'"{k}"=%s' for k in conflictKeys])
        values += [row[k] for k in conflictKeys]
        sql = f'{sql} {set_keys} where {where_keys}'
        cursor.execute(sql, values) 

    except Exception as e:
        print("bad sql:",cursor.query)
        raise e

class SimpleDictCursor(psycopg2.extras.DictCursor):
    def insertBatch(cursor, *args, **kwargs): 
        return insertBatch(cursor, *args, **kwargs)

    def insertUpdate(cursor, table, row, onConflictKeys='', returnId=False): 
        return insertUpdate(cursor, table, row, onConflictKeys, returnId)

# SimpleDictCursor.insertUpdate = insertUpdate

def getDbCursor(dbconf: Dict[str,Union[str,int]])->SimpleDictCursor:
    # {database, user,  password, host, port}
    conn = psycopg2.connect(**dbconf)
    conn.set_session(readonly=False, autocommit=True)
    # cursor = conn.cursor()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.insertBatch = insertBatch.__get__(cursor)
    cursor.insertUpdate = insertUpdate.__get__(cursor)
    return cursor


def loop_file(file_path):
    for line in open(file_path):
        wfid = line.strip().split(',')[-1]
        if wfid:
            fetch_time(wfid)

def fetch_time(wfid):
    cursor.execute(f'select start_time from current_workflows where workflow_id=%s', [wfid])
    res = cursor.fetchone()
    if res:
        ctime = res['start_time']
        print(wfid, ctime)
        return ctime

if __name__ == "__main__":
    dbconf={
            "database":"ahuigo",
             "user":"ahui", 
    }
    cursor = getDbCursor(dbconf)
    cursor.execute(f'select code,label from t where code=%s', ['a1'])
    res = cursor.fetchone()
    print('query:',cursor.query)
    print("res", res["code"])
    print("res", dict(res))

