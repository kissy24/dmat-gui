#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3

con = sqlite3.connect('./dmat.db')
cur = con.cursor()


def getContent():
    ret = cur.execute("select name,skill,area,period from dmatdata")
    return ret.fetchall()


def setContent(name, skill, area, period):
    cur.execute('insert into dmatdata values(?,?,?,?)', [name, skill, area, period])
    con.commit()


if __name__ == '__main__':
    pass
