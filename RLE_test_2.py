import numpy as np
import cv2
import sqlite3 as lite
from itertools import groupby

conn = lite.connect('RLE')
curs3=conn.execute("SELECT ID, ROW, Start_Col, End_Col, PermLabel from RLE3")
rows3=curs3.fetchall()

curs2=conn.execute("SELECT LINE, ROW_Start, Row_End FROM RLE2 ORDER BY LINE")
rows2=curs2.fetchall()

#TOP DOWN PASS
L=0
NLINES = len(rows2)
while L<=NLINES:
    L=L+1
    P=rows2[L][1]
    PLAST=rows2[L][2]
    
    if L==1:
        Q=0
        QLAST=0
    else:
        Q=rows2[L-1][1]
        QLAST=rows2[L-1][2]


    if P<>0 AND Q<>0:
        #INITIALIZE_EQUIV()

    #SCAN 1
    while P<=PLAST and Q<=QLAST:
        ENDCOL_P = [item[3] for item in rows3 if item[0]==P][0]
        STARTCOL_Q = [item[2] for item in rows3 if item[0]==Q][0]
        ENDCOL_Q=[item[3] for item in rows3 if item[0]==Q][0]
        STARTCOL_P=[item[2] for item in rows3 if item[0]==P][0]
        PERMLABEL_P=[item[4] for item in rows3 if item[0]==P][0]
        PERMLABEL_Q=[item[4] for item in rows3 if item[0]==Q][0]

        #CASE
        if  ENDCOL_P<  STARTCOL_Q:
            P=P+1
        elif ENDCOL_Q < STARTCOL_P :
            Q=Q+1
        else:
            PLABEL = PERMLABEL_P

            #CASE
            if PLABEL ==0:
                curs3=conn.execute("UPDATE RLE3 SET PermLabel = ? WHERE ID = ?",([item[4] for item in rows3 if item[0]==Q][0],P))
                curs3=conn.execute("SELECT ID, ROW, Start_Col, End_Col, PermLabel from RLE3")
                rows3=curs3.fetchall()
            elif PLABEL<>0 AND PERMLABEL_Q<> PLABEL:
                #MAKE_EQUIVALENT(PLABEL,PERMLABEL_Q)
            #END CASE
            
            #CASE
            if ENDCOL_P>ENDCOL_Q:
                Q=Q+1
            elif ENDCOL_Q>ENDCOL_P:
                P=P+1
            elif ENDCOL_Q==ENDCOL_P:
                Q=Q+1
                P=P+1
            #END CASE
        #END CASE
    #END WHILE

    #SCAN 2
    P=rows2[L][1]
    WHILE P<=PLAST:
        PLABEL = PERMLABEL_P
        
        #CASE
        IF PLABEL==0:
            ##### NEED NEWLABEL FUNCTION
            PERMLABEL_P=NEWLABEL
        elif PLABEL<>0 AND LABEL:
    #END WHILE
