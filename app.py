from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


# /기본코드
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.username} {self.title} 추천 by {self.username}'

with app.app_context():
    db.create_all()



@app.route("/")
def home():
    name = '김엄지'
    motto = "웃으면 행복해집니다.방긋"

    context = {
        "name": name,
        "motto": motto,
    }
    return render_template('motto.html', data=context)

@app.route("/music/")
def music():
    # db에서 데이터 가져오는 코드, song_list에 데이터가 담기게 됨
    song_list = Song.query.all()
    return render_template('music.html', data=song_list)

@app.route("/music/<username>")
def render_music_filter(username):
    # username에 따라서 변수에 이름을 넣어을때, filter된 list로 추천인의 list만 보여줌
    filter_list = Song.query.filter_by(username=username).all()
    return render_template('music.html', data=filter_list)


@app.route("/iloveyou/<name>/")
def iloveyou(name):
    motto = f"{name}야 난 너뿐이야!"

    context = {
        'name': name,
        'motto': motto,
    }
    return render_template('motto.html', data=context)

@app.route('/music/create')
def music_create():
    # form에서 보낸 데이터 받아오기
    username_receive = request.args.get('username')
    title_receive = request.args.get('title')
    artist_receive = request.args.get('artist')
    image_url_receive = request.args.get('image_url')

    #데이터를 DB에 저장하기
    song= Song(username=username_receive, title=title_receive, artist=artist_receive, image_url=image_url_receive)
    db.session.add(song)
    db.session.commit()
    # redirect : 페이지를 이동시켜줌, render_music_filter 추천인 기준으로 만든 페이지로.
    return redirect(url_for('render_music_filter', username=username_receive))



# 입학 시험 문제 : 삭제버튼을 만들어서, 
# 삭제버튼을 누르면 해당 카드가 삭제되는 실행 코드 작성

@app.route('/music/delete')
def music_delete():
    id_receive = request.args.get('delete_id')
    delete_data = Song.query.filter_by(id=id_receive).first()
    db.session.delete(delete_data)
    db.session.commit()
    song_list = Song.query.all()
    return redirect(url_for('music'))

if __name__ == "__main__":
    app.run(debug=True)