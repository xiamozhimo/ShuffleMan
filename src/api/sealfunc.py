'''
Created on Sep 25, 2019

@author: tfu
'''
from orm.orm import Student,Course
from conn.conn import createSession
import random

def resetMap():
    session=createSession()
    students = session.query(Student).all()
    courses = session.query(Course).all()
    for student in students:
        student.enrichresult=''
        student.ismapped='0'
    for course in courses:
        course.currentenroll=0
    session.commit()
    session.close()

def rerand():
    session=createSession()
    students = session.query(Student).all()
    for student in students:
        student.rand=random.random()
    session.commit()
    session.close()

def startMap():
    sessionMain=createSession()
    courses = sessionMain.query(Course).all()
    coursesnames=[x.coursekey for x in courses]
    students = sessionMain.query(Student).filter(Student.studentchoice != None).order_by(Student.weight.desc()).order_by(Student.rand.desc()).all()
    
    for student in students:
        if student.ismapped == '0':
            sessionSub=createSession()
            course_temp=student.studentchoice[0].courseselection[:-1].split(';')
            studentbanlist=[x.coursekey for x in student.studentslog]
            selectlist=[]
            for c in course_temp:
                if c in coursesnames and c not in studentbanlist:
                    selectlist.append(c)
            for course in selectlist:
                studentnewstatus=sessionSub.query(Student).filter(Student.student_number == student.student_number).one()
                coursestatus=sessionSub.query(Course).filter(Course.coursekey == course).one()
                if coursestatus.currentenroll <coursestatus.maxenroll and studentnewstatus.ismapped=='0':
                    coursestatus.currentenroll=coursestatus.currentenroll+1
                    studentnewstatus.enrichresult=course
                    studentnewstatus.ismapped='1'
                    sessionSub.commit()
                    print('Mapping:',studentnewstatus.firstname,studentnewstatus.lastname,'successfully!','Grade:',studentnewstatus.gradelevel,'weight:',studentnewstatus.weight,'First Choice is',course_temp[0],'Map to',course)
            sessionSub.close()   
    sessionMain.close()   
    print('this shuffle is done!')     

