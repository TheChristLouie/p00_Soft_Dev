import sqlite3
import csv

DB_FILE = "blogs.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

# Function to create a new database connection per request (Flask-friendly)
def get_db():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    return db

# Makes tables in the database (run this once, or after changes)
def makeDb():
    db = get_db()
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, blogname TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS blogs (blogname TEXT, numEntries INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS entries (blogname TEXT, title TEXT, entry TEXT, date TEXT)")
    db.commit()

# Registers a user with a username and password
def addUser(u, p):
    db = get_db()
    c = db.cursor()
    c.execute(f"INSERT INTO users (username, password) VALUES ('{u}', '{p}')")
    exportUsers()
    db.commit()

# Adds a blogname to a user, creates a new blog with 0 entries
def addBlog(user, b):
    db = get_db()
    c = db.cursor()
    c.execute(f"UPDATE users SET blogname = '{b}' WHERE username = '{user}'")
    c.execute(f"INSERT INTO blogs (blogname, numEntries) VALUES ('{b}', 0)")
    exportBlogs()
    db.commit()

# Adds an entry to a pre-existing blog
def addEntry(bname, title, txt, dat):
    db = get_db()
    c = db.cursor()
    c.execute(f"UPDATE blogs SET numEntries = numEntries + 1 WHERE blogname = '{bname}'")
    c.execute(f"INSERT INTO entries (blogname, title, entry, date) VALUES ('{bname}', '{title}', '{txt}', '{dat}')")
    exportEntries()
    db.commit()

# Gets a list of entries for a specific blog given the blog name
def getEntries(bname):
    db = get_db()
    c = db.cursor()
    c.execute(f"SELECT title, entry, date FROM entries WHERE blogname = '{bname}'")
    return c.fetchall()

# Gets a specific entry based on title
def getEntry(title):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT blogname, entry, date FROM entries WHERE title = ?", (title,))
    return c.fetchone()  # This returns the first matching row, or None if no match is found

# Gets a random entry from the entries table
def getRandomEntry():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT blogname, title, entry, date FROM entries ORDER BY RANDOM() LIMIT 1")
    result = c.fetchone()  # Fetches a random entry

    # If no result is found, return a tuple with None values
    return result if result else (None, None, None, None)

def getMostRecentEntry(username):
    db = get_db()
    c = db.cursor()
    c.execute("""
        SELECT b.blogname, e.title, e.entry, e.date
        FROM entries e
        JOIN blogs b ON e.blogname = b.blogname
        JOIN users u ON b.blogname = u.blogname
        WHERE u.username = ?
        ORDER BY e.date DESC
        LIMIT 1
    """, (username,))

    return c.fetchone()

# Gets the user's password (for verification purposes)
def getPass(user):
    db = get_db()
    c = db.cursor()
    c.execute(f"SELECT password FROM users WHERE username = '{user}'")
    return c.fetchone()
def getBlogname(username):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT blogname FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    return result[0] if result else None

# Gets a list of all blognames (no entries)
def listAllBlogs():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT blogname FROM blogs")
    return c.fetchall()

# Deletes a blog
def deleteBlog(bname):
    db = get_db()
    c = db.cursor()
    c.execute(f"DELETE FROM blogs WHERE blogname = '{bname}'")
    c.execute(f"DELETE FROM entries WHERE blogname = '{bname}'")
    exportBlogs()
    exportEntries()
    db.commit()

# Deletes a user
def deleteUser(username):
    db = get_db()
    c = db.cursor()
    c.execute(f"SELECT blogname FROM users WHERE username = '{username}'")
    blognames = [row[0] for row in c.fetchall()]
    for blog in blognames:
        deleteBlog(blog)
    c.execute(f"DELETE FROM users WHERE username = '{username}'")
    exportUsers()
    db.commit()

# Helper function to export data to CSV
def exportToCSV(query, filename):
    db = get_db()
    c = db.cursor()
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        c.execute(query)
        writer.writerow([i[0] for i in c.description])  # Write header
        writer.writerows(c.fetchall())  # Write data

def exportUsers():
    exportToCSV("SELECT * FROM users", 'users.csv')

def exportBlogs():
    exportToCSV("SELECT * FROM blogs", 'blogs.csv')

def exportEntries():
    exportToCSV("SELECT * FROM entries", 'entries.csv')