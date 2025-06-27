from flask import  Blueprint,render_template

core=Blueprint('core',__name__)

@core.route('/')
def index():
    return render_template('index.html')
@core.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')