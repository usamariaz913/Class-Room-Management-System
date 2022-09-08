import datetime

import pymysql
from datetime import date

import random
from Classroom import Classroom
import string




def checkIfStudentExist(con, cur, id): #this function check student from Students table (If exist or not)
    query="select s_id from students where s_id = %s";
    args=(id)
    cur.execute(query,args)
    rows=cur.fetchall()
    if rows:
        return True
    print("Student doest not exist")
    return False

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
def checkIfClassExist(cur,classId): #it will check whether a class exist or not
    deletionDate="0000-00-00"
    query="select * from classroom where c_id = %s and c_deletionDate = %s"  #simply check from classroom table if row of that class exist or not
    args=(classId,deletionDate)
    cur.execute(query,args)
    rows=cur.fetchall()
    if rows:
        print("Yes class exist")
        return True
    print("Class doest not exist")
    return False



class Teachers:
    def __init__(self,t_id,t_name,t_phone,t_noOfClasses,t_email,t_password,t_accountStatus):
        self.t_id=t_id
        self.t_name=t_name
        self.t_phone=t_phone
        self.t_noOfClasses=t_noOfClasses
        self.t_email=t_email
        self.t_password=t_password
        self.t_accountStatus=t_accountStatus
    def createClassrooms(self):
        self.t_noOfClasses=self.getNoOfClasses()
        if self.t_noOfClasses<5:
            id=generateClassId()
            while checkForDuplication(id)==False:
                id = generateClassId()
            c_name=input("Enter class Name")
            c_noOfStudents=0
            today=date.today()
            classroom=Classroom(id,c_name,self.t_id,c_noOfStudents,today,'')
            try:
                con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
                cur = con.cursor()
                query = "insert into classroom (c_id,c_name,t_id,c_noOfStudents,c_creationDate,c_deletionDate) values(%s,%s,%s,%s,%s,%s)"
                args = (id, c_name, self.t_id, c_noOfStudents, date.today(), date.today() - date.today())
                cur.execute(query, args)
                con.commit()
                makeClass(con,cur,c_name,c_noOfStudents,id)

                self.t_noOfClasses=self.getNoOfClasses()+1

                query="UPDATE `cms`.`teachers` SET `t_noOfClasses` = %s WHERE (`t_id` = %s);"
                args=(self.t_noOfClasses,self.t_id)
                cur.execute(query,args)
                con.commit()
                print("class created successfully")
                con.close()
            except Exception as e:
                print(e)
        else:
            print("You have already created 5 classes. Now you cannot create more class")

    def getNoOfClasses(self):
        try:

            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            query = "select t_noOfClasses from teachers where t_id = %s"
            args = (self.t_id)
            cur.execute(query, args)
            row = cur.fetchone()
            return row[0]
        except Exception as e:
            print(e)
    def displayAllClasses(self,cur):
        deletionDate="0000-00-00"
        query="Select c_id, c_name,c_noOfStudents from classroom where t_id=%s and c_deletionDate = %s "
        args=(self.t_id,deletionDate)
        cur.execute(query,args)
        rows=cur.fetchall()
        print("Class id\tClassName(No of Students)")
        for x in rows:
            print(x[0]+"\t\t"+ x[1]+"(",x[2],")")

    def displayAClass(self,cur,className,classId):
        enrolledStatus=1
        query="Select * from `%s-%s` where enrolledStatus= %s"
        args=(className,classId,enrolledStatus)
        cur.execute(query,args)
        rows=cur.fetchall()
        if rows:

            print("Student_id : StudentName : Marks")
            print("------------------------------------------")
            size=len(rows[0])
        for x in rows:
            for i in range(0,size):
                print(x[i],end=" : ")
            print()
    def addStudentToClass(self):

        try:
            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            if self.getNoOfClasses()>0:
                print("Following are the", self.getNoOfClasses(),"classes on which you can add student")
                self.displayAllClasses(cur)
                classId = input("Enter the class id in which you want to add students")
                if (checkIfClassExist(cur, classId)) == True: #first check if class exist or not
                    quantity = int(input("Enter number of students you want to add"))


                    completeClassName = getCompleteClassName(cur,classId)
                    addedStudent=0
                    if self.displayStudentsTable(cur)==True:
                        for i in range(0, quantity):
                            id = input("Enter student id")

                            marks = 0
                            enrolledStatus = 1
                            while checkIfStudentExist(con, cur, id) == False:  #checking if entered student is present in student table
                                print("Student not found.\Enter again")
                                id=input()
                            if checkForEnrolledStatus(cur, completeClassName, classId, id) == 0: #checking if teacher has already removed that student from class in past
                                print("You cannot add this student because you have already removed it")
                            elif checkForEnrolledStatus(cur, completeClassName, classId, id) == 1: #checking if student is already present in class or not
                                print("Student already present in class")
                            else: #if student is present in data base and not enrolled in class, now you can add
                                studentName=self.getStudentName(cur,id)
                                query = " insert into `%s-%s` (`s_id`,`s_name`, `marks`,`enrolledStatus`) values (%s,%s,%s,%s);"
                                args = (completeClassName, classId, id,studentName, marks, enrolledStatus)
                                cur.execute(query, args)
                                con.commit()
                                addedStudent+=1

                        query = "select c_noOfStudents from classroom where c_id=%s"
                        args = (classId)
                        cur.execute(query, args)
                        noOfStudents = cur.fetchone()
                        total=int(noOfStudents[0])
                        total += addedStudent
                        print("Total Students enrolled in this class are",total)
                        query = "UPDATE `cms`.`classroom` SET `c_noOfStudents` = %s WHERE (`c_id` = %s);"
                        args = (total, classId)
                        cur.execute(query, args)
                        con.commit()
                        print("#####Displaying students of ",completeClassName,"-",classId,"######")
                        self.displayAClass(cur,completeClassName,classId)
            else:
                print("Currently you have 0 classes")


            con.close()
        except Exception as e:
            print(e)

    def getStudentName(self,cur,studentId):
        try:
            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            query="select s_name from students where s_id = %s"
            args=(studentId)
            cur.execute(query,args)
            row=cur.fetchone()
            return row
        except Exception as e:
            print(e)

    def removeStudent(self):
        try:
            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            if self.getNoOfClasses()>0:

                print("Following are the", self.getNoOfClasses(),"classes on which you can remove student")
                self.displayAllClasses(cur)
                classId=input("Enter class id from which you want to remove student")
                while(checkIfClassExist(cur,classId))==False:
                    print("Class does not exist.\nEnter again")
                    classId=input()
                completeClassName =getCompleteClassName(cur,classId)
                self.displayAClass(cur,completeClassName,classId)
                if self.getStudentsLength(classId)>0:
                    studentId=input("Enter student id which you want to remove")
                    while(checkIfStudentExist(con,cur,studentId)==False):
                        print("Student not found.\nEnter again")
                        studentId=input()

                    completeClassName =getCompleteClassName(cur,classId)

                    if checkIfStudentExistInClass(cur,studentId,completeClassName,classId)==False:
                        print("Student already not present in class")
                    else:


                        query="UPDATE `cms`.`%s-%s` SET `enrolledStatus` = 0 WHERE (`s_id` = %s);"
                        args=(completeClassName,classId,studentId)
                        cur.execute(query,args)
                        print("Student removed successfully")
                        con.commit()

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
                else:
                    print("Currently 0 students present in class")
            else:
                print("Currently you have 0 classes")
            con.close()




        except Exception as e:
            print(e)

    def getStudentsLength(self,classId):
        try:
            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            query="select c_noOfStudents from classroom where c_id = %s"
            args=(classId)
            cur.execute(query,args)
            rows=cur.fetchone()
            return rows[0]

            con.close()

        except Exception as e:
            print(e)

    def searchStudent(self):


        try:
            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            choice = int(input("Press1 to search from student database.\n2 to search from specific class"))

            if choice == 1:
                studenId = input("Enter student id")
                if checkIfStudentExist(con,cur,studenId):
                    print("Student Found!!!!")
                    print("##Student Table##")
                    print("FORMAT-->Student_id:Student Name:Student Email:Student Password: Student AccountStatus\n")
                    self.display1StudentFromStudentTable(cur, studenId)

                else:
                    print("Student not found")
            elif choice==2:
                if self.getNoOfClasses()>0:
                    print("Following are the classes on which you can search for student")
                    self.displayAllClasses(cur)
                    classId=input("Enter class id")
                    while checkIfClassExist(cur,classId)==False:
                        print("Class not found.\nEnter again")
                        classId=input()
                    studentId=input("Enter student id")
                    completeClassName=getCompleteClassName(cur,classId)
                    if checkIfStudentExistInClass(cur,studentId,completeClassName,classId)==True:
                        query="select s_id,s_name, marks, enrolledStatus from `%s-%s` where s_id=%s"
                        studentName=self.getStudentName(cur,studentId)
                        args=(completeClassName,classId,studentId)
                        cur.execute(query,args)
                        rows=cur.fetchall()
                        print("Student Found")
                        print("\n###CLASS NAME: ",completeClassName,"-",classId,"##")
                        print("Student_id: StudentName :  Marks:enrolledStatus")
                        for x in rows:
                            print(x[0], ":", x[1], ":", x[2]," :" ,x[3])
                    else:
                        print("Student not found")
                else:
                    print("Currently you have 0 Class")
            con.close()
        except Exception as e:
            print(e)

    def displayStudentsTable(self,cur):
        try:
            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            query="select * from students"
            cur.execute(query)
            rows=cur.fetchall()
            if rows:
                print("#####Displaying Students Database/Table#####")

                print("StudentId : StudentName : StudentEmail : StudentPassword : AccountStatus")
                print("------------------------------------------------------------------------")
                size=len(rows[0])
                for x in rows:
                    for i in range(0,size):
                        print(x[i],end=" : ")
                    print("")
                return True
            else:
                print("Sorry , Student database is Empty")
                return False


        except Exception as e:
            print(e)

    def display1StudentFromStudentTable(self, cur, studentId):
        query = "select * from students where s_id=%s "
        args = (studentId)
        cur.execute(query, args)
        rows = cur.fetchall()
        for x in rows:
            print(x[0], ":", x[1], ":", x[2], ":", x[3], ":", x[4])


    def createPost(self):
        try:

            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            if(self.getNoOfClasses()>0):
                print("Following are the",self.getNoOfClasses()," classes on which you can add post")
                self.displayAllClasses(cur)
                classId = input("Enter class id")

                while checkIfClassExist(cur,classId)==False:
                    print("Enter again")
                    classId=input()

                while self.checkIfClassExistforTeacher(cur,classId)==False:
                    print("You have currently no class under this id.\nEnter class id again")
                    classId=input()
                className=getCompleteClassName(cur,classId)
                post=input("Enter post not more than 100 words")
                postLength=len(post.split(' '))
                while postLength>100:
                    post=input("Error! Words more than 100. \nEnter again")
                    postLength=len(post.split(' '))
                query="INSERT INTO `cms`.`posts` (`teacher_id`, `class_id`, `p_msg`,`p_date`) VALUES ( %s, %s, %s,%s);"
                args=(self.t_id,classId,post,date.today())
                cur.execute(query,args)
                con.commit()
                print("Post entered succeffully")
            else:
                print("You have currently 0 classes")

        except Exception as e:
            print(e)

    def checkIfClassExistforTeacher(self,cur,classId): #it will check if teacher has that class or not
        query="Select c_id from classroom where t_id=%s and c_id = %s "
        args=(self.t_id,classId)
        cur.execute(query,args)
        row=cur.fetchone()
        if row:
            return True
        return False

        try:

            con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms")
            cur = con.cursor()
            query = "select t_noOfClasses from teachers where t_id = %s"
            args = (self.t_id)
            cur.execute(query, args)
            row = cur.fetchone()
            return row[0]
        except Exception as e:
            print(e)


def getCompleteClassName(cur,classId): #it will return className like ai
    query = "select c_name from classroom where c_id=%s;"
    args = (classId)
    cur.execute(query, args)
    className = cur.fetchone()
    completeClassName = ''.join(className)
    return  completeClassName

def makeClass(con,cur,className,noOfStudents,classId): #it will make Class Table

    query="CREATE TABLE `cms`.`%s-%s` (`s_id` VARCHAR(9) NOT NULL,`s_name` VARCHAR(45),`marks` INT NULL,`enrolledStatus` INT NULL,PRIMARY KEY (`s_id`), FOREIGN KEY (`s_id`)REFERENCES `cms`.`students` (`s_id`)ON DELETE CASCADE ON UPDATE CASCADE);"

    args=(className,classId)

    cur.execute(query, args)
    con.commit()







def generateClassId():  #generates class id having 5 even letters
    id = 'bdfhjlnprtvxz'

    strs = ''

    for x in range(0, 5):
        strs += random.choice(id)
    print(strs," is the class id Generated randomly")
    return strs;

def checkForDuplication(id): #it will make sure that no class id is generated twice
    try:
        con = pymysql.connect(host="localhost", user="root", password="usamariaz", db="cms",
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        args=(id)
        query="Select t_id from teachers where t_id= %s"
        cur.execute(query,id)
        rows=cur.fetchall()
        print(rows)
        if rows:
            con.close()
            return False
        con.close()
        return True


    except Exception as e:
        print(e)


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


