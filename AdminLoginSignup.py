import datetime
import random
import re
import pymysql

import Students_View
from Teachers_view import Teachers
import Teachers_view



def isDigitInName(name):
    for n in name:
        if n.isdigit():
            return True


def signup():
 # ******************************************
 # First of all we will validate the Email
 #

    email = input("Enter your Email:")
    while(email.find("@") == -1):
        print("Your email must have @ ")
        email = input("Enter your Email:")

    temp = email.split("@")
    speacialCharaCheck = re.compile('[!#$%^&*()<>?/\|}{~:;]')

    while(not(speacialCharaCheck.search(temp[0]) == None)):
        print("Your Email should not have speacial character Before @")
        print("only _ + and . are allowed \n")
        email = input("Enter your Email:")

        while(email.find("@") == -1):
            print("Your email must have @ ")
            email = input("Enter your Email:")

        temp = email.split("@")

    while(not(temp[1] == "yahoo.com" or temp[1] == "gmail.com" or temp[1] == "outlook.com")):
        print("Your Email must have contain\nYahoo.com,gamil.com or outlook.com\n")
        email = input("Enter your Email:")

        while(email.find("@") == -1):
            print("Your email must have @ ")
            email = input("Enter your Email:")

        temp = email.split("@")
        while(not(speacialCharaCheck.search(temp[0]) == None)):
            print("Your Email should not have speacial character Before @")
            print("only _ + and . are allowed \n")
            email = input("Enter your Email:")
            temp = email.split("@")

        # while(not(temp[1] == "yahoo.com" or temp[1] == "gmail.com" or temp[1] == "outlook.com")):
        #     print("Your Email must have contain\nYahoo.com,gamil.com or outlook.com\n")
        #     email = input("Enter your Email:")
        #     temp = email.split("@")

# Email validations Complete here
# After this segment of code we finally have validate Email Adress
# ************************************************

# Here we get password and validate it.
    password = input("Enter your Password: ")
    while(len(password) < 8):
        print("Password length should be atleast 8")
        password = input("Enter your Password: ")

# Here we ask for account Type
    acctype = input("Please Enter the Account Type i.e Teacher or Student:")
    while((acctype != "teacher" and acctype != "Teacher") and (acctype != "Student" and acctype != "student")):
        print("Account Type must be Teacher or Student")
        acctype = input("Please Enter the Account Type: ")

    uName = input("Enter your Name:")

# Here we ask for name and make sure it does not conatin any digits
    while(isDigitInName(uName)):
        print("Name should not contain digits")
        uName = input("Enter your Name:")

# Now we will generate a unique Account ID
    accountID = ''
    try:
        # Connecting to the DataBase

        connection = pymysql.connect(
            host="localhost", user="root", password="arsalHussain#10", database="cms")
        # create cursor
        cur = connection.cursor()
        count = 0
        status = True

#   If User choose Teacher as an account type then we will search from data base
#   that id generated by the random function is already taken or not

        if(acctype == "teacher" or acctype == "Teacher"):
            val = random.randint(1000, 9999)
            query = "SELECT t_id from teachers"
            cur.execute(query)
            rows = cur.fetchall()

            while(status):

                for r in rows:
                    l = str(r[0])
                    idcheck = l.split("_")
                    if ((idcheck[1]) == val):
                        count = count+1

                if(count == 0):
                    status = False
                else:
                    # if the account id is already taken then progarm will generate again
                    val = random.randint(1000, 9999)
                    count = 0
                    status = True

            # At last we concatenate the unique number with Teach keyword that identify that
            # account type is Teacher
            accountID = "Teach_"+str(val)

            phoneNum = input("Enter your Phone Number:")

            # finally we will store it in our DataBase
            cur.execute("""INSERT INTO teachers VALUES ( % s, % s, % s, % s,%s,%s,%s)
            """, (accountID, uName, phoneNum, 0, email, password, 1))
            connection.commit()
            connection.close()
            print('\nYou have SignUp successfully.')
            t=Teachers_view.Teachers(accountID,uName,phoneNum,0,email,password,1)

            print("\n***********************************************")
            print("Your Account ID is   : ", accountID)
            print("Your Name is         : ", uName)
            print("Your Email is        : ", email)
            print("Your Password is     : ", password)
            print("Your Account Type is : ", acctype)
            print("***********************************************\n")
            return t


        # the same procedure goes for the Student Type account

        elif(acctype == "student" or acctype == "Student"):

            val = random.randint(1000, 9999)
            query = "SELECT s_id from students"
            cur.execute(query)
            rows = cur.fetchall()

            while(status):

                for r in rows:
                    l = str(r[0])
                    idCheck = l.split("_")
                    if (int(idCheck[1]) == val):
                        count += 1

                if(count == 0):
                    status = False
                else:
                    val = random.randint(1000, 9999)
                    count = 0
                    status = True

            accountID = "stud_"+str(val)

            cur.execute("""INSERT INTO students
            VALUES ( %s, %s, %s, %s,%s)
            """, (accountID, uName, email, password, 1))
            connection.commit()
            connection.close()
            print('\nYou have SignUp successfully.')
            s=Students_View.Students(accountID,uName,email,password,1)

            print("\n***********************************************")
            print("Your Account ID is   : ", accountID)
            print("Your Name is         : ", uName)
            print("Your Email is        : ", email)
            print("Your Password is     : ", password)
            print("Your Account Type is : ", acctype)
            print("***********************************************\n")

            return s

    except Exception as e:
        print(str(e))



# *****************************************************************************


def login():
    try:
        # Connecting to the DataBase

        connection = pymysql.connect(
            host="localhost", user="root", password="arsalHussain#10", database="cms")

        # create cursor
        cur = connection.cursor()
        loginStatus = False
        count = 1
        accountId = input("Enter your Account Id : ")

        while(accountId.find("_") == -1):
            print("Your Account ID must have _ after account Type and before number ")
            accountId = input("Enter your Account Id :")

        temp = accountId.split("_")

        if(temp[0] == "teach" or temp[0] == "Teach"):

            query = "SELECT t_id,t_password,t_accountStatus from teachers"
            cur.execute(query)
            rows = cur.fetchall()
            for r in rows:
                if(r[0] == accountId and r[2] == 1):
                    password = input("Enter your Password : ")
                    if(r[1] == password):
                        loginStatus = True
                        break
                    else:
                        print("Your Password is Wrong")
                        print(3-count, " Attempts left")
                        password = input("Enter your Password Again : ")

                        count += 1
                        while(password != r[1] and count < 3):
                            print("Your Password is Wrong")
                            print(3-count, " Attempts left")
                            password = input("Enter your Password Again : ")
                            count += 1

                        if(r[1] != password and count >= 3):
                            query = "update teachers set t_accountStatus = 0 where t_id = %s"
                            args = accountId
                            cur.execute(query, args)
                            connection.commit()
                            connection.close()

                            print(
                                "Your Account is Disable due to Entering Incorrect Password")
                            print("Contact to the Administrator to Enable\n")

                        if(r[1] == password):
                            loginStatus = True

                elif(r[0] == accountId and r[2] == 0):
                    print("Your Account is Blocked, Kindly Visit Administrator")
                    break

            if(loginStatus):
                print("Account ID and Password Matched")
                try:
                    con = pymysql.connect(host="localhost", user="root", password="arsalHussain#10", db="cms")
                    cur = con.cursor()
                    query = "select t_name, t_phone, t_noOfClasses, t_email, t_accountStatus " \
                            "from teachers where t_id= %s "
                    args = (accountId)
                    cur.execute(query, args)
                    rows = cur.fetchall()
                    t_name = rows[0][0]
                    t_phone = rows[0][1]
                    t_noOfClasses = rows[0][2]
                    t_email = rows[0][3]
                    t_accountStatus = rows[0][4]
                    print("---WELCOME ",t_name,"---")
                    t = Teachers_view.Teachers(accountId, t_name, t_phone, t_noOfClasses, t_email, password,
                                               t_accountStatus)
                    con.close()
                    return t
                except Exception as e:
                    print(e)
            else:
                print("Account does not exsist")

        elif(temp[0] == "stud" or temp[0] == "Stud"):

            query = "SELECT s_id,s_password,s_accountStatus from students"
            cur.execute(query)
            rows = cur.fetchall()

            for r in rows:

                if(r[0] == accountId and r[2] == '1'):

                    password = input("Enter your Password : ")

                    if(r[1] == password):
                        loginStatus = True
                        break
                    else:
                        print("Your Password is Wrong")
                        print(3-count, " Attempts left")
                        password = input("Enter your Password Again : ")

                        count += 1
                        while(password != r[1] and count < 3):
                            print("Your Password is Wrong")
                            print(3-count, " Attempts left")
                            password = input("Enter your Password Again : ")
                            count += 1

                        if(r[1] != password and count >= 3):
                            query = "update students set s_accountStatus = 0 where s_id = %s"
                            args = accountId
                            cur.execute(query, args)
                            connection.commit()
                            connection.close()

                            print(
                                "Your Account is Disable due to Entering Incorrect Password")
                            print("Contact to the Administrator to Enable\n")

                        if(r[1] == password):
                            loginStatus = True

                elif(r[0] == accountId and r[2] == '0'):
                    print("Your Account is Blocked Kindly visit administrator")
                    break

            if(loginStatus):
                print("Account ID and Password Matched")
                try:
                    con = pymysql.connect(host="localhost", user="root", password="arsalHussain#10", db="cms")
                    cur = con.cursor()
                    query = "select s_name, s_email, s_accountStatus from students where s_id = %s "
                    args = (accountId)
                    cur.execute(query, args)
                    rows = cur.fetchall()
                    s_name = rows[0][0]
                    s_email = rows[0][1]
                    s_accountStatus = rows[0][2]
                    print("---WELCOME" ,s_name,"---")
                    s = Students_View.Students(accountId,s_name,s_email,password,s_accountStatus)
                    con.close()
                    return s
                except Exception as e:
                    print(e)


            else:
                print("Account does not exsist")

        elif(temp[0] == "admin" or temp[0] == "Admin"):
            query = "SELECT a_id,a_password from admin"
            cur.execute(query)
            rows = cur.fetchall()

            for r in rows:
                if(r[0] == accountId):
                    password = input("Enter your Password : ")

                    if(r[1] == password):
                        loginStatus = True
                        break

            if(loginStatus):
                print("Account ID and Password Matched")
                try:
                    con = pymysql.connect(host="localhost", user="root", password="arsalHussain#10", db="cms")
                    cur = con.cursor()
                    query = "select a_name, a_email from admin where a_id = %s "
                    args = (accountId)
                    cur.execute(query, args)
                    rows = cur.fetchall()
                    a_name = rows[0][0]
                    a_email = rows[0][1]
                    print("---WELCOME" ,a_name,"---")
                    a = AdminView(accountId,a_name,a_email,password)
                    con.close()
                    return a
                except Exception as e:
                    print(e)






            else:
                print("Account does not exsist")
        else:
            print("Account does not exsist")

        connection.close()

    except Exception as e:
        print(str(e))


class AdminView:
    def __init__(self,a_id,a_name,a_email,a_password):
        self.a_id=a_id
        self.a_name=a_name
        self.a_email=a_email
        self.a_password=a_password

    def updateUserInfo(self, userId):
        try:
            # Connecting to the DataBase

            connection = pymysql.connect(
                host="localhost", user="root", password="arsalHussain#10", database="cms")
            # create cursor
            cur = connection.cursor()

            des = input(
                "Press 1 if you want to Enable the account\nPress 2 if you want Disable the account")
            temp = str(userId).split("_")

            if(des == '1'):
                if(temp[0] == "teach" or temp[0] == "Teach"):
                    query = "update teachers set t_accountStatus = 1 where t_id = %s"
                    args = userId
                    cur.execute(query, args)
                    print("Account of : ", userId, " is Enable Successfully\n")

                elif(temp[0] == "stud" or temp[0] == "Stud"):
                    query = "update students set s_accountStatus = 1 where s_id = %s"
                    args = userId
                    cur.execute(query, args)
                    print("Account of : ", userId, " is Enable Successfully\n")

            elif(des == '2'):

                if(temp[0] == "teach" or temp[0] == "Teach"):
                    query = "update teachers set t_accountStatus = 0 where t_id = %s"
                    args = userId
                    cur.execute(query, args)
                    print("Account of : ", userId,
                          " is Disable Successfully\n")

                elif(temp[0] == "stud" or temp[0] == "Stud"):
                    query = "update students set s_accountStatus = 0 where s_id = %s"
                    args = userId
                    cur.execute(query, args)
                    print("Account of : ", userId,
                          " is Disable Successfully\n")

            connection.commit()
            connection.close()

        except Exception as e:
            print(str(e))

    def deleteClassroom(self,classroomId):

        try:
            # Connecting to the DataBase

            connection = pymysql.connect(
                host="localhost", user="root", password="arsalHussain#10", database="cms")
            # create cursor
            cur = connection.cursor()
            className=Teachers_view.getCompleteClassName(cur,classroomId)

            query = "select c_name from classroom where c_id=%s"
            args = classroomId
            cur.execute(query, args)
            if (cur.fetchone() != None):

                query = "delete from posts where class_id=%s"
                args = classroomId
                cur.execute(query, args)

                query = "update classroom set c_deletionDate  = %s where c_id = %s"
                x = datetime.date.today()
                args = (x, classroomId)
                cur.execute(query, args)
                query = "DROP TABLE IF EXISTS `'"+className+"'-'"+classroomId+"'`"+";"
                print(query)
                cur.execute(query)

                print("Classroom Deleted Successfully")



                query="select t_id from classroom where c_id = %s"
                args=(classroomId)
                cur.execute(query,args)
                teahcers_id=cur.fetchone()
                print(teahcers_id[0])

                query="select t_noOfClasses from teachers where t_id = %s"
                args=(teahcers_id[0])
                cur.execute(query,args)
                noOfClasses=cur.fetchone()
                classes=noOfClasses[0]-1

                query = "UPDATE `cms`.`teachers` SET `t_noOfClasses` = %s WHERE (`t_id` = %s);"
                args = (classes, teahcers_id)
                cur.execute(query, args)
                connection.commit()

                connection.commit()
                connection.close()
            else:
                print("\nClassroom does not Exist")

        except Exception as e:
            print(str(e))

    def classroomInfo(self, sDate, eDate):
        # sDate = datetime.strptime(sDate, "%Y-%m-%d")
        # print(type(sDate))
        try:
            # Connecting to the DataBase

            connection = pymysql.connect(
                host="localhost", user="root", password="arsalHussain#10", database="cms")

            # create cursor
            cur = connection.cursor()
            query = "select count(c_name) from classroom where c_creationDate between '" + \
                sDate + "' and '"+eDate+"' "
            # print(query)
            cur.execute(query)
            count1 = cur.fetchone()

            print("\nThe count of Classes Created between " +
                  sDate+" and "+eDate+" is : ", count1[0])

            query = "select count(c_name) from classroom where C_deletionDate between '" + \
                sDate+"' and '"+eDate+"' "
            cur.execute(query)
            count2 = cur.fetchone()
            print("\nThe count of Classes Deleted between " +
                  sDate+" and "+eDate+" is : ", count2[0], "\n")

            connection.close()

        except Exception as e:
            print(str(e))

    def searchStudents(self, sName, classId1, classId2):
        try:
            # Connecting to the DataBase
            connection = pymysql.connect(
                host="localhost", user="root", password="arsalHussain#10", database="cms")
            # create cursor
            cur = connection.cursor()
            query = "select c_name,c_deletionDate from classroom where c_id = %s"
            args = (classId1)
            cur.execute(query, args)
            clasName1 = cur.fetchall()
            if not clasName1:
                exit(0)

            ls = clasName1[0]

            query = "select c_name,c_deletionDate from classroom where c_id = %s"
            args = (classId2)
            cur.execute(query, args)
            clasName2 = cur.fetchall()
            ls2 = clasName2[0]
            count = 0

            if ls[1] == "0000-00-00":
                ## query="select enrolledStatus from `%s-%s` where s_id=%s " 'ai'-'rlbzf'

                query = "select * from `'"+ls[0]+"'-'"+classId1+"'`"+" where s_name = %s"
                args = (sName)
                cur.execute(query, args)
                data = cur.fetchall()

                if data != None:
                    print("\n*****************************************************")
                    print("Fatching Data from", ls[0], "Class\n")

                    for d in data:
                        if(d[1] == sName):
                            count += 1
                            print("Student ID:", d[0], "|", "Student Name:",
                                  d[1], "|", "Marks in Course: ", d[2])
                if count == 0:
                    print("Student of Name ", sName,
                          " does not exsist in ", ls[0], " Class")

            else:
                print(ls[0], "Class Does not Exsist.")

            if ls2[1] == "0000-00-00":
                query = "select * from `'"+ls2[0]+"'-'"+classId2+"'`"+" where s_name = %s"
                args = (sName)
                cur.execute(query, args)
                data = cur.fetchall()
                count = 0
                if data != None:

                    print("\n*****************************************************")
                    print("Fatching Data from", ls2[0], "Class\n")

                    for d in data:
                        if(d[1] == sName):
                            count += 1
                            print("Student ID:", d[0], "|", "Student Name:",
                                  d[1], "|", "Marks in Course: ", d[2])
                if count == 0:
                    print("Student of Name ", sName,
                          " does not exsist in ", ls2[0], " Class")

            else:
                print(ls2[0], "Class Does not Exsist.")

            connection.close()

        except Exception as e:
            print(str(e))


