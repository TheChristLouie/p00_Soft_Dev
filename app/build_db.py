#Stella Yampolsky
#SoftDev
#Oct 2024

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

#create the database + tables
#Run before using functions
#Run only once

DB_FILE="blogs.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

def makedb():
    c.execute("create table users (username text, password text, blogname text)")
    c.execute("create table blogs (blogname text, int empty)")
    c.execute("create table entries (blogname text, title text, entry text int date)")
#When a user registers, before they make their blog
def addUser(u, p):
    c.execute("insert into users values(u, p)")
def addBlog(user, b):
    c.execute("insert into users select(user)(blogname) values(b)")

makedb()
#addUser("name","1234")

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

db.commit() 
db.close()  
