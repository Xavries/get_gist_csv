import os
from io import BytesIO
import datetime

from flask import render_template, Blueprint, request, flash, Response
from alchemical import Alchemical

from app import models as m
from app import forms as f
from app.commands import get_csv_bites
from app.logger import log


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    form = f.MainForm(request.form)
    all_studies = ["no studies found"]
    db_file_path_saved = "db_file_path.txt"

    if not form.db_file_path.data or request.method == "GET":
        if os.path.isfile(db_file_path_saved):
            try:
                with open(db_file_path_saved, "r") as fi:
                    db_path = fi.read()
                # establish connection to the database file
                db = Alchemical("sqlite:///" + os.path.expanduser(db_path))
                session = db.Session()
                all_studies = session.scalars(m.Study.select())
            except Exception as e:
                log(log.ERROR, "Error: [%s]", e)
                flash("No studies found", "danger")
        return render_template("index.html", form=form, all_studies=all_studies)

    if form.remember_path.data:
        open(db_file_path_saved, "w").write(form.db_file_path.data)

    # establish connection to the database file
    db = Alchemical("sqlite:///" + os.path.expanduser(form.db_file_path.data))
    session = db.Session()

    all_studies = session.scalars(m.Study.select())

    if form.validate_on_submit():

        study: m.Study = session.scalar(m.Study.select().where(m.Study.study == form.study.data))

        log(log.INFO, "Form submitted. Study: [%s]", study.study)
        if study:
            log(log.INFO, "Study found.")
            csv_bites: BytesIO = get_csv_bites(db_file_path=form.db_file_path.data)
            session.close()
            return Response(csv_bites.getvalue(),
                            mimetype='application/zip',
                            headers={
                                'Content-Disposition':
                                f'attachment;filename=study-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.zip'
                            })
        flash("Wrong study name.", "danger")
        return render_template("index.html", form=form, all_studies=all_studies)

    elif form.is_submitted():
        log(log.WARNING, "Form submitted error: [%s]", form.errors)
        flash(f"Form submitted error: {form.errors}", "danger")
        session.close()

    else:
        log(log.WARNING, "Something went wrong.")
        flash("Something went wrong.", "danger")
        session.close()
