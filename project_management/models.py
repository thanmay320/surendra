from werkzeug.security import generate_password_hash, check_password_hash
from project_management import db, login_manager
from flask_login import UserMixin

# ---------- Flask-Login Loader ----------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# ---------- Table 1: Users ----------
class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    user_mail = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")
    user_friend = db.Column(db.String(100), nullable=False, default="user")
    password_hash = db.Column(db.String(255), nullable=False)

    # one-to-many
    projects = db.relationship("Project", backref="user", lazy=True)

    def __init__(self, username, user_mail, password, user_friend, role="user"):
        self.username = username
        self.user_mail = user_mail
        self.role = role
        self.user_friend = user_friend
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"<User {self.username}>"

# ---------- Table 2: Projects ----------
class Project(db.Model):
    __tablename__ = "projects"
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(150), nullable=False)
    project_description = db.Column(db.Text, nullable=True)
    project_price = db.Column(db.Float, nullable=False)
    project_technologies = db.Column(db.String(256), nullable=False)
    project_thumbnail = db.Column(db.LargeBinary(length=(16 * 1024 * 1024)), nullable=False)  # 16MB
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    # one-to-many
    images = db.relationship("Image", backref="project", lazy=True)
    files = db.relationship("ProjectFile", backref="project", lazy=True)

    def __repr__(self):
        return f"<Project {self.project_name}>"

# ---------- Table 3: Images ----------
class Image(db.Model):
    __tablename__ = "images"
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_data = db.Column(db.LargeBinary(length=(16 * 1024 * 1024)), nullable=False)
    image_name = db.Column(db.String(100), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"), nullable=False)

    def __repr__(self):
        return f"<Image {self.image_name}>"

# ---------- Table 4: Project Files ----------
class ProjectFile(db.Model):
    __tablename__ = "project_files"
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_data = db.Column(db.LargeBinary(length=(64 * 1024 * 1024)), nullable=False)  # 64MB
    file_name = db.Column(db.String(255), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"), nullable=False)

    def __repr__(self):
        return f"<ProjectFile {self.file_name}>"
