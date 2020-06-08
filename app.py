import os
from datetime import datetime
from flask_wtf import FlaskForm
from sqlalchemy import null
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort
import time
import os
from util import Pic_str
import base64
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/block?charset=utf8'
app.config["SECRET_KEY"] = "12345678"
db = SQLAlchemy(app)


# block类
class Block(db.Model):
    """block类表"""
    __tablename__ = "block"
    previousHash = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(15), nullable=False)
    msg = db.Column(db.String(30), nullable=False)
    hMsg = db.Column(db.String(64), nullable=False)
    time_stamp = db.Column(db.String(64), nullable=False)
    nonce = db.Column(db.Integer)
    hash = db.Column(db.String(64), nullable=False)


# db.drop_all()
# # 创建所有的表
# db.create_all()


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


# 上传照片
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 上传视频
UPLOAD_FOLDER1 = 'uploadVideo'
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
ALLOWED_EXTENSIONS1 = set(['mp4', 'mpeg', 'mpg', 'dat'])


def allowed_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS1


# 上传音频
UPLOAD_FOLDER2 = 'uploadAudio'
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
ALLOWED_EXTENSIONS2 = set(['cd', 'wave', 'aiff', 'mpeg', 'mp3', 'midi', 'wma', 'vqf', 'amr', 'ape'])


def allowed_audio(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS2


@app.route('/picture')
def picture():
    # 如果需要存储多个文件，需要将数据库增加一行，用以存储图片名字
    # obj_list=Block.query.all()   obj_list=obj_list
    filename = session.get('pictureFilename')
    session['pictureFilename'] = ''
    return render_template('picture.html', filename=filename)


# {{url_for('download',filename=filename)}}
# 上传文件
@app.route('/picture', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        # 输出文件的地址
        print(fname)
        ext = fname.rsplit('.', 1)[1]
        new_filename = Pic_str().create_uuid() + '.' + ext
        # 对图片进行加水印处理

        # 处理结束

        # 图片进行上链处理，并将数据传到数据库

        # 处理结束
        print(new_filename)
        session['pictureFilename'] = new_filename
        f.save(os.path.join(file_dir, new_filename))
        # 保存文件地址
        print(file_dir)
        session['success'] = '上传成功'
        return redirect('/picture')
    else:
        session['success'] = '上传失败'
        return redirect('/picture')


@app.route('/picture/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('upload', filename)):
            # 对获取的图片进行解水印处理

            # 处理结束
            return send_from_directory('upload', filename, as_attachment=True)
        pass


# 上传音频
@app.route('/audio')
def audio():
    filename = session.get('audioFilename')
    session['audioFilename'] = ''
    return render_template('audio.html', filename=filename)


# 上传音频
@app.route('/audio', methods=['POST'], strict_slashes=False)
def up_audio():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER2'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['audio']
    if f and allowed_audio(f.filename):
        fname = secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]
        new_filename = Pic_str().create_uuid() + '.' + ext
        # 对音频进行加水印处理

        # 处理结束

        # 音频进行上链处理，并将数据传到数据库

        # 处理结束
        print(new_filename)
        session['audioFilename'] = new_filename
        session['success'] = '上传成功'
        f.save(os.path.join(file_dir, new_filename))
        print(file_dir)
        return redirect('/audio')
    else:
        session['success'] = '上传失败'
        return redirect('/audio')


@app.route('/audio/<string:filename>', methods=['GET'])
def down_audio(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('uploadAudio', filename)):
            # 对音频进行解水印处理

            # 处理结束
            return send_from_directory('uploadAudio', filename, as_attachment=True)
        pass


# 上传视频
@app.route('/video')
def video():
    # obj_list = Block.query.all()
    filename = session.get('videoFilename')
    session['videoFilename'] = ''
    return render_template('video.html', filename=filename)


# 上传视频
@app.route('/video', methods=['POST'], strict_slashes=False)
def up_video():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER1'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['video']
    if f and allowed_video(f.filename):
        fname = secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]
        new_filename = Pic_str().create_uuid() + '.' + ext
        # 对视频进行加水印处理

        # 处理结束

        # 视频进行上链处理，并将数据传到数据库

        # 处理结束
        session['videoFilename'] = new_filename
        f.save(os.path.join(file_dir, new_filename))
        print(file_dir)
        return redirect('/video')
    else:
        return redirect('/video')


@app.route('/video/<string:filename>', methods=['GET'])
def down_video(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('uploadVideo', filename)):
            # 对视频进行解水印处理

            # 处理结束
            return send_from_directory('uploadVideo', filename, as_attachment=True)
        pass


@app.route('/table', methods=['GET'])
def table():
    obj_list = Block.query.all()
    if obj_list:
        return render_template('table.html', obj_list=obj_list)
    return render_template('table.html')


@app.route('/aboutUs')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
