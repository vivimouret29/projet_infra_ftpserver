from flask import Flask, redirect, url_for, flash, make_response, session
from flask import render_template
import utils
from flask import request

FTP_OBJECT = None

app = Flask(__name__)


@app.route('/')
def login():
    if FTP_OBJECT != None:
        home()
    else:
        return render_template('login.html')


@app.route('/index', methods=['GET', 'POST'])
def home():
    global FTP_OBJECT
    if request.method == 'POST':
        if FTP_OBJECT == None:
            user = request.form['User']
            path = request.form['Path']
            pwd = request.form['Pwd']
            FTP_OBJECT = utils.Ftp(user=user, passwd=pwd, path=path)
            ls_res = FTP_OBJECT.ls()
            return render_template('index.html', user=user, ls_res=ls_res)
    if FTP_OBJECT != None:
        fichier = 'test'
        user = FTP_OBJECT.user
        print(FTP_OBJECT.path)
        ls_res = FTP_OBJECT.cd(fichier+'/')
    return render_template('index.html', user=user, ls_res=ls_res)


if __name__ == '__main__':
    app.run()
