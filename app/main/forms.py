from flask.ext.wtf import Form
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import Required
from flask.ext.pagedown.fields import PageDownField

class EditAboutForm(Form):
	about_me = PageDownField('about_me',validators=[Required()]);
	submit = SubmitField('Submit');

class PostForm(Form):
	title = TextAreaField('title',validators=[Required()]);
	body = PageDownField("What's on your mind?",validators=[Required()]);
	readmore = PageDownField("article's first paragraph",validators=[Required()])
	classify = SelectField(u'type',coerce=str,choices=[('zhuxian','zhuxian'),('luxian','luxian'),( 'xianxian','xianxian'),('juexian','juexian')]);
	submit = SubmitField('Submit');