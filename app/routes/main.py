from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # В будущем здесь будет логика получения данных из БД
    return render_template('index.html', title="Портфолио Разработчика")

@main_bp.route('/projects')
def projects():
    return render_template('projects.html', title="Мои Проекты")

@main_bp.route('/about')
def about():
    return render_template('about.html', title="Обо мне")

@main_bp.route('/contact')
def contact():
    return render_template('contact.html', title="Контакты")
