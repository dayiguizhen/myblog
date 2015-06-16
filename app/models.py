import hashlib
from datetime import datetime
from . import db,login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach

class User(UserMixin,db.Model):
    __tablename__ = 'users';
    id = db.Column(db.Integer,primary_key = True);
    email = db.Column(db.String(64),unique=True,index=True);
    username = db.Column(db.String(64),unique=True,index=True);
    password_hash = db.Column(db.String(128));
    about_me = db.Column(db.Text());
    about_me_html = db.Column(db.Text);
    posts = db.relationship('Post',backref='author',lazy='dynamic');

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password);
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    @staticmethod
    def on_changed_about(target,value,oldvalue,initiator):
        allowed_tags = ['a','abbr','acronym','b','blockquote','code','em','i','li','ol','pre','strong','ul','h1','h2','h3','h4','p'];
        target.about_me_html = bleach.linkify(bleach.clean(markdown(value,output_format='html'),tags=allowed_tags,strip=True));
db.event.listen(User.about_me,'set',User.on_changed_about)

class Post(db.Model):
    __tablename__ = 'posts';
    id = db.Column(db.Integer,primary_key=True);
    body = db.Column(db.Text);
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow);
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'));
    classify = db.Column(db.String(64));
    body_html = db.Column(db.Text);
    readmore = db.Column(db.Text);
    readmore_html = db.Column(db.Text);
    title = db.Column(db.String(64));

    @staticmethod
    def on_change_body(target,value,oldvalue,initiator):
        allowed_tags = ['a','abbr','acronym','b','blockquote','code','em','i','li','ol','pre','strong','ul','h1','h2','h3','h4','p'];
        #target.body_html = bleach.linkify(bleach.clean(markdown(value,output_format='html'),tags=allowed_tags,strip=True));
        target.body_html = bleach.linkify(markdown(value,output_format='html'));

    def on_change_readmore(target,value,oldvalue,initiator):
        allowed_tags = ['a','abbr','acronym','b','blockquote','code','em','i','li','ol','pre','strong','ul','h1','h2','h3','h4','p'];
        target.readmore_html = bleach.linkify(bleach.clean(markdown(value,output_format='html'),tags=allowed_tags,strip=True));
db.event.listen(Post.body,'set',Post.on_change_body)
db.event.listen(Post.readmore,'set',Post.on_change_readmore)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id));