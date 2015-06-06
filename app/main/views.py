from flask import render_template, current_app, flash, redirect, url_for, request
from flask.ext.login import login_required, current_user
from .. models import User, Post
from .forms import EditAboutForm, PostForm
from . import main
from .. import db


@main.route('/index/<path:classify>',methods=['GET','POST'])
def index(classify):
    if classify == 'all':
        page = request.args.get('page',1,type=int);
        pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=10,error_out=False)
        posts = pagination.items
    else:
        page = request.args.get('page',1,type=int);
        pagination = Post.query.filter_by(classify=classify).order_by(Post.timestamp.desc()).paginate(page,per_page=10,error_out=False)
        posts = pagination.items
    print pagination;
    return render_template('index.html',posts=posts,pagination=pagination);

@main.route('/edit-post',methods=['GET','POST'])
@login_required
def edit_post():
    form = PostForm();
    if form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user._get_current_object(),classify=form.classify.data,title=form.title.data);
        db.session.add(post);
    return render_template('edit_post.html',form=form)

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id);
    return render_template('post.html',posts=[post])

@main.route('/about')
def about():
    if current_user.is_authenticated():
        user = current_user;
    else:
        user = User.query.filter_by(username='yzxu').first();
    return render_template('user.html',user=user);

@main.route('/edit-about',methods=['GET','POST'])
@login_required
def edit_about():
    form = EditAboutForm();
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data;
        flash('Your about has been updated');
        #return redirect(url_for('.user',username=current_user.username));
    form.about_me.data = current_user.about_me;
    return render_template('edit_about.html',form=form)
