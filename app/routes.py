from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, JobForm, ProfileForm
from app.models import User, Job
from flask_login import login_user, logout_user, login_required, current_user
import logging
import os
from werkzeug.utils import secure_filename

#Logging setup
logging.basicConfig(filename='jobboard.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


#Home Page/Jobs List
@app.route("/")
@app.route("/jobs")
def jobs():  # endpoint = 'jobs'
    all_jobs = Job.query.order_by(Job.date_posted.desc()).all()
    return render_template("jobs.html", jobs=all_jobs)


#Registration
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('jobs'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        logging.info(f"New user registered: {user.email}")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


#Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('jobs'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            logging.info(f"User logged in successfully: {user.email}")
            return redirect(url_for('jobs'))
        else:
            flash('Login failed. Check email or password.', 'danger')
            logging.warning(f"Failed login attempt: {form.email.data}")
    return render_template('login.html', form=form)


#Logout
@app.route("/logout")
@login_required
def logout():
    logging.info(f"User logged out: {current_user.email}")
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('jobs'))


#Add Job
@app.route("/add_job", methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            short_desc=form.short_desc.data,
            full_desc=form.full_desc.data,
            company=form.company.data,
            salary=form.salary.data,
            location=form.location.data,
            category=form.category.data,
            author=current_user
        )
        db.session.add(job)
        db.session.commit()
        flash("Job added successfully!", "success")
        logging.info(f"Job added: {job.title} by {current_user.email}")
        return redirect(url_for('jobs'))
    return render_template("add_job.html", form=form)


#Job Details
@app.route("/job/<int:job_id>")
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template("job_detail.html", job=job)


#Edit Job
@app.route("/edit_job/<int:job_id>", methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        flash("You cannot edit this job.", "danger")
        return redirect(url_for('jobs'))
    form = JobForm(obj=job)
    if form.validate_on_submit():
        job.title = form.title.data
        job.short_desc = form.short_desc.data
        job.full_desc = form.full_desc.data
        job.company = form.company.data
        job.salary = form.salary.data
        job.location = form.location.data
        job.category = form.category.data
        db.session.commit()
        flash("Job updated successfully!", "success")
        logging.info(f"Job edited: {job.title} by {current_user.email}")
        return redirect(url_for('job_detail', job_id=job.id))
    return render_template("edit_job.html", form=form, job=job)


#Delete Job
@app.route("/delete_job/<int:job_id>", methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        flash("You cannot delete this job.", "danger")
        return redirect(url_for('jobs'))
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully!", "success")
    logging.info(f"Job deleted: {job.title} by {current_user.email}")
    return redirect(url_for('jobs'))


#Profile
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data

        if form.profile_image.data:
            image_file = form.profile_image.data
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.root_path, 'static/profile_pics', filename)
            image_file.save(filepath)
            current_user.profile_pic = filename

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))
    return render_template("profile.html", form=form)

#About Page
@app.route("/about")
def about():
    return render_template("about.html")


#Inspiration Page (API)
@app.route("/inspiration")
def inspiration():
    quote = None
    try:
        import requests
        resp = requests.get("https://zenquotes.io/api/random")
        resp.raise_for_status()
        data = resp.json()
        first = data[0]
        quote = {"text": first.get("q"), "author": first.get("a")}
    except Exception as e:
        logging.error(f"ZenQuotes API error: {e}")
    return render_template("inspiration.html", quote=quote)


#User Jobs Page
@app.route("/user/<int:user_id>")
def user_jobs(user_id):
    user = User.query.get_or_404(user_id)
    jobs = Job.query.filter_by(user_id=user.id).order_by(Job.date_posted.desc()).all()
    return render_template("user_jobs.html", user=user, jobs=jobs)


#Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500
