#!/usr/bin/env python
# -*- coding: cp1252 -*-
# all the imports
#must read https://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor.execute
"""
 Aplicacoes distribuidas 

"""
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,make_response

from contextlib import closing
import json
import os.path
# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
if not os.path.isfile('flaskr.db'):
    init_db()
    

##request handel
@app.before_request
def before_request():
    g.db = connect_db()
    g.db.execute("PRAGMA foreign_keys = ON")

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def strISint(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

##ADD
##aluno
@app.route('/alunos', methods=['PUT'])
def add_alunos():
    try:
        req = request.data
        req = json.loads(req)
        if not strISint(req['idade']):
           raise ValueError('Idade must be int')
        g.db.execute('insert into alunos (nome, nacionalidade,idade)values (?,?,?)',(req['nome'],req['nacionalidade'],req['idade']))
        g.db.commit()
        msg=json.dumps({"message":'New entry was successfully added'})
        resp = make_response(msg, 200)
        return  resp
    except ValueError as erro:
        msg=json.dumps({"message":'New entry was not added \nCause: '+erro.args[0]})
        resp = make_response(msg, 400)
        return  resp
##disciplina
@app.route('/disciplinas', methods=['PUT'])
def add_disciplinas():
    try:
        req = request.data
        req = json.loads(req)
        if not req['ano'] in ('1','2','3','4','5'):
           raise ValueError('Ano must be between 1 and 5')
        if not req['semestre'] in ('1','2'):
            raise ValueError('Semestre must be int between 1 and 2')
        g.db.execute('insert into disciplina (ano, semestre,designacao)values (?,?,?)',(req['ano'],req['semestre'],req['designacao']))
        g.db.commit()
        msg=json.dumps({"message":'New entry was successfully added'})
        resp = make_response(msg, 200)
        return  resp
    except ValueError as erro:
        msg=json.dumps({"message":'New entry was not added \nCause: '+erro.args[0]})
        resp = make_response(msg, 400)
        return  resp   
##turma
@app.route('/turmas', methods=['PUT'])
def add_turmas():
    try:
        req = request.data
        req = json.loads(req)
        chek = g.db.execute("SELECT EXISTS(SELECT id FROM disciplina WHERE id=?)",req['id_disciplina']).fetchone()
        if not chek[0]==1:
            raise ValueError('Id disciplina must be int and exist')
        if not req['tipo'] in ('T','TP','PL','O','OT'):
            raise ValueError('Tipo must be one of the following (T,TP,PL,O,OT)')
        test = g.db.execute('insert into turma (id_disciplina, tipo,designacao)values (?,?,?)',(req['id_disciplina'],req['tipo'],req['designacao']))
        g.db.commit()
        msg=json.dumps({"message":'New entry was successfully added'})
        resp = make_response(msg, 200)
        return  resp
    except ValueError as erro:
        msg=json.dumps({"message":'New entry was not added \nCause: '+erro.args[0]})
        resp = make_response(msg, 400)
        return  resp
##turma aluno
@app.route('/turmas', methods=['POST'])
def add_aluno_truma():
    try:
        req = request.data
        req = json.loads(req)
        chek1 = g.db.execute("SELECT EXISTS(SELECT id FROM alunos WHERE id=?)",req['id_aluno']).fetchone()
        if not chek1[0]==1:
            raise ValueError('Id aluno must be int and exist')
        chek2 = g.db.execute("SELECT EXISTS(SELECT id FROM turma WHERE id=?)",req['id_turma']).fetchone()
        if not chek2[0]==1:
            raise ValueError('Id turma must be int and exist')
        g.db.execute('insert into inscricoes (id_aluno, id_turma)values (?,?)',(req['id_aluno'],req['id_turma']))
        g.db.commit()
        msg=json.dumps({"message":'New entry was successfully added'})
        resp = make_response(msg, 200)
        return  resp
    except ValueError as erro:
        msg=json.dumps({"message":'New entry was not added \nCause: '+erro.args[0]})
        resp = make_response(msg, 400)
        return  resp
    except  sqlite3.IntegrityError:
        msg=json.dumps({"message":'New entry was not added \nCause: Aluno ja esta inscrito na turma'})
        resp = make_response(msg, 400)
        return  resp        
##REMOVE
##aluno
@app.route('/alunos', methods=['DELETE'])
def del_alunos():
    try:
        req = request.data
        if req == '':
            g.db.execute('DELETE FROM alunos')
            g.db.commit()
            msg=json.dumps({"message":'ALL Entrys were successfully DELETED'})
            resp = make_response(msg, 200)
            return  resp
        else:
            req = json.loads(req)
            if req.has_key("id_aluno"):
                if not strISint(req['id_aluno']):
                   raise ValueError('Id of aluno must be int')
                chek=g.db.execute('DELETE FROM alunos WHERE id==?',req['id_aluno'])
                g.db.commit()
                if chek.rowcount == 1:
                    msg=json.dumps({"message":'Entry was successfully DELETED'})
                else:
                    msg=json.dumps({"message":'Entry didnt exist no rows affected'})
                resp = make_response(msg, 200)
                return  resp
            elif req.has_key("alunos_turma"):
                if not strISint(req['alunos_turma']):
                   raise ValueError('Id of turma must be int')
                search = g.db.execute('select id_aluno from inscricoes where id_turma=?',req['alunos_turma'])
                n = 0
                for row in search.fetchall():
                    g.db.execute('DELETE FROM alunos WHERE id==?',str(row[0]))
                    g.db.commit()
                    n+=1
                msg=json.dumps({"message": str(n)+' Entrys were successfully DELETED'})
                resp = make_response(msg, 200)
                return  resp
            elif req.has_key("alunos_disciplina"):
                if not strISint(req['alunos_disciplina']):
                   raise ValueError('Id of disciplina must be int')
                search = g.db.execute('select i.id_aluno from inscricoes as i ,turma as t where i.id_turma=t.id and id_disciplina=?',req['alunos_disciplina'])
                n = 0
                for row in search.fetchall():
                    g.db.execute('DELETE FROM alunos WHERE id==?',str(row[0]))
                    g.db.commit()
                    n+=1
                msg=json.dumps({"message": str(n)+' Entries were successfully DELETED'})
                resp = make_response(msg, 200)
                return  resp
    except ValueError as erro:
        msg=json.dumps({"message":'No Entries were deleted \nCause: '+erro.args[0]})
        resp = make_response(msg, 400)
        return  resp
    except:
        msg=json.dumps({"message":'Unexpected Error; No Entries were deleted'})
        resp = make_response(msg, 400)
        return  resp     
##disciplina
@app.route('/disciplinas', methods=['DELETE'])
def del_disciplinas():
    try:
        req = request.data
        if req == '':
            g.db.execute('DELETE FROM disciplina')
            g.db.commit()
            msg=json.dumps({"message":'ALL Entries were successfully DELETED'})
            resp = make_response(msg, 200)
            return  resp
        else:
            req = json.loads(req)
            if req.has_key("id_disciplina"):
                if not strISint(req['id_disciplina']):
                   raise ValueError('Id da disciplina must be int')                
                chek=g.db.execute('DELETE FROM disciplina WHERE id==?',req['id_disciplina'])
                g.db.commit()
                if chek.rowcount == 1:
                    msg=json.dumps({"message":'Entry was successfully DELETED'})
                else:
                    msg=json.dumps({"message":'Entry didnt exist no rows affected'})                
                msg=json.dumps({"message":'Unexpected Error; No Entries were deleted'})
                resp = make_response(msg, 200)
                return  resp
    except ValueError as erro:
        msg=json.dumps({"message":'No Entries were deleted \nCause: '+erro.args[0]})
        resp = make_response(msg, 400)
        return  resp
    except:
        msg=json.dumps({"message":'No Entries were deleted'})
        resp = make_response(msg, 400)
        return  resp     
##turma
@app.route('/turmas', methods=['DELETE'])
def del_turmas():
    try:
        req = request.data
        if req == '':
            g.db.execute('DELETE FROM turma')
            g.db.commit()
            msg=json.dumps({"message":'ALL Entries were successfully DELETED'})
            resp = make_response(msg, 200)
            return  resp
        else:
            req = json.loads(req)
            if req.has_key("id_aluno")and req.has_key("id_turma"):
                if not strISint(req['id_aluno']):
                   raise ValueError('Id of aluno must be int')
                if not strISint(req['id_turma']):
                   raise ValueError('Id of turma must be int')
                chek = g.db.execute('DELETE FROM inscricoes WHERE id_aluno==? and id_turma==?',(req['id_aluno'],req['id_turma']))
                g.db.commit()
                if chek.rowcount == 1:
                    msg=json.dumps({"message":'Entry was successfully DELETED'})
                else:
                    msg=json.dumps({"message":'Entry didnt exist no rows affected'})    
                resp = make_response(msg, 200)
                return  resp    
            elif req.has_key("id_turma"):
                if not strISint(req['id_turma']):
                   raise ValueError('Id of turma must be int') 
                chek=g.db.execute('DELETE FROM turma WHERE id==?',req['id_turma'])
                g.db.commit()
                if chek.rowcount == 1:
                    msg=json.dumps({"message":'Entry was successfully DELETED'})
                else:
                    msg=json.dumps({"message":'Entry didnt exist no rows affected'})                   
                resp = make_response(msg, 200)
                return  resp
            elif req.has_key("turma_disciplina"):
                if not strISint(req['turma_disciplina']):
                   raise ValueError('Id da disciplina must be int') 
                search = g.db.execute('select id from turma where id_disciplina = ?',str(req['turma_disciplina']))
                n = 0
                for row in search.fetchall():
                    g.db.execute('DELETE FROM turma WHERE id==?',str(row[0]))
                    g.db.commit()
                    n+=1
                msg=json.dumps({"message": str(n)+' Entries were successfully DELETED'})
                resp = make_response(msg, 200)
                return  resp            
    except ValueError as erro:
        msg=json.dumps({"message":'No Entries were deleted \nCause: '+erro.args[0]})
        resp = make_response(msg, 400)
        return  resp
    except:
        msg=json.dumps({"message":'No Entries were deleted'})
        resp = make_response(msg, 400)
        return  resp




@app.route('/alunos', methods=['GET'])
def show_alunos():
    try:
        req = request.data
        if req == '':
            cur = g.db.execute('select * from alunos order by id desc')
            entries = {}
            for row in cur.fetchall():
                entries[row[0]]=(row[1],row[2],row[3])
            msg={"tableAA":entries}
            msg = json.dumps(msg)
            resp = make_response(msg, 200)
            return resp
        else:
            req = json.loads(req)
            if req.has_key("id_aluno"):
                if not strISint(req['id_aluno']):
                   raise ValueError('Id of aluno must be int') 
                row = g.db.execute('select * from alunos where id = ? order by id desc',req["id_aluno"]).fetchone()
                if row!=None:
                    entries = {row[0]:(row[1],row[2],row[3])}
                    msg={"tableAA":entries}
                    msg = json.dumps(msg)
                else:
                    msg=json.dumps({"message":'No entries found'})
                resp = make_response(msg, 200)
                return resp
            elif req.has_key("alunos_turma"):
                if not strISint(req['alunos_turma']):
                   raise ValueError('Id of turma must be int') 
                search = g.db.execute('select id_aluno from inscricoes where id_turma=?',req['alunos_turma'])
                entries = {}
                for row in search.fetchall():
                    row1 = g.db.execute('select * from alunos where id = ? order by id desc',str(row[0])).fetchone()
                    entries[row1[0]]=(row1[1],row1[2],row1[3])
                msg={"tableAA":entries}
                msg = json.dumps(msg)
                resp = make_response(msg, 200)
                return resp
            elif req.has_key("alunos_disciplina"):
                if not strISint(req['alunos_disciplina']):
                   raise ValueError('Id da disciplina must be int') 
                search = g.db.execute('select i.id_aluno from inscricoes as i ,turma as t where i.id_turma=t.id and id_disciplina=?',req['alunos_disciplina'])
                entries = {}
                for row in search.fetchall():
                    row1 = g.db.execute('select * from alunos where id = ? order by id desc',str(row[0])).fetchone()
                    entries[row1[0]]=(row1[1],row1[2],row1[3])
                msg={"tableAA":entries}
                msg = json.dumps(msg)
                resp = make_response(msg, 200)
                return resp
    except ValueError as erro:
        msg=json.dumps({"message":'No Entries were deleted \nCause: '+erro.args[0]})
        resp = make_response(msg, 400)
        return  resp
    except:
        msg=json.dumps({"message":'No Entries Available'})
        resp = make_response(msg, 400)
        return  resp
@app.route('/disciplinas', methods=['GET'])
def show_disciplinas():
    try:
        req = request.data
        if req == '':
            cur = g.db.execute('select * from disciplina order by id desc')
            entries = {}
            for row in cur.fetchall():
                entries[row[0]]=(row[1],row[2],row[3])
            msg={"tableAD":entries}
            msg = json.dumps(msg)
            resp = make_response(msg, 200)
            return resp
        else:
            req = json.loads(req)
            if req.has_key("id_disciplina"):
                if not strISint(req['id_disciplina']):
                   raise ValueError('Id of disciplina must be int') 
                row = g.db.execute('select * from disciplina where id = ? order by id desc',req["id_disciplina"]).fetchone()
                if row!=None:
                    entries = {row[0]:(row[1],row[2],row[3])}
                    msg={"tableAD":entries}
                    msg = json.dumps(msg)
                else:
                    msg=json.dumps({"message":'No entry found'})
                resp = make_response(msg, 200)
                return resp
    except ValueError as erro:
        msg=json.dumps({"message":'No Entries were deleted \nCause: '+erro.args[0]})
        resp = make_response(msg, 400)
        return  resp
    except:
        msg=json.dumps({"message":'No Entries Available ERROR'})
        resp = make_response(msg, 400)
        return  resp


@app.route('/turmas', methods=['GET'])
def show_turmas():
    try:
        req = request.data
        if req == '':
            cur = g.db.execute('select * from turma order by id desc')
            entries = {}
            for row in cur.fetchall():
                entries[row[0]]=(row[1],row[2],row[3])
            msg={"tableAT":entries}
            msg = json.dumps(msg)
            resp = make_response(msg, 200)
            return resp
        else:
            req = json.loads(req)
            if req.has_key("id_aluno") and req.has_key("id_turma"):
                if not strISint(req['id_aluno']):
                   raise ValueError('Id of aluno must be int')
                if not strISint(req['id_turma']):
                   raise ValueError('Id da turma must be int')
                row = g.db.execute('select * from inscricoes WHERE id_aluno==? and id_turma==?',(str(req['id_aluno']),str(req['id_turma']))).fetchone()
                if row!=None:
                    msg={"message":"Aluno "+str(req['id_aluno'])+" esta inscrito na turma "+str(req['id_turma'])}
                else:
                    msg={"message":"Aluno "+str(req['id_aluno'])+" NAO esta inscrito na turma "+str(req['id_turma'])}
                msg = json.dumps(msg)
                resp = make_response(msg, 200)
                return resp  
            elif req.has_key("id_turma"):
                if not strISint(req['id_turma']):
                   raise ValueError('Id of turma must be int') 
                row = g.db.execute('select * from turma where id = ? order by id desc',req["id_turma"]).fetchone()
                if row!=None:
                    entries = {row[0]:(row[1],row[2],row[3])}
                    msg={"tableAT":entries}
                    msg = json.dumps(msg)
                else:
                    msg=json.dumps({"message":'No entry found'})    
                resp = make_response(msg, 200)
                return resp
            elif req.has_key("turma_disciplina"):
                if not strISint(req['turma_disciplina']):
                   raise ValueError('Id da disciplina must be int')
                search = g.db.execute('select * from turma where id_disciplina=? order by id desc',str(req['turma_disciplina']))
                entries = {}
                for row in search.fetchall():
                    entries[row[0]]=(row[1],row[2],row[3])
                msg={"tableAT":entries}
                msg = json.dumps(msg)
                resp = make_response(msg, 200)
                return resp
    except ValueError as erro:
        msg=json.dumps({"message":'No Entries were deleted \nCause: '+erro.args[0]})
        resp = make_response(msg, 400)
        return  resp
    except:
        msg=json.dumps({"message":'No Entries Available'})
        resp = make_response(msg, 400)
        return  resp


if __name__ == '__main__':
    app.run()
