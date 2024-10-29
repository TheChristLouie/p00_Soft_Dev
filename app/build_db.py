#Clyde "Thluffy" Sinclair
#SoftDev
#skeleton/stub :: SQLITE3 BASICS
#Oct 2024

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="blogs.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#==========================================================
# c.execute("create table students (one text, two int, three int)")
# c.execute("create table courses (one text, two int, three int)")
# with open("students.csv", newline='') as file:
#     r = csv.DictReader(file)    
#     for row in r:
#         c.execute(f"insert into students values('{row['name']}', '{row['age']}', '{row['id']}')")
# file.close()
# with open("courses.csv", newline='') as file:
#     r = csv.DictReader(file)    
#     for row in r:
#         c.execute(f"insert into courses values('{row['code']}', '{row['mark']}', '{row['id']}')")
# file.close()





#==========================================================

db.commit() #save changes
db.close()  #close database
