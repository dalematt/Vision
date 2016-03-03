import numpy as np
import cv2
import sqlite3 as lite
from itertools import groupby

conn = lite.connect('RLE')

curs4=conn.execute("DROP TABLE if exists RLE4")
curs4 = conn.execute("CREATE TABLE RLE4 (ID INT, RUN INT)")

curs3=conn.execute("SELECT ID, ROW, Start_Col, End_Col, PermLabel from RLE3 ORDER BY ROW, Start_Col")
rows3=curs3.fetchall()

currRec=0
while currRec<=len(rows3)-1:
    
    
    cID=currRec
    cRun = rows3[currRec][0]
    curs4.execute("INSERT INTO RLE4 VALUES (?,?); ",(int(cID),int(cRun)))    
    
    currRec = currRec + 1

conn.commit()
curs4.close
curs3.close

    
