from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, send_file, abort
)
from flask_login import login_required, current_user
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import mimetypes

from project_management import db
from project_management.projects.forms import ProjectForm
from project_management.models import Project, Image, ProjectFile

project = Blueprint("project", __name__)


# ---------------------------------------------------------------------------
# CREATE PROJECT
# ---------------------------------------------------------------------------
@project.route("/project/create", methods=["GET", "POST"])
@login_required
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():
        # 1) basic fields -----------------------------------------------------
        new_project = Project(
            project_name=form.project_name.data,
            project_description=form.project_description.data,
            project_price=form.project_price.data,
            project_technologies=form.project_technologies.data,
            project_thumbnail=form.project_thumbnail.data.read(),
            user_id=current_user.user_id,
        )
        db.session.add(new_project)
        db.session.flush()        # so we already have new_project.project_id

        # 2) images ----------------------------------------------------------
        for image_file in form.images.data:
            if image_file:
                db.session.add(
                    Image(
                        image_data=image_file.read(),
                        image_name=image_file.filename,
                        project_id=new_project.project_id,
                    )
                )

        # 3) other downloadable files ----------------------------------------
        for file in form.project_files.data:
            if file:
                db.session.add(
                    ProjectFile(
                        file_data=file.read(),
                        file_name=file.filename,
                        project_id=new_project.project_id,
                    )
                )

        db.session.commit()
        flash("Project created successfully!", "success")
        return redirect(url_for("project.projects"))

    return render_template("create_project.html", form=form)


# ---------------------------------------------------------------------------
# LIST + VIEW
# ---------------------------------------------------------------------------
@project.route("/projects")
def projects():
    all_projects = Project.query.all()
    return render_template("projects.html", projects=all_projects)


@project.route("/project/<int:project_id>")
def view_project(project_id):
    project_obj = Project.query.get_or_404(project_id)
    return render_template("view_project.html", project=project_obj)


# ════════════════════════════════════════════════════════════════════════════
# NEW ⬇⬇⬇  DOWNLOAD ENDPOINTS
# ════════════════════════════════════════════════════════════════════════════

def _authorize(project_obj: Project):
    """Block access if the current user doesn’t own this project."""
    if project_obj.user_id != current_user.user_id:
        abort(403, description="You are not authorized to access this project.")


# -- 1) DOWNLOAD ONE FILE ----------------------------------------------------
@project.route("/project/<int:project_id>/file/<int:file_id>/download")
@login_required
def download_file(project_id: int, file_id: int):
    project_obj = Project.query.get_or_404(project_id)
    _authorize(project_obj)

    file_rec = ProjectFile.query.filter_by(
        file_id=file_id, project_id=project_id
    ).first_or_404()

    data = file_rec.file_data                       # bytes
    filename = file_rec.file_name
    mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    buf = BytesIO(data)
    buf.seek(0)

    return send_file(
        buf,
        mimetype=mime_type,
        as_attachment=True,
        download_name=filename,
    )


# -- 2) DOWNLOAD ENTIRE PROJECT AS ZIP ---------------------------------------
@project.route("/project/<int:project_id>/download")
@login_required
def download_project(project_id: int):
    project_obj = Project.query.get_or_404(project_id)
    _authorize(project_obj)

    mem_zip = BytesIO()
    with ZipFile(mem_zip, mode="w", compression=ZIP_DEFLATED) as zf:
        for f in project_obj.files:                 # relationship “files” assumed
            zf.writestr(f.file_name, f.file_data)

    mem_zip.seek(0)
    archive_name = f"{project_obj.project_name or 'project'}_{project_id}.zip"

    return send_file(
        mem_zip,
        mimetype="application/zip",
        as_attachment=True,
        download_name=archive_name,
    )
