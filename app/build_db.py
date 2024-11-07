import sqlite3
import csv

#TO USE ANY OF THIS type:
#import * from .build_db
#It shoulllld creat the db + tables automatically
DB_FILE = "blogs.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

# Makes tables in the database (do not run, run at the end of the file)
def makeDb():
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, blogname TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS blogs (blogname TEXT, numEntries INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS entries (blogname TEXT, title TEXT, entry TEXT, date TEXT)")
    db.commit()

# Registers a user with a username and password
def addUser(u, p):
    c.execute(f"INSERT INTO users (username, password) VALUES ('{u}', '{p}')")
    exportUsers()
    db.commit()

# Adds a blogname to a user, creates a new blog with 0 entries
def addBlog(user, b):
    c.execute(f"UPDATE users SET blogname = '{b}' WHERE username = '{user}'")
    c.execute(f"INSERT INTO blogs (blogname, numEntries) VALUES ('{b}', 0)")
    exportBlogs()
    db.commit()

# Adds an entry to a pre-existing blog
def addEntry(bname, title, txt, dat):
    c.execute(f"UPDATE blogs SET numEntries = numEntries + 1 WHERE blogname = '{bname}'")
    c.execute(f"INSERT INTO entries (blogname, title, entry, date) VALUES ('{bname}', '{title}', '{txt}', '{dat}')")
    exportEntries()
    db.commit()

# Gets a list of entries for a specific blog given the blog name
def getEntries(bname):
    c.execute(f"SELECT title, entry, date FROM entries WHERE blogname = '{bname}'")
    return c.fetchall()

def getEntry(title):
    c.execute("SELECT blogname, entry, date FROM entries WHERE title = ?", (title,))
    return c.fetchone()  # This returns the first matching row, or None if no match is found

# Gets a random entry from the entries table
def getRandomEntry():
    c.execute("SELECT blogname, title, entry, date FROM entries ORDER BY RANDOM() LIMIT 1")
    return c.fetchone()  # Fetches a random entry


No problem! To retrieve the blogname, title, entry, and date for the most recent blog entry, you can simply adjust the SQL query to select all four fields (blogname, title, entry, and date).

Updated SQL Query:
sql
Copy code
SELECT b.blogname, e.title, e.entry, e.date
FROM entries e
JOIN blogs b ON e.blogname = b.blogname
JOIN users u ON b.blogname = u.blogname
WHERE u.username = ?
ORDER BY e.date DESC
LIMIT 1
Explanation:
b.blogname: The blogname from the blogs table.
e.title: The title from the entries table.
e.entry: The entry (content of the blog post) from the entries table.
e.date: The date from the entries table.
ORDER BY e.date DESC: This sorts the entries by date in descending order to get the most recent entry.
LIMIT 1: Limits the result to just one row, which will be the most recent entry.
Updated Python Code:
Here’s how you can fetch the blogname, title, entry, and date from this query:

python
Copy code
def getMostRecentEntry(username):
    # Get the most recent entry for the user's blog, including blogname, title, entry, and date
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
    c.execute(f"SELECT password FROM users WHERE username = '{user}'")
    return c.fetchone()

# Gets a list of all blognames (no entries)
def listAllBlogs():
    c.execute("SELECT blogname FROM blogs")
    return c.fetchall()

# Deletes a blog
def deleteBlog(bname):
    c.execute(f"DELETE FROM blogs WHERE blogname = '{bname}'")
    c.execute(f"DELETE FROM entries WHERE blogname = '{bname}'")
    exportBlogs()
    exportEntries()
    db.commit()

# Deletes a user
def deleteUser(username):
    c.execute(f"SELECT blogname FROM users WHERE username = '{username}'")
    blognames = [row[0] for row in c.fetchall()]
    for blog in blognames:
        deleteBlog(blog)
    c.execute(f"DELETE FROM users WHERE username = '{username}'")
    exportUsers()
    db.commit()

# Helper function to export data to CSV
def exportToCSV(query, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        c.execute(query)
        writer.writerow([i[0] for i in c.description])  # Write header
        writer.writerows(c.fetchall())  # Write data

# Export Users to CSV (helper)
def exportUsers():
    exportToCSV("SELECT * FROM users", 'users.csv')

# Export Blogs to CSV (helper)
def exportBlogs():
    exportToCSV("SELECT * FROM blogs", 'blogs.csv')

# Export Entries to CSV (helper)
def exportEntries():
    exportToCSV("SELECT * FROM entries", 'entries.csv')

makeDb()
db.close()
