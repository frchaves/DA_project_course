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
            print 'Nenhum resultado encontrado'
        for x in res.keys():
            print "ID aluno: "+x
            print "Nome: "+res[x][0]
            print "Nacionalidade: "+res[x][1]
            print "Idade: "+str(res[x][2])
            print "\n"
    elif res.has_key("tableAD"):
        res=res["tableAD"]
        if res=={}:
            print 'Nenhum resultado encontrado'
        for x in res.keys():
            print "ID disciplina: "+x
            print "Designacao: "+res[x][0]
            print "Semestre: "+str(res[x][1])
            print "Ano: "+str(res[x][2])
            print "\n"
    elif res.has_key("tableAT"):
        res=res["tableAT"]
        if res=={}:
            print 'Nenhum resultado encontrado'
        for x in res.keys():
            print "ID Turma: "+x
            print "ID disciplina : "+str(res[x][0])
            print "tipo: "+res[x][1]
            print "designacao: "+res[x][2]
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
                if cmdinput[1]=="ALUNO":
                    msg=json.dumps({'nacionalidade':cmdinput[2],'idade':cmdinput[3],'nome':cmdinput[4]})
                    r = requests.put(url+'alunos',data=msg)
                    print_nice(r)
                elif cmdinput[1]=="DISCIPLINA":
                    msg=json.dumps({'ano':cmdinput[2],'semestre':cmdinput[3],'designacao':cmdinput[4]})
                    r = requests.put(url+'disciplinas',data=msg)
                    print_nice(r)
                elif cmdinput[1]=="TURMA":
                    msg=json.dumps({'id_disciplina':cmdinput[2],'tipo':cmdinput[3],'designacao':cmdinput[4]})
                    r = requests.put(url+'turmas',data=msg)
                    print_nice(r)
            elif (len(cmdinput)==3):
                msg=json.dumps({'id_aluno':cmdinput[1],'id_turma':cmdinput[2]})
                r = requests.post(url+'turmas',data=msg)
                print_nice(r)
            else:
                print "Invalid input"
        except:
            print "Unexpected Error"
    elif cmdinput[0]=="REMOVE":
        try:
            if cmdinput[1]=="ALUNO":
                msg=json.dumps({'id_aluno':cmdinput[2]})
                r = requests.delete(url+'alunos',data=msg)
                print_nice(r)
            elif cmdinput[1]=="DISCIPLINA":
                msg=json.dumps({'id_disciplina':cmdinput[2]})
                r = requests.delete(url+'disciplinas',data=msg)
                print_nice(r)
            elif cmdinput[1]=="TURMA":
                msg=json.dumps({'id_turma':cmdinput[2]})
                r = requests.delete(url+'turmas',data=msg)
                print_nice(r)   
            elif cmdinput[1]=="ALL":
                if len(cmdinput)==3:
                    if cmdinput[2]=='ALUNOS':
                        r = requests.delete(url+'alunos')
                        print_nice(r)
                    elif cmdinput[2]=="DISCIPLINAS":
                        r = requests.delete(url+'disciplinas')
                        print_nice(r)
                    elif cmdinput[2]=="TURMAS":
                        r = requests.delete(url+'turmas')
                        print_nice(r)
                elif cmdinput[2]=='ALUNOS':
                    if cmdinput[3]=="TURMA":
                            msg=json.dumps({'alunos_turma':cmdinput[4]})
                            r = requests.delete(url+'alunos',data=msg)
                            print_nice(r)
                    elif cmdinput[3]=="DISCIPLINA":
                            msg=json.dumps({'alunos_disciplina':cmdinput[4]})
                            r = requests.delete(url+'alunos',data=msg)
                            print_nice(r)
                elif cmdinput[2]=='TURMAS':
                    msg=json.dumps({'turma_disciplina':cmdinput[3]})
                    r = requests.delete(url+'turmas',data=msg)
                    print_nice(r)
            elif (len(cmdinput)==3):
                msg=json.dumps({'id_aluno':cmdinput[1],'id_turma':cmdinput[2]})
                r = requests.delete(url+'turmas',data=msg)
                print_nice(r)
            else:
                print 'Invalid input'
        except:
            print "Unexpected Error"        
    elif cmdinput[0]=="SHOW":
        try:
            if cmdinput[1]=="ALUNO":
                msg=json.dumps({'id_aluno':cmdinput[2]})
                r = requests.get(url+'alunos',data=msg)
                print_nice(r)
            elif cmdinput[1]=="DISCIPLINA":
                msg=json.dumps({'id_disciplina':cmdinput[2]})
                r = requests.get(url+'disciplinas',data=msg)
                print_nice(r)
            elif cmdinput[1]=="TURMA":
                msg=json.dumps({'id_turma':cmdinput[2]})
                r = requests.get(url+'turmas',data=msg)
                print_nice(r)
            elif cmdinput[1]=="ALL":
                if len(cmdinput)==3:
                    if cmdinput[2]=='ALUNOS':
                        r = requests.get(url+'alunos')
                        print_nice(r)
                    elif cmdinput[2]=="DISCIPLINAS":
                        r = requests.get(url+'disciplinas')
                        print_nice(r)
                    elif cmdinput[2]=="TURMAS":
                        r = requests.get(url+'turmas')
                        print_nice(r)
                elif cmdinput[2]=='ALUNOS':
                    if cmdinput[3]=="TURMA":
                            msg=json.dumps({'alunos_turma':cmdinput[4]})
                            r = requests.get(url+'alunos',data=msg)
                            print_nice(r)
                    elif cmdinput[3]=="DISCIPLINA":
                            msg=json.dumps({'alunos_disciplina':cmdinput[4]})
                            r = requests.get(url+'alunos',data=msg)
                            print_nice(r)
                elif cmdinput[2]=='TURMAS':
                    msg=json.dumps({'turma_disciplina':cmdinput[3]})
                    r = requests.get(url+'turmas',data=msg)
                    print_nice(r)
            elif (len(cmdinput)==3):
                msg=json.dumps({'id_aluno':cmdinput[1],'id_turma':cmdinput[2]})
                r = requests.get(url+'turmas',data=msg)
                print_nice(r)
            else:
                print 'Invalid input'
        except:
            print "Unexpected Error"  
