from flask import render_template, Blueprint, request, redirect, url_for, flash

from app import models as m
from app import forms as f
from app import db
from app.logger import log


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    form = f.MainForm(request.form)
    all_studies = db.session.scalars(m.Study.select()).all()

    if form.validate_on_submit():

        if not form.study.data.isdigit():
            log(log.WARNING, "Form study error: [study value is not digit]")
            flash("Form study error: study value is not digit", "danger")
            return render_template("index.html", form=form, all_studies=all_studies)

        query = db.session.scalar(m.Study.select().where(m.Study.id == int(form.study.data)))
        log(log.INFO, "Form submitted. Study: [%s]", query.study)
        if query:
            log(log.INFO, "Study found.")
            # TODO supply csv
            return render_template("index.html", form=form, all_studies=all_studies)
        flash("Wrong study name.", "danger")

    elif form.is_submitted():
        log(log.WARNING, "Form submitted error: [%s]", form.errors)
        flash(f"Form submitted error: {form.errors}", "danger")
    return render_template("index.html", form=form, all_studies=all_studies)