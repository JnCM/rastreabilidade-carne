# coding: utf-8
import MySQLdb
from rastreio_carne_ufv import settings

def connectDb():
    
    db = MySQLdb.connect(
        host=settings.HOST_DB_ITUTEMP,
        user=settings.USER_DB_ITUTEMP,
        passwd=settings.PASSWORD_DB_ITUTEMP,
        db=settings.NAME_DB_ITUTEMP
    )

    db.set_character_set("utf8")

    return db


def select(table, columns, condition="", order_by=""):
    try:
        sql = "SELECT "
        tamColumns = len(columns) - 1
        for i, column in enumerate(columns):
            sql += column
            if i < tamColumns:
                sql += ","
        sql += " FROM {}".format(table)
        
        if condition != "":
            sql += " WHERE {}".format(condition)
        
        if order_by != "":
            sql += " ORDER BY {}".format(order_by)
        
        mydb = connectDb()
        mydb.query(sql)
        result = mydb.use_result().fetch_row(0, how=1)
        result = list(result) if result != "" and result != None else ""
        mydb.close()
        # print("RESULT: {}".format(result))
        return result
    except Exception as e:
        print("Erro no select: ", e.args)
        return "ERROR"