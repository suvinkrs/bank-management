from initialization import check

import pickle
import mysql.connector
import maskpass
from mysql.connector import errorcode
existing=0

conn=None
cursor=None

TABLES = {}
TABLES['employees'] = (
    "CREATE TABLE `employees` ("
    "  `emp_no` int(5) NOT NULL ,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(15) NOT NULL,"
    "  `last_name` varchar(15) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ")

TABLES['clients'] = (
    "CREATE TABLE `clients` ("
    "  `acc_no` int NOT NULL PRIMARY KEY,"
    "  `type` enum('S','C') NOT NULL,"
    "  `first_name` varchar(15) NOT NULL,"
    "  `last_name` varchar(15) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `birth_date` date NOT NULL,"
    "  `accd` date NOT NULL,"
    "  `mobile_no` varchar(20) NOT NULL,"
    "  `email_id` varchar(25) NOT NULL,"
    "  `pass` varchar(512) NOT NULL,"
    "  `aadhar` int(8) NOT NULL"
    ") "
)

TABLES['empass'] = (
    "CREATE TABLE `empass` ("
    "  `emp_no` int(5) NOT NULL,"
    "  `pass` varchar(512) NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") "
)


TABLES['savings'] = (
    "CREATE TABLE `savings` ("
    "  `acc_no` int(5) NOT NULL,"
    "  `balance` int NOT NULL,"
    "  `loan` enum('YES','NO') NOT NULL,"
    "  PRIMARY KEY (`acc_no`)"
    ") "
)

TABLES['current'] = (
    "CREATE TABLE `current` ("
    "  `acc_no` int(5) NOT NULL,"
    "  `balance` int NOT NULL,"
    "  `overdraft` enum('YES','NO') NOT NULL,"
    "  PRIMARY KEY (`acc_no`)"
    ") "
)

TABLES['loan'] = (
    "CREATE TABLE `loan` ("
    "  `acc_no` int(5) NOT NULL,"
    "  `loan_type` enum('PL','HL','EL','TL','BL') NOT NULL,"
    "  `loan_amt` int NOT NULL,"
    "  `time_period_months` int NOT NULL,"
    "  `iterest_perc_per_annum` int(1) NOT NULL,"
    "  `amt-per-month` int NOT NULL,"
    "  `remaining_amt` int NOT NULL,"
    "  PRIMARY KEY (`acc_no`)"
    ") "
)

TABLES['overdraft']=(
    "CREATE TABLE `overdraft` ("
    "  `acc_no` int(5) NOT NULL,"
    "  `overdraft_amt` int NOT NULL,"
    "  `od_with_interest_remaining` int NOT NULL,"
    "  PRIMARY KEY (`acc_no`)"
    ") "
)

TABLES['cash_in_hand']=(
    "CREATE TABLE `cash_in_hand` ("
    "  `acc_no` int(5) NOT NULL,"
    "  `cash_in_hand` int NOT NULL,"
    "  PRIMARY KEY (`acc_no`)"
    ") "
)

TABLES['aadhar_verify']=(
    "CREATE TABLE `aadhar_verify` ("
    "  `aadhar` int(8) NOT NULL,"
    "  `first_name` varchar(15) NOT NULL,"
    "  PRIMARY KEY (`aadhar`)"
    ") "
)

#enter aadhar details directly from sql workbench
#use the following code
# use "database name";
# insert into aadhar_verify(aadhar, first_name) values(43211196, "ram");
# insert into aadhar_verify(aadhar, first_name) values(84843964, "shyam");
# insert into aadhar_verify(aadhar, first_name) values(21218931, "pushpa");


############################################################################################
query=""
Password=""
Database=""
def sqlpwd():
    global Password
    cred = open("files//cred.dat","rb")
    dat=pickle.load(cred)
    cred.close()
    Password=dat[0]
    return Password

def sqldb():
    global Database
    cred = open("files//cred.dat","rb")
    dat=pickle.load(cred)
    cred.close()
    Database=dat[1]
    return Database

def connectionquery():
    try:
        Databa=sqldb()
        Passwo=sqlpwd()
        query=mysql.connector.connect(host="localhost",user="root",password=Passwo,database=Databa)
    except:
        import traceback
        traceback.print_exc()
        query=""
    return query

def querycheck():
    global conn
    global cursor
    global existing
    conn=connectionquery()
    ans=False
    if conn!="":
        if conn.is_connected:
            print("Connection established successfully.")
            if check.check()==True:
                cursor=conn.cursor()
                #Table creation
                for table_name in TABLES:
                    table_description = TABLES[table_name]
                    try:
                        print("Creating table {}: ".format(table_name), end='')
                        cursor.execute(table_description)
                        existing+=1
                    except mysql.connector.Error as err:
                        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                            print("already exists.")
                            existing+=1
                        else:
                            print(err.msg)
                    else:
                        print("OK")
            if existing==9:
                with open("files//firsttime.txt","w") as f:
                    f.write("False")
                ans=True
        
    if not ans:
        print("There was a problem in connection")
        print("Maybe this is because you entered wrong credentials(password and database name)")
    return ans

def mysqlsetup():
    print("\n-----------------MYSQL Setup-------------------\n")
    print("Remember that you can't change the database afterwards\n")
    print("Create a database in your MYSQL Workbench.\n")
    Database=input("Enter database name: ")
    Password=maskpass.askpass(prompt="Enter sql password (enter '' if nothing):",mask='*')
    cred2= open("files//cred.dat","wb")
    data=[Password,Database]
    pickle.dump(data,cred2)
    cred2.close()
    querycheck()

def setup():
    global cursor
    global conn
    global existing
    while check.check():
        print("\n\n-----------------Welcome to the Project!!!-------------------")
        print("This is the setup process which runs when the user uses the program for the first time.")
        print("\n----------------------Database Setup------------------------\n")
        print("1.Mysql 8.0 (Dependency MYSQL)")
        print("2.Standalone (Data files)")
        print("0.Cancel operation\n")
        ans2=input("How do you want to store the data? (1/2): ")
        if ans2 == "0":
            break
        elif ans2=="1":
            mysqlsetup()
            if existing==7:
                continue
        elif ans2=="2":
            print("\nThis is under development :). Please use mysql till then...")
        else:
            print("\nWrong input, (1/2).........")
    else: 
        if querycheck():
            return True