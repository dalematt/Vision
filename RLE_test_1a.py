import numpy as np
import cv2
import sqlite3 as lite
from itertools import groupby

image=cv2.imread("C:\Users\dmatt\Documents\Music\Music Software\Mozart_DieZauberflote_page1_7380_1_9.bmp")

conn = lite.connect('RLE')
curs=conn.execute("DROP TABLE if exists RLE1")
curs2=conn.execute("DROP TABLE if exists RLE2")
curs3=conn.execute("DROP TABLE if exists RLE3")

curs = conn.execute("CREATE TABLE RLE1 (ID INT, ROW INT, Type INT, Start_Col Int, End_Col Int, PermLabel INT)")
curs2=conn.execute("CREATE TABLE RLE2 (LINE INT, Row_Start INT, Row_End INT)")
curs3=conn.execute("CREATE TABLE RLE3 (ID INT, ROW INT, Type INT, Start_Col Int, End_Col Int, PermLabel INT)")

CurrID = 0

max_Row=len(image)
i=0

while i<=max_Row-1:
    image_Row = image[i,:,0]
    a=[(k, sum(1 for _ in g)) for k,g in groupby(image[i,:,0])]
    CurrColumn = 0
    j=0
    FirstRun = 0
    CurrRun = 0

    for item in a:
        CurrID = CurrID + 1
        

        
        CurrRow = i
        CurrType = a[j][0]
        CurrEndColumn = CurrColumn + a[j][1]-1
        curs.execute("INSERT INTO RLE1 VALUES (?,?,?,?,?,?); ",(CurrID, int(CurrRow),int(CurrType),CurrColumn,CurrEndColumn,0))

        # add to RLE2 if black 
        if CurrType == 0:
            curs3.execute("INSERT INTO RLE3 VALUES (?,?,?,?,?,?); ",(CurrID, int(CurrRow),int(CurrType),CurrColumn,CurrEndColumn,0))
            CurrRun = CurrID
            if FirstRun == 0:
                FirstRun = CurrID

        
        CurrColumn = CurrColumn + a[j][1]
        j=j+1

    #update RLE2
    curs2.execute("INSERT INTO RLE2 VALUES (?,?,?); ",(int(i),int(FirstRun),int(CurrRun)))

    i=i+1
    print (CurrID, i)

    conn.commit()



