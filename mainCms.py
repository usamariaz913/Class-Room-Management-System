#Muhammad Arsal Bcsf19a014
#Usama Riaz Bcsf19a016
import AdminLoginSignup
import Students_View
import Teachers_view
from Teachers_view import Teachers
from Students_View import Students
from Classroom import Classroom
from AdminLoginSignup import AdminView
import pymysql

def validateDate(date):
    i=0
    myLen=len(date)
    while(i<myLen):
        if((date[i]>='a' and date[i]<='z') or (date[i]>='A' and date[i]<='Z')):
            print("Please write date in correct format. yyyy-mm-dd")
            return False
        i+=1
    return True

print("-----WELCOME TO CLASSROOM MANAGEMENT SYSTEM------")
choice= input("Press 1 for Signup. 2 for login")
while choice !='1' and choice !='2':
    choice=input("Invalid Input. Enter again")
if choice=="1":
    person=AdminLoginSignup.signup()

    if type(person)==Students_View.Students:
        print(person.s_id)
        again='n'
        while again=='n' or again=='N':
            studentsChoice=input("Press 1 to join class. 2 to leave Class. 3 to view Teachers post")
            while studentsChoice!="1" and studentsChoice!="2" and studentsChoice!="3":
                studentsChoice=input("Invalid Input. Enter Again")
            if studentsChoice=="1":
                person.joinClass()
            elif studentsChoice=="2":
                person.leaveClass()
            else:
                person.viewTeachersPost()
            again=input("Would you like to quit? (y/n)")

    else:
        teacher=person
        again='n'
        while again=='n' or again=='N':
            teachersChoice=input("Press 1 to Create Classroom.\n2 to add Student to Class.\n"
                                     "3 to remove Student from class.\n4 to Search Students."
                                     "\n5 to Create Post")
            while teachersChoice!="1" and teachersChoice!="2" and teachersChoice!="3" and teachersChoice!="4" and teachersChoice!="5":
                teachersChoice=input("Invalid Input. Enter Again")
            if teachersChoice=="1":
                teacher.createClassrooms()
            elif teachersChoice=="2":
                teacher.addStudentToClass()
            elif teachersChoice=="3":
                teacher.removeStudent()
            elif teachersChoice=="4":
                teacher.searchStudent()
            else:
                teacher.createPost()
            again=input("Would you like to quit? (y/n)")


else:
    person = AdminLoginSignup.login()

    if type(person) == Students_View.Students:
        print(person.s_id)
        again = 'n'
        while again == 'n' or again == 'N':
            studentsChoice = input("Press 1 to join class. 2 to leave Class. 3 to view Teachers post")
            while studentsChoice != "1" and studentsChoice != "2" and studentsChoice != "3":
                studentsChoice = input("Invalid Input. Enter Again")
            if studentsChoice == "1":
                person.joinClass()
            elif studentsChoice == "2":
                person.leaveClass()
            else:
                person.viewTeachersPost()
            again = input("Would you like to quit? (y/n)")

    elif type(person) == Teachers_view.Teachers:
        teacher = person
        again = 'n'
        while again == 'n' or again == 'N':
            teachersChoice = input("Press 1 to Create Classroom.\n2 to add Student to Class.\n"
                                       "3 to remove Student from class.\n4 to Search Students."
                                       "\n5 to Create Post")
            while teachersChoice != "1" and teachersChoice != "2" and teachersChoice != "3" and teachersChoice != "4" and teachersChoice != "5":
                teachersChoice =input("Invalid Input. Enter Again")
            if teachersChoice == "1":
                teacher.createClassrooms()
            elif teachersChoice == "2":
                teacher.addStudentToClass()
            elif teachersChoice == "3":
                teacher.removeStudent()
            elif teachersChoice == "4":
                teacher.searchStudent()
            else:
                teacher.createPost()
            again = input("Would you like to quit? (y/n)")
    elif type(person)==AdminLoginSignup.AdminView:
        again = 'n'
        while again == 'n' or again == 'N':
            person=AdminView
            adminChoice=input("Press 1 to delete classroom.\n2 to update user information.\n3 to view "
                                  "Classroom information.\n4 to Search Student")
            while(adminChoice!="1" and adminChoice!="2" and adminChoice!="3" and adminChoice!="4"):
                adminChoice=input("Wrong input.\n Enter Again")

            if adminChoice=="1":
                classId=input("Enter class id which you want to delete")

                person.deleteClassroom(person,classId)
            elif adminChoice=="2":
                userId=input("Enter user id which you want to update")
                person.updateUserInfo(person,userId)
            elif adminChoice=="3":
                date1=input("Enter starting date in yyyy-mm-dd format")
                while validateDate(date1) == False:
                    date1=input()
                date2=input("Enter ending date in yyyy-mm-dd format")
                while validateDate(date2) == False:
                    date2=input()
                while date1> date2:
                    print("Starting date must be smaller than ending date.\nEnter again")
                    date1 = input("Enter starting date in yyyy-mm-dd format")
                    while validateDate(date1) == False:
                        date1 = input()
                    date2 = input("Enter ending date in yyyy-mm-dd format")
                    while validateDate(date2) == False:
                        date2 = input()


                person.classroomInfo(person,date1,date2)
            else:
                try:
                    con = pymysql.connect(host="localhost", user="root", password="arsalHussain#10", db="cms")
                    cur = con.cursor()
                    studentName=input("Enter student name ")
                    id1=input("Enter  first class id")
                    while Teachers_view.checkIfClassExist(cur,id1)==False:
                        id1=input("Class doest no exist. Enter again")
                    id2=input("Enter 2nd class id")
                    while Teachers_view.checkIfClassExist(cur,id2)==False:
                        id2=input("Class doest no exist. Enter again")
                    con.close()
                    person.searchStudents(person,studentName,id1,id2)
                except Exception as e:
                    print(e)
            again = input("Would you like to quit? (y/n)")



