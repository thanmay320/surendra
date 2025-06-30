from flask import  Blueprint,render_template
from project_management.models import Project
from flask_login import  login_required
core=Blueprint('core',__name__)

@core.route('/')
def index():
    projects = Project.query.all()  # fetch all projects from the database
    return render_template('index.html', projects=projects)
@core.route("/project/<int:project_id>")
@login_required
def project(project_id):
    project_obj = Project.query.get_or_404(project_id)
    return render_template("project.html", project=project_obj)

@core.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
from flask import render_template
import base64

@core.route('/favorites')
@login_required
def favorite_projects():
    projects = Project.query.all()

    def serialize_project(p):
        return {
            'project_id': p.project_id,
            'project_name': p.project_name,
            'project_description': p.project_description,
            'project_technologies': p.project_technologies,
            'project_price': p.project_price,
            'project_thumbnail': base64.b64encode(p.project_thumbnail).decode('utf-8') if p.project_thumbnail else None
        }

    serialized_projects = [serialize_project(p) for p in projects]
    return render_template('favorite_projects.html', projects=serialized_projects)

