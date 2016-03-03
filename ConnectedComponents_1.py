import numpy as np
import cv2
import sqlite3 as lite
from itertools import groupby

conn = lite.connect('RLE')

curs4=conn.execute("SELECT ID, RUN FROM RLE4 ORDER BY ID")
rows4=curs4.fetchall()

curs3=conn.execute("SELECT ID, ROW, Start_Col, End_Col, PermLabel from RLE3 ORDER BY ROW, Start_Col")
rows3=curs3.fetchall()

curs2=conn.execute("SELECT LINE, ROW_Start, Row_End FROM RLE2 ORDER BY LINE")
rows2=curs2.fetchall()

#RLE3 - rows3 field numbers
fRun=0
fRow=1
fStartCol=2
fEndCol=3
fPermLabel = 4

#RLE2 - rows2 field numbers
f2Row=0
f2FirstRun=1
f2LastRun=2


lastLabel=0
currRec=0
maxRec=len(rows3)-1

while currRec<=maxRec:
    if rows3[currRec][fRun]==1:
        lastLabel = lastLabel+1

        ###rows3[currRec][fPermLabel]=lastLabel
    else:
        currRow=rows3[currRec][fRow]
        currStart = rows3[currRec][fStartCol]
        currEnd = rows3[currRec][fEndCol]
        currPL = rows3[currRec][fPermLabel]

        prevRow=currRow-1
        prevRun=rows2[prevRow][f2FirstRun]
        prevMaxRun = rows2[prevRow][f2LastRun]
        prevRec=rows4[currRec][1]
        while prevRun<=prevMaxRun:
            if (rows3[prevRec][fEndCol]<currStart) | (rows3[prevRec][fStartCol]>currEnd):
                #no overlap - nothing to do
                lastLabel=lastLabel+1
        
                #rows3[currRec][4]=lastLabel
                lst=list(rows3[currRec])
                lst[4]=lastLabel
                rows3[currRec]=tuple(lst)
            
            else:
                if currPL == 0:
                    #rows3[currRec][4]=rows[prevRec][4]
                    lst=list(rows3[currRec])
                    lst[4]=rows3[prevRec][fPermLabel]
                    rows3[currRec]=tuple(lst)
    
    
                else:
                    #rows3[prevRec][4]=rows[currRec][4]
                    lst=list(rows3[prevRec])
                    lst[4]=rows3[currRec][fPermLabel]
                    rows3[prevRec]=tuple(lst)

            prevRun=prevRun + 1
            
    currRec=currRec+1

