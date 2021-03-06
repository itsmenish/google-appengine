from flask import Flask, render_template, request
import data

app = Flask(__name__)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments
    )

@app.route('/')
def home():
    projects = data.get_projects()
    return render_template(
        'index.html',
        projects=projects
    )

@app.route('/batchstatus', methods=['POST'])
def batchstatus():
    project = request.form['project']
    batch = data.get_batch_status(project)
    return render_template(
        'batchstatus.html',
        SLA = batch['SLA'],
        SLO = batch['SLO'],
        status = batch['status']
    )