import sqlite3
import os

# Create an in-memory database
database_path = os.path.abspath("agentic_ai/data/employee.db")
os.makedirs(os.path.dirname(database_path), exist_ok=True)

connection = sqlite3.connect(database_path)

# Create a cursor object
cursor = connection.cursor()

# Create the Employee table with new fields: salary, location, and hire_date
cursor.execute('''
CREATE TABLE Employee (
    employee_name TEXT NOT NULL,
    employee_email TEXT UNIQUE NOT NULL,
    org_name TEXT,
    designation TEXT NOT NULL,
    years_of_experience REAL NOT NULL,
    salary REAL,
    location TEXT,
    hire_date TEXT
);
''')

# Sample data to populate the Employee table, including new fields
employees = [
    ("Alice Johnson", "alice.johnson@example.com", "TechCorp", "Software Engineer", 3.5, 70000, "New York", "2019-06-15"),
    ("Bob Smith", "bob.smith@example.com", "TechCorp", "Product Manager", 7.0, 95000, "San Francisco", "2016-02-10"),
    ("Charlie Brown", "charlie.brown@example.com", "InnovateLtd", "Data Scientist", 2.0, 75000, "Austin", "2020-03-01"),
    ("Diana Prince", "diana.prince@example.com", "InnovateLtd", "Senior Analyst", 5.5, 85000, "Los Angeles", "2017-08-20"),
    ("Eve Davis", "eve.davis@example.com", "CreativeSolutions", "UX Designer", 4.0, 72000, "Chicago", "2018-05-12"),
    ("Frank Miller", "frank.miller@example.com", "CreativeSolutions", "Project Manager", 6.2, 90000, "Seattle", "2015-09-10"),
    ("Grace Hopper", "grace.hopper@example.com", "TechCorp", "Lead Engineer", 10.0, 120000, "New York", "2010-11-01"),
    ("Hank Pym", "hank.pym@example.com", "InnovateLtd", "Research Scientist", 8.5, 95000, "San Francisco", "2014-02-15"),
    ("Irene Adler", "irene.adler@example.com", "CreativeSolutions", "Content Strategist", 3.8, 75000, "Chicago", "2016-06-17"),
    ("Jack Reacher", "jack.reacher@example.com", "TechCorp", "QA Engineer", 2.4, 67000, "Austin", "2020-07-22"),
    ("Karen Page", "karen.page@example.com", "InnovateLtd", "Business Analyst", 6.0, 80000, "Los Angeles", "2014-12-05"),
    ("Leo Messi", "leo.messi@example.com", "TechCorp", "DevOps Engineer", 4.5, 85000, "New York", "2017-01-25"),
    ("Mia Wallace", "mia.wallace@example.com", "CreativeSolutions", "Graphic Designer", 3.3, 65000, "Seattle", "2019-11-30"),
    ("Nick Fury", "nick.fury@example.com", "InnovateLtd", "Operations Head", 15.0, 150000, "San Francisco", "2005-03-22"),
    ("Oscar Wilde", "oscar.wilde@example.com", "TechCorp", "Technical Writer", 5.1, 78000, "Austin", "2016-08-15")
]

# Insert data into the Employee table
cursor.executemany('''
INSERT INTO Employee (employee_name, employee_email, org_name, designation, years_of_experience, salary, location, hire_date)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', employees)

# Commit the changes
connection.commit()

# Query the Employee table to confirm data insertion
cursor.execute("SELECT * FROM Employee where years_of_experience >3; ")
rows = cursor.fetchall()

connection.close()

# Print the records
for row in rows:
    print(row)