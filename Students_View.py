
import pymysql

import Teachers_view
from Teachers_view import Teachers

class Students:
    def __init__(self,s_id,s_name,s_email,s_password,s_AccountStatus):
        self.s_id=s_id
        self.s_name=s_name
        self.s_email=s_email
        self.s_password=s_password
        self.s_AccountStatus=s_AccountStatus

    def joinClass(self):

        try:
            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            if self.displayClassroom(cur)==True:
                classId = input("Enter the class id in which you want to join")
                while (checkIfClassExist(cur, classId)) == False:  # first check if class exist or not
                    print("Class not found.\nEnter class id again")
                    classId=input()

                completeClassName = getCompleteClassName(cur, classId)

                marks = 0
                enrolledStatus = 1

                if checkForEnrolledStatus(cur,completeClassName,classId,self.s_id) == 0:
                    print("Sorry You cannot be added into this class as your teacher has removed you")
                elif checkForEnrolledStatus(cur, completeClassName, classId,
                                            self.s_id) == 1:  # checking if student is already present in class or not
                    print("you are already added in this class")
                else:  # if student is present in data base and not enrolled in class, now you can add
                    print("now iserting values")
                    query = " insert into `%s-%s` (`s_id`,`s_name`,`marks`,`enrolledStatus`) values (%s,%s,%s,%s);"
                    args = (completeClassName, classId, self.s_id, self.s_name,marks, enrolledStatus)
                    cur.execute(query, args)
                    con.commit()

                    query = "select c_noOfStudents from classroom where c_id=%s"
                    args = (classId)
                    cur.execute(query, args)
                    noOfStudents = cur.fetchone()
                    print(noOfStudents[0])
                    total = int(noOfStudents[0])
                    print(total)
                    total += 1
                    print("total", total)
                    query = "UPDATE `cms`.`classroom` SET `c_noOfStudents` = %s WHERE (`c_id` = %s);"
                    args = (total, classId)
                    cur.execute(query, args)
                    con.commit()

                con.close()
        except Exception as e:
            print(e)
    def leaveClass(self):
        try:
            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()


            if self.displayClassroom(cur)==True:
                classId = input("Enter class id from which you want to leave")

                while(checkIfClassExist(cur,classId))==False:
                    print("Class does not exist.\nEnter again")
                    classId=input()

                completeClassName =getCompleteClassName(cur,classId)

                if checkIfStudentExistInClass(cur,self.s_id,completeClassName,classId)==False:
                    print("You are already not present in class")
                else:


                    query="DELETE FROM `cms`.`%s-%s` WHERE s_id =%s;"
                    args=(completeClassName,classId,self.s_id)
                    cur.execute(query,args)
                    con.commit()
                    print("Class left successfully")

                    query="select c_noOfStudents from classroom where c_id=%s"
                    args=(classId)
                    cur.execute(query,args)
                    row=cur.fetchone()
                    noOfStudents=row[0]-1
                    print(noOfStudents)
                    query="UPDATE `cms`.`classroom` SET `c_noOfStudents` = %s WHERE (`c_id` = %s);"
                    args=(noOfStudents,classId)
                    cur.execute(query,args)
                    print("No of students in a classroom updated")
                    con.commit()

            con.close()

        except Exception as e:
            print(e)

    def viewTeachersPost(self):
        try:
            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            query="select * from posts"
            cur.execute(query)
            rows=cur.fetchall()
            if rows:
                self.displayClassroom(cur)
                classId=input("Enter class id of which you want to see post")
                while checkIfClassExist(cur,classId)==False:
                    print("Class not exist.\Enter class again")
                    classId=input()

                completeClassName=getCompleteClassName(cur,classId)
                if checkIfStudentExistInClass(cur,self.s_id,completeClassName,classId)==False:
                    print("Sorry you cannot view post because you are not enrolled in this class")
                else:

                    query="select p_msg, p_date from posts where class_id =%s"
                    args=(classId)
                    cur.execute(query,args)
                    rows=cur.fetchall()
                    if rows:
                        i=1;
                        print()
                        for x in rows:
                            print("Post#",i,"\t",x[0],"\t",x[1])
                            i+=1
                    else:
                        print("Currently 0 post ")

                con.commit()
            else:
                print("No posts available")
            con.close()

        except Exception as e:
            print(e)

    def displayClassroom(self,cur):
        try:
            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()

            deletionDate="0000-00-00"
            query="Select * from classroom where c_deletionDate = %s"
            args=(deletionDate)
            cur.execute(query,args)
            rows=cur.fetchall()
            if(rows):
                print("Following is the list of all classes")
                print("class_id : class_name : teacher_id : NoOfStudents : Creation date : Deletion Date")
                print("------------------------------------------------------------------------------------")
                size=len(rows[0])
                for x in rows:
                    for i in range(0,size):
                        print(x[i],end=' : ')
                    print()
                return True
            else:
                print("Sorry currently no class is available ")
                return False


        except Exception as e:
            print(e)

def getCompleteClassName(cur, classId):  # it will return className like ai
    query = "select c_name from classroom where c_id=%s;"
    args = (classId)
    cur.execute(query, args)
    className = cur.fetchone()
    completeClassName = ''.join(className)
    return completeClassName

def checkIfClassExist(cur,classId): #it will check whether a class exist or not
    deletionDate="0000-00-00"
    query="select * from classroom where c_id = %s and c_deletionDate= %s"  #simply check from classroom table if row of that class exist or not
    args=(classId,deletionDate)
    cur.execute(query,args)
    rows=cur.fetchall()
    if rows:
        print("Yes class exist")
        return True
    print("Class doest not exist")
    return False


def checkForEnrolledStatus(cur,completeClassName,classId,id): #it will return the enrolled status os student from a specific class
    query="select enrolledStatus from `%s-%s` where s_id = %s "
    args=(completeClassName,classId,id)
    cur.execute(query,args)
    row=cur.fetchone()
    if row:
        if row[0] == 1:
            return 1
        elif row[0] == 0:
            return 0
    return 2

def checkIfStudentExistInClass(cur,studentId,completeClassName,classId): # it will check student from a specific class

    query="select enrolledStatus from `%s-%s` where s_id=%s "
    args=(completeClassName,classId,studentId)
    cur.execute(query,args)
    rows=cur.fetchone()
    if rows:
        if rows[0]==1:
            return True
        return False
    return False

