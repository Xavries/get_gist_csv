from io import BytesIO
import datetime

from flask import render_template, Blueprint, request, flash, Response

from app import models as m
from app import forms as f
from app import db
from app.commands import get_csv_bites
from app.logger import log


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    form = f.MainForm(request.form)
    all_studies = db.session.scalars(m.Study.select())

    if form.validate_on_submit():

        if not form.study.data.isdigit():
            log(log.WARNING, "Form study error: [study value is not digit]")
            flash("Form study error: study value is not digit", "danger")
            return render_template("index.html", form=form, all_studies=all_studies)

        study: m.Study = db.session.scalar(m.Study.select().where(m.Study.id == int(form.study.data)))
        stdy_popns = [i.population for i in study.populations]

        log(log.INFO, "Form submitted. Study: [%s]", study.study)
        if study:
            log(log.INFO, "Study found.")
            csv_bites: BytesIO = get_csv_bites()
            return Response(csv_bites.getvalue(),
                            mimetype='application/zip',
                            headers={
                                'Content-Disposition':
                                f'attachment;filename=study-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.zip'
                            })
            # return render_template("index.html", form=form, all_studies=all_studies)
        flash("Wrong study name.", "danger")

    elif form.is_submitted():
        log(log.WARNING, "Form submitted error: [%s]", form.errors)
        flash(f"Form submitted error: {form.errors}", "danger")
    return render_template("index.html", form=form, all_studies=all_studies)
