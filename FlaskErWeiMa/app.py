from flask import Flask,render_template,redirect,url_for,request
import qrc
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('url'))

@app.route('/url',methods=['GET','POST'])
def url():
    if request.method  == 'GET':
        return render_template('url.html',title='链接生成二维码')
    else:

        url = request.form['URL']
        imgUrl = qrc.reurl(url)
        return render_template('urlimg.html',imgUrl=imgUrl,url = url,title='链接生成二维码')

@app.route('/text',methods=['GET','POST'])
def text():
    if request.method  == 'GET':
        return render_template('text.html',title='文字生成二维码')
    else:
        text = request.form['TEXT']
        imgUrl = qrc.reurl(text)
        return render_template('textimg.html',imgUrl=imgUrl,text = text,title='文字生成二维码')

if __name__ == '__main__':
    app.run()