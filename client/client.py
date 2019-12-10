#!/usr/bin/env python
# -*- coding: cp1252 -*-

import requests
import json
url='http://127.0.0.1:5000/'
on=True

def print_nice(r):
    res=r.json()
    print "HTTP "+str(r.status_code)+"\n"
    head=r.headers
    for x in head.keys():
        print x+": "+head[x]
    print "\n"  
    if res.has_key("message"):
        print res["message"]
    elif res.has_key("tableAA"):
        res=res["tableAA"]
        if res=={}:
            print 'No result found'
        for x in res.keys():
            print "ID student: "+x
            print "Name: "+res[x][0]
            print "Nationality: "+res[x][1]
            print "Age: "+str(res[x][2])
            print "\n"
    elif res.has_key("tableAD"):
        res=res["tableAD"]
        if res=={}:
            print 'No result found'
        for x in res.keys():
            print "ID course: "+x
            print "Description: "+res[x][0]
            print "Semester: "+str(res[x][1])
            print "Year: "+str(res[x][2])
            print "\n"
    elif res.has_key("tableAT"):
        res=res["tableAT"]
        if res=={}:
            print 'No result found'
        for x in res.keys():
            print "ID Class: "+x
            print "ID course : "+str(res[x][0])
            print "type: "+res[x][1]
            print "description: "+res[x][2]
            print "\n"    
        

while on:
    cmdinput=raw_input("> ")
    cmdinput =cmdinput.split(" ")
    if cmdinput[0]=="EXIT":
        on = False
    elif cmdinput[0]=="":
        pass
    
    elif cmdinput[0]=="ADD":
        try:
            if len(cmdinput)==5:
                if cmdinput[1]=="STUDENT":
                    msg=json.dumps({'nationality':cmdinput[2],'age':cmdinput[3],'name':cmdinput[4]})
                    r = requests.put(url+'students',data=msg)
                    print_nice(r)
                elif cmdinput[1]=="COURSE":
                    msg=json.dumps({'year':cmdinput[2],'semester':cmdinput[3],'description':cmdinput[4]})
                    r = requests.put(url+'courses',data=msg)
                    print_nice(r)
                elif cmdinput[1]=="CLASS":
                    msg=json.dumps({'id_course':cmdinput[2],'type':cmdinput[3],'description':cmdinput[4]})
                    r = requests.put(url+'classes',data=msg)
                    print_nice(r)
            elif (len(cmdinput)==3):
                msg=json.dumps({'id_student':cmdinput[1],'id_class':cmdinput[2]})
                r = requests.post(url+'classes',data=msg)
                print_nice(r)
            else:
                print "Invalid input"
        except:
            print "Unexpected Error"
    elif cmdinput[0]=="REMOVE":
        try:
            if cmdinput[1]=="STUDENT":
                msg=json.dumps({'id_student':cmdinput[2]})
                r = requests.delete(url+'students',data=msg)
                print_nice(r)
            elif cmdinput[1]=="COURSE":
                msg=json.dumps({'id_course':cmdinput[2]})
                r = requests.delete(url+'courses',data=msg)
                print_nice(r)
            elif cmdinput[1]=="CLASS":
                msg=json.dumps({'id_class':cmdinput[2]})
                r = requests.delete(url+'classes',data=msg)
                print_nice(r)   
            elif cmdinput[1]=="ALL":
                if len(cmdinput)==3:
                    if cmdinput[2]=='STUDENTS':
                        r = requests.delete(url+'students')
                        print_nice(r)
                    elif cmdinput[2]=="COURSES":
                        r = requests.delete(url+'courses')
                        print_nice(r)
                    elif cmdinput[2]=="CLASSES":
                        r = requests.delete(url+'classes')
                        print_nice(r)
                elif cmdinput[2]=='STUDENTS':
                    if cmdinput[3]=="CLASS":
                            msg=json.dumps({'students_turma':cmdinput[4]})
                            r = requests.delete(url+'students',data=msg)
                            print_nice(r)
                    elif cmdinput[3]=="COURSES":
                            msg=json.dumps({'students_course':cmdinput[4]})
                            r = requests.delete(url+'alunos',data=msg)
                            print_nice(r)
                elif cmdinput[2]=='CLASSES':
                    msg=json.dumps({'class_course':cmdinput[3]})
                    r = requests.delete(url+'classes',data=msg)
                    print_nice(r)
            elif (len(cmdinput)==3):
                msg=json.dumps({'id_student':cmdinput[1],'id_class':cmdinput[2]})
                r = requests.delete(url+'classes',data=msg)
                print_nice(r)
            else:
                print 'Invalid input'
        except:
            print "Unexpected Error"        
    elif cmdinput[0]=="SHOW":
        try:
            if cmdinput[1]=="STUDENT":
                msg=json.dumps({'id_student':cmdinput[2]})
                r = requests.get(url+'students',data=msg)
                print_nice(r)
            elif cmdinput[1]=="COURSE":
                msg=json.dumps({'id_course':cmdinput[2]})
                r = requests.get(url+'courses',data=msg)
                print_nice(r)
            elif cmdinput[1]=="CLASS":
                msg=json.dumps({'id_class':cmdinput[2]})
                r = requests.get(url+'classes',data=msg)
                print_nice(r)
            elif cmdinput[1]=="ALL":
                if len(cmdinput)==3:
                    if cmdinput[2]=='STUDENTS':
                        r = requests.get(url+'students')
                        print_nice(r)
                    elif cmdinput[2]=="COURSES":
                        r = requests.get(url+'courses')
                        print_nice(r)
                    elif cmdinput[2]=="CLASSES":
                        r = requests.get(url+'classes')
                        print_nice(r)
                elif cmdinput[2]=='STUDENTS':
                    if cmdinput[3]=="CLASS":
                            msg=json.dumps({'students_class':cmdinput[4]})
                            r = requests.get(url+'students',data=msg)
                            print_nice(r)
                    elif cmdinput[3]=="COURSE":
                            msg=json.dumps({'students_course':cmdinput[4]})
                            r = requests.get(url+'students',data=msg)
                            print_nice(r)
                elif cmdinput[2]=='CLASSES':
                    msg=json.dumps({'class_course':cmdinput[3]})
                    r = requests.get(url+'classes',data=msg)
                    print_nice(r)
            elif (len(cmdinput)==3):
                msg=json.dumps({'id_student':cmdinput[1],'id_class':cmdinput[2]})
                r = requests.get(url+'classes',data=msg)
                print_nice(r)
            else:
                print 'Invalid input'
        except:
            print "Unexpected Error"  
