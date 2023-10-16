def sayhello():
    print(
"""
import mysql.connector as myconnector
mycon = myconnector.connect(host="localhost",user="root" , passwd="test", database="test")
mycursor = mycon.cursor()
def create_table():
    query = '''
                CREATE TABLE employee(
                    emp_id int primary key,
                    name varchar(225) not null,
                    pay int, 
                    bonus int
                );
            '''
    mycursor.execute(query)
def insert_values():
    my_inputs = []
    n = int(input("Enter the number of rows you want to insert : "))
    print("the order of columns is emp_id , name , pay , bonus ")
    for i in range(n) : 
        temp = input("Enter values in order seperated by ',' : ")
        temp = temp.split(",")
        for i in range(len(temp)):
            temp[i] = temp[i].strip()
        my_inputs.append(temp)
    query = '''INSERT INTO employee (emp_id , name , pay , bonus) VALUES (%s,%s,%s,%s)'''
    for i in range(len(my_inputs)):
        mycursor.execute(query,my_inputs[i])
        mycon.commit()


def alter():
    query = input("Enter your query to alter your table: ")
    mycursor.execute(query)
    mycon.commit()

def update():
    query = input("Enter your query to update your table: ")
    mycursor.execute(query)
    mycon.commit()

def show_content():
    mycursor.execute("select * from employee")
    result = mycursor.fetchall()
    for i in result:
        print(i)

def describe():
    mycursor.execute('desc employee')
    result = mycursor.fetchall()
    for i in result:
        print(i)

n = ""
print('''Press 1 to create table 
      Press 2 to insert values into table 
      Press 3 to alter table 
      Press 4 to update table
      Press 5 to display table 
      Press 6 to describe table
      Say press 0 to end.

''')
while n != 0:
    n = int(input("Command : "))
    if n == 1 :
        create_table()
    if n == 2 :
        insert_values()
    if n == 3 :
        alter()
    if n == 4 :
        update()
    if n == 5 :
        show_content()
    if n == 6 :
        describe()
""")