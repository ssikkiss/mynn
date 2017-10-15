from flask import Flask,request
from flask_apscheduler import APScheduler
import os,time,datetime

app = Flask(__name__)

def job1():
    print('------- start job --------\n')
    print(datetime.datetime.now())

workdir='/sdcard/'

sch = APScheduler()
#sch.api_enabled = True
sch.init_app(app)
@app.route("/")
def hello():
    return "Hello Worldgggghhhgg!"

@app.route('/addjob')
def addjob():
    d1=datetime.datetime.now()
    d2=d1+datetime.timedelta(seconds=10) 
    sch.add_job(job1,'date',run_date=d2,id='job1')
    sch.start()
    return 'add job susscessful'
@app.route('/deljob')
def deljob():
    sch.pause_job('job1')
    sch.remove_job('job')
    sch.shutdown()
    return 'del job susscessful'
@app.route("/file/dir")
def dir():
    ret=''
    try:
        ret=str(os.listdir(workdir))
    except:
        ret='error'
    return ret
@app.route("/file/listdir/<src>")
def listdir(src):
    ret=''
    zsrc=workdir+src
    try:
        ret=str(os.listdir(zsrc))
    except:
        ret='error'
    return ret
@app.route('/file/remove/<src>')
def remove(src):
    ret=''
    try:
        os.remove(workdir+src)
        ret='ok'
    except:
        ret='error'
    return ret
@app.route('/file/create/<src>')
def create(src):
    if not src:
        return 'error:no file name'
    zsrc=workdir+src
    if os.path.exists(zsrc):
        return 'error: file has been exists'
    f=open(zsrc,'wt')
    f.write('')
    f.close()
    return 'ok'
@app.route('/file/write',methods=['post'])
def write():
    ret=''
    filedata=request.form['filedata']
    src=request.form['filename']
    if src=='':
        return 'error:no file name'
    zsrc=workdir+src
    if os.path.exists(zsrc):
        os.remove(zsrc)
    f=open(zsrc,'wt')
    f.write(filedata)
    f.close()
    ret='ok'
    return ret
@app.route('/file/rename/<src>/<dst>')
def rename(src,dst):
    zsrc=workdir+src
    zdst=workdir+dst
    if os.path.exists(zdst):
        return 'error: exists:'+dst
    if not os.path.exists(zsrc):
        return 'error" not exists:'+src
    os.rename(zsrc,zdst)
    return 'ok'

@app.route('/file/read/<src>')
def read(src):
    zsrc=workdir+src
    if not os.path.exists(zsrc):
        return 'error: file not exists:'+src
    f=open(zsrc,'rt')
    r=f.read()
    f.close()
    ret='<form method="post" action="/file/write">\n'
    ret+='<textarea name=filedata id=filedata rows=30 cols=60>'
    ret+=r
    ret+='</textarea><br>'
    ret+='<input type=text name=filename id=filename value="'+src+'"></input><br>'
    ret+='<input type=submit value="   write   "></input><br>'
    return ret




if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
