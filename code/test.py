import sqlite3

connection = sqlite3.connect('data.db')
cursor= connection.cursor()
create_table="CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)"

cursor.execute(create_table)

user=(1,'sar','asdf')
insert_query ="INSERT INTO users values (?,?,?)"
cursor.execute(insert_query, user)

users=[(2,'bar','asdf'),
       (3,'dar','asdf')]
cursor.executemany(insert_query,users)

select_query="SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()