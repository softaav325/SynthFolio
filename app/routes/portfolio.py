from flask import Blueprint, render_template
import logging

portfolio_bp = Blueprint('portfolio', __name__)
logger = logging.getLogger(__name__)

@portfolio_bp.route('/projects')
def projects():
    # In a real app, you would fetch projects from db.session.query(Project).all()
    projects_list = [
        {"id": 1, "title": "Infrastructure Forge", "desc": "IaC Generator for Python"},
        {"id": 2, "title": "Cloud Optimizer", "desc": "Cost analysis tool for AWS"},
    ]
    return render_template('projects.html', projects=projects_list)

@portfolio_bp.route('/project/<int:project_id>')
def project_detail(project_id):
    # Simulation of database fetch
    project = {"id": project_id, "title": "Sample Project", "desc": "Detailed description of the project."}
    return render_template('project_detail.html', project=project)

@portfolio_bp.route('/skills')
def skills():
    skills_list = ["Python", "Flask", "Docker", "Kubernetes", "Terraform", "PostgreSQL"]
    return render_template('skills.html', skills=skills_list)
