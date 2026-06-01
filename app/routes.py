from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Course, Module, Lesson, Enrollment, Contact

main = Blueprint('main', __name__)


# ─────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────
@main.route('/')
def index():
    return render_template('index.html')


# ─────────────────────────────────────────────
# AUTH – LOGIN
# ─────────────────────────────────────────────
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.courses'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Bem-vindo de volta, ' + user.username + '!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.courses'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')

    return render_template('login.html')


# ─────────────────────────────────────────────
# AUTH – CADASTRO
# ─────────────────────────────────────────────
@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('main.courses'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm', '').strip()

        if not username or not email or not password:
            flash('Preencha todos os campos obrigatórios.', 'danger')
        elif password != confirm:
            flash('As senhas não coincidem.', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'danger')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('main.login'))

    return render_template('cadastro.html')


# ─────────────────────────────────────────────
# AUTH – LOGOUT
# ─────────────────────────────────────────────
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('main.index'))


# ─────────────────────────────────────────────
# CONTATO
# ─────────────────────────────────────────────
@main.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        titulo = request.form.get('titulo', '').strip()
        telefone = request.form.get('telefone', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name:
            flash('O nome é obrigatório.', 'danger')
            return render_template('contatos.html')

        contact = Contact(
            name=name,
            titulo=titulo,
            telefone=telefone,
            email=email,
            message=message
        )
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('main.receive'))

    return render_template('contatos.html')


# ─────────────────────────────────────────────
# RECEIVE (confirmation)
# ─────────────────────────────────────────────
@main.route('/receive')
def receive():
    return render_template('receive.html')


# ─────────────────────────────────────────────
# QUEM SOMOS
# ─────────────────────────────────────────────
@main.route('/quem-somos')
def quem_somos():
    return render_template('quemsomos.html')


# ─────────────────────────────────────────────
# CURSOS (list)
# ─────────────────────────────────────────────
@main.route('/cursos')
@login_required
def courses():
    all_courses = Course.query.all()
    enrolled_ids = [e.course_id for e in Enrollment.query.filter_by(user_id=current_user.id).all()]
    return render_template('courses.html', courses=all_courses, enrolled_ids=enrolled_ids)


# ─────────────────────────────────────────────
# ENROLL
# ─────────────────────────────────────────────
@main.route('/cursos/<int:course_id>/matricular', methods=['POST'])
@login_required
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    existing = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if not existing:
        enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash(f'Matrícula em "{course.name}" realizada!', 'success')
    else:
        flash(f'Você já está matriculado em "{course.name}".', 'info')
    return redirect(url_for('main.module_view', course_id=course_id))


# ─────────────────────────────────────────────
# MÓDULOS (sidebar + lesson content)
# ─────────────────────────────────────────────
@main.route('/cursos/<int:course_id>/modulos')
@login_required
def module_view(course_id):
    course = Course.query.get_or_404(course_id)
    modules = Module.query.filter_by(course_id=course_id).order_by(Module.order).all()

    # Default: first lesson of first module
    lesson_id = request.args.get('lesson_id', type=int)
    selected_lesson = None
    selected_module = None

    if lesson_id:
        selected_lesson = Lesson.query.get(lesson_id)
        if selected_lesson:
            selected_module = selected_lesson.module
    elif modules and modules[0].lessons:
        selected_lesson = sorted(modules[0].lessons, key=lambda l: l.order)[0]
        selected_module = modules[0]

    return render_template(
        'module.html',
        course=course,
        modules=modules,
        selected_lesson=selected_lesson,
        selected_module=selected_module,
    )
