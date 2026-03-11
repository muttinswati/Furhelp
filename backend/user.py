import db_connection

def get_users():
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM users")
    rows = mycursor.fetchall()
    print("Query successful!!!!")
    for row in rows:
        print(row)
    conn.close()


def add_user(fname, lname, email, password, phnor,city):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql = "INSERT INTO users(fname, lname, email, password, pnor,city) VALUES (%s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, (fname, lname, email, password, phnor, city))
    conn.commit()
    print('User inserted successfully!!')
    conn.close()


def check_stat(email,password):
    conn=db_connection.get_db_connection()
    mycursor=conn.cursor()
    sql='select email,password,uid from users where email=%s and password=%s'
    mycursor.execute(sql,(email,password))
    r=mycursor.fetchone()
    print("Checking login:", email, password)
    print("DB result:", r)
    conn.close()
    return r



def add_doc(fname, lname, email, pnor, password, city, address):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    
    sql = """
        INSERT INTO docters(fname, lname, email, pnor, password,  city, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    mycursor.execute(sql, (fname, lname, email, pnor, password,  city, address))
    conn.commit()
    print('Doctor inserted successfully!!')
    conn.close()


def get_doc():
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT fname,lname,city,address FROM docters")
    rows = mycursor.fetchall()
    print("Query successful!!!!")
    for x in rows:
        print(x)
    conn.close()
    return rows
    
def doc_check_stat(email,password):
    conn=db_connection.get_db_connection()
    mycursor=conn.cursor()
    sql='select email,password,did from docters where email=%s and password=%s'
    mycursor.execute(sql,(email,password))
    r=mycursor.fetchone()
    print("Checking login:", email, password)
    print("DB result:", r)
    conn.close()
    return r

def addmul(dl):
    conn=db_connection.get_db_connection()
    mycursor=conn.cursor()
    sql= """
        INSERT INTO docters (fname, lname, email, pnor, password, city, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    mycursor.executemany(sql,dl)
    conn.commit()
    print('inserted!!!')
    conn.close()


# check_stat('zepto19@gmail.com','z1234')

if __name__ == '__main__':
    pass
# # List of dummy users: (name, gender, email, phone, password, city, area)
#     dummy_users = [
#     # Bangalore
#     ('Ananya','F','ananya1@gmail.com','9000010001','pass1','Bangalore','Whitefield'),
#     ('Arjun','M','arjun2@gmail.com','9000010002','pass2','Bangalore','Koramangala'),
#     ('Riya','F','riya3@gmail.com','9000010003','pass3','Bangalore','HSR Layout'),
#     ('Karthik','M','karthik4@gmail.com','9000010004','pass4','Bangalore','Indiranagar'),
#     ('Meera','F','meera5@gmail.com','9000010005','pass5','Bangalore','Malleshwaram'),
#     ('Varun','M','varun6@gmail.com','9000010006','pass6','Bangalore','Whitefield'),
#     ('Sneha','F','sneha7@gmail.com','9000010007','pass7','Bangalore','Jayanagar'),
#     ('Aditya','M','aditya8@gmail.com','9000010008','pass8','Bangalore','Basavanagudi'),
#     ('Nisha','F','nisha9@gmail.com','9000010009','pass9','Bangalore','HSR Layout'),
#     ('Ravi','M','ravi10@gmail.com','9000010010','pass10','Bangalore','Koramangala'),

#     # Hubli
#     ('Ankit','M','ankit1@gmail.com','9000020001','pass1','Hubli','Vidyanagar'),
#     ('Priya','F','priya2@gmail.com','9000020002','pass2','Hubli','Gokul'),
#     ('Rahul','M','rahul3@gmail.com','9000020003','pass3','Hubli','Anandnagar'),
#     ('Divya','F','divya4@gmail.com','9000020004','pass4','Hubli','Vidyanagar'),
#     ('Sandeep','M','sandeep5@gmail.com','9000020005','pass5','Hubli','Gokul'),
#     ('Nandini','F','nandini6@gmail.com','9000020006','pass6','Hubli','Anandnagar'),
#     ('Kiran','M','kiran7@gmail.com','9000020007','pass7','Hubli','Vidyanagar'),
#     ('Shreya','F','shreya8@gmail.com','9000020008','pass8','Hubli','Gokul'),
#     ('Mohit','M','mohit9@gmail.com','9000020009','pass9','Hubli','Anandnagar'),
#     ('Aishwarya','F','aishwarya10@gmail.com','9000020010','pass10','Hubli','Vidyanagar'),

#     # Belgaum
#     ('Rohan','M','rohan1@gmail.com','9000030001','pass1','Belgaum','Tilakwadi'),
#     ('Sneha','F','sneha2@gmail.com','9000030002','pass2','Belgaum','Camp'),
#     ('Aman','M','aman3@gmail.com','9000030003','pass3','Belgaum','ShivajiNagar'),
#     ('Priya','F','priya4@gmail.com','9000030004','pass4','Belgaum','Tilakwadi'),
#     ('Arjun','M','arjun5@gmail.com','9000030005','pass5','Belgaum','Camp'),
#     ('Nisha','F','nisha6@gmail.com','9000030006','pass6','Belgaum','ShivajiNagar'),
#     ('Karthik','M','karthik7@gmail.com','9000030007','pass7','Belgaum','Tilakwadi'),
#     ('Meera','F','meera8@gmail.com','9000030008','pass8','Belgaum','Camp'),
#     ('Varun','M','varun9@gmail.com','9000030009','pass9','Belgaum','ShivajiNagar'),
#     ('Shreya','F','shreya10@gmail.com','9000030010','pass10','Belgaum','Tilakwadi'),
# ]
#     addmul(dummy_users)
