# Python Generators

*  Novice  
*  Weight: 1  
*  Project will start Dec 2, 2024 12:00 AM, must end by Dec 9, 2024 12:00 AM  
*  Checker was released at Dec 2, 2024 12:00 AM  
*  **Manual QA review must be done** (request it when you are done with the project)  
*  An auto review will be launched at the deadline

#### **About the Project**

This project introduces advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations. The tasks focus on leveraging Python’s yield keyword to implement generators that provide iterative access to data, promoting optimal resource utilization, and improving performance in data-driven applications.

#### **Learning Objectives**

By completing this project, you will:

1. **Master Python Generators**: Learn to create and utilize generators for iterative data processing, enabling memory-efficient operations.  
2. **Handle Large Datasets**: Implement batch processing and lazy loading to work with extensive datasets without overloading memory.  
3. **Simulate Real-world Scenarios**: Develop solutions to simulate live data updates and apply them to streaming contexts.  
4. **Optimize Performance**: Use generators to calculate aggregate functions like averages on large datasets, minimizing memory consumption.  
5. **Apply SQL Knowledge**: Use SQL queries to fetch data dynamically, integrating Python with databases for robust data management.

#### **Requirements**

1. Proficiency in Python 3.x.  
2. Understanding of yield and Python’s generator functions.  
3. Familiarity with SQL and database operations (MySQL and SQLite).  
4. Basic knowledge of database schema design and data seeding.  
5. Ability to use Git and GitHub for version control and submission.

### Quiz questions

**Great\!** You've completed the quiz successfully\! Keep going\! (Show quiz)

## Tasks

### 0\. Getting started with python generators

**mandatory**

**Objective: create a generator that streams rows from an SQL database one by one.**

**Instructions:**

* Write a python script that seed.py:  
  * Set up the MySQL database, ALX\_prodev with the table user\_data with the following fields:  
  * user\_id(Primary Key, UUID, Indexed)  
  * name (VARCHAR, NOT NULL)  
  * email (VARCHAR, NOT NULL)  
  * age (DECIMAL,NOT NULL)  
  * Populate the database with the sample data from this [user\_data.csv](https://intranet.alxswe.com/rltoken/kPrtJ_hN0TXKgEfwKY4vHg)  
    * Prototypes:  
  * def connect\_db() :- connects to the mysql database server  
  * def create\_database(connection):- creates the database ALX\_prodev if it does not exist  
  * def connect\_to\_prodev() connects the the ALX\_prodev database in MYSQL  
  * def create\_table(connection):- creates a table user\_data if it does not exists with the required fields  
  * def insert\_data(connection, data):- inserts data in the database if it does not exist

faithokoth@ubuntu:python-generators-0x00 % cat 0-main.py  
\#\!/usr/bin/python3

seed \= \_\_import\_\_('seed')

connection \= seed.connect\_db()  
if connection:  
    seed.create\_database(connection)  
    connection.close()  
    print(f"connection successful")

    connection \= seed.connect\_to\_prodev()

    if connection:  
        seed.create\_table(connection)  
        seed.insert\_data(connection, 'user\_data.csv')  
        cursor \= connection.cursor()  
        cursor.execute(f"SELECT SCHEMA\_NAME FROM INFORMATION\_SCHEMA.SCHEMATA WHERE SCHEMA\_NAME \= 'ALX\_prodev';")  
        result \= cursor.fetchone()  
        if result:  
            print(f"Database ALX\_prodev is present ")  
        cursor.execute(f"SELECT \* FROM user\_data LIMIT 5;")  
        rows \= cursor.fetchall()  
        print(rows)  
        cursor.close()

faithokoth@ubuntu:python-generators-0x00 % ./0-main.py  
connection successful  
Table user\_data created successfully  
Database ALX\_prodev is present   
\[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119), ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49), ('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22), ('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly\_Balistreri22@hotmail.com', 102)\]

faithokoth@h@ubuntu:python-generators-0x00 % 

**Repo:**

* GitHub repository: alx-backend-python  
* Directory: python-generators-0x00  
* File: seed.py, README.md

Check submission

### 1\. generator that streams rows from an SQL database

**mandatory**

**Objective:** create a generator that streams rows from an SQL database one by one.

**Instructions:**

* In 0-stream\_users.py write a function that uses a generator to fetch rows one by one from the user\_data table. You must use the Yield python generator  
  * Prototype: def stream\_users()  
  * Your function should have no more than 1 loop

(venv)faithokoth@Faiths-MacBook-Pro python-generators-0x00 % cat 1-main.py 

\#\!/usr/bin/python3  
from itertools import islice  
stream\_users \= \_\_import\_\_('0-stream\_users')

\# iterate over the generator function and print only the first 6 rows

for user in islice(stream\_users(), 6):  
    print(user)

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 %./1-main.py

{'user\_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}  
{'user\_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}  
{'user\_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}  
{'user\_id': '00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'name': 'Ronnie Bechtelar', 'email': 'Sandra19@yahoo.com', 'age': 22}  
{'user\_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly\_Balistreri22@hotmail.com', 'age': 102}  
{'user\_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 %

**Repo:**

* GitHub repository: alx-backend-python  
* Directory: python-generators-0x00  
* File: 0-stream\_users.py

Check submission

### 2\. Batch processing Large Data

**mandatory**

**Objective:** Create a generator to fetch and process data in batches from the users database

**Instructions:**

* Write a function stream\_users\_in\_batches(batch\_size) that fetches rows in batches  
* Write a function batch\_processing() that processes each batch to filter users over the age of25\`  
* You must use no more than 3 loops in your code. Your script must use the yield generator  
  * Prototypes:  
    * def stream\_users\_in\_batches(batch\_size)  
    * def batch\_processing(batch\_size)

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % cat 2-main.py                  
\#\!/usr/bin/python3  
import sys  
processing \= \_\_import\_\_('1-batch\_processing')

\#\#\#\#\# print processed users in a batch of 50  
try:  
    processing.batch\_processing(50)  
except BrokenPipeError:  
    sys.stderr.close()

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % ./2-main.py | head \-n 5 

{'user\_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}

{'user\_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}

{'user\_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}

{'user\_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly\_Balistreri22@hotmail.com', 'age': 102}

{'user\_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % 

**Repo:**

* GitHub repository: alx-backend-python  
* Directory: python-generators-0x00  
* File: 1-batch\_processing.py

Check submission

### 3\. Lazy loading Paginated Data

**mandatory**

**Objective:** Simulte fetching paginated data from the users database using a generator to lazily load each page

**Instructions:**

* Implement a generator function lazy*paginate(page*size) that implements the paginate\_users(page\_size, offset) that will only fetch the next page when needed at an offset of 0.  
  * You must only use one loop  
  * Include the paginate\_users function in your code  
  * You must use the yield generator  
  * Prototype:  
  * def lazy\_paginate(page\_size)

\#\!/usr/bin/python3  
seed \= \_\_import\_\_('seed')

def paginate\_users(page\_size, offset):  
    connection \= seed.connect\_to\_prodev()  
    cursor \= connection.cursor(dictionary=True)  
    cursor.execute(f"SELECT \* FROM user\_data LIMIT {page\_size} OFFSET {offset}")  
    rows \= cursor.fetchall()  
    connection.close()  
    return rows

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % cat 3-main.py  
\#\!/usr/bin/python3  
import sys  
lazy\_paginator \= \_\_import\_\_('2-lazy\_paginate').lazy\_pagination

try:  
    for page in lazy\_paginator(100):  
        for user in page:  
            print(user)

except BrokenPipeError:  
    sys.stderr.close()  
(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00  % python 3-main.py | head \-n 7

{'user\_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}

{'user\_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}

{'user\_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}

{'user\_id': '00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'name': 'Ronnie Bechtelar', 'email': 'Sandra19@yahoo.com', 'age': 22}

{'user\_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly\_Balistreri22@hotmail.com', 'age': 102}

{'user\_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}

{'user\_id': '01ab6c5d-7ae2-4968-991a-d63e93d8d025', 'name': 'Forrest Heaney', 'email': 'Albert51@hotmail.com', 'age': 104}  
(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % 

**Repo:**

* GitHub repository: alx-backend-python  
* Directory: python-generators-0x00  
* File: 2-lazy\_paginate.py

### 4\. Memory-Efficient Aggregation with Generators

**mandatory**

**Objective:** to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset

**Instruction:**

* Implement a generator stream\_user\_ages() that yields user ages one by one.  
* Use the generator in a different function to calculate the average age without loading the entire dataset into memory  
* Your script should print Average age of users: average age  
* You must use no more than two loops in your script  
* You are not allowed to use the SQL AVERAGE

**Repo:**

* GitHub repository: alx-backend-python  
* Directory: python-generators-0x00  
* File: 4-stream\_ages.py

Check submission

### 5\. Manual Review

**mandatory**

**Repo:**

* GitHub repository: alx-backend-python  
* Directory: python-generators-0x00

Ready for a review

[Back](https://intranet.alxswe.com/concepts/108699?project_id=101619)

[Next](https://intranet.alxswe.com/concepts/107381?project_id=101620)
