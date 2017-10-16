from flask import Flask,request
from flask_apscheduler import APScheduler
import os,time,datetime,subprocess

app = Flask(__name__)
workdir='/sdcard/'

def job1():
    print('------- start job --------\n')
    print(datetime.datetime.now())
    f=workdir+'nn.py'
    if os.path.exists(f):
        ret=subprocess.call('python nn.py',shell=True)
        print(ret)
    else:
        print('err:nn.py not exists')


sch = APScheduler()
sch.api_enabled = True
sch.init_app(app)
@app.route("/")
def hello():
    return "Hello Worldgggghhhgg!"

@app.route('/addjob')
def addjob():
    if not sch.running:
        sch.start()
    d1=datetime.datetime.now()
    d2=d1+datetime.timedelta(seconds=20) 
    sch.add_job(func=job1,id='job1',trigger='date',run_date=d2)
    return 'add job susscessful'
@app.route('/deljob')
def deljob():
    jobs=sch.get_jobs()
    if len(jobs)>0:
        sch.pause_job('job1')
        sch.delete_job('job1')
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
