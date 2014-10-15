# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from forms import AddMakerForm
from models import Maker, Category
from flask_login import login_required
from config import DEFAULT_PER_PAGE
from flask.ext.babel import gettext

@app.route('/makers')
@app.route('/makers/<int:page>')
@login_required
def makers(page=1):
    makers = Maker.query.paginate(page, DEFAULT_PER_PAGE, False)
    return render_template('settings/makers.html',
                           title=gettext("Makers"),
                           makers=makers)


@app.route('/addmaker', methods=['GET', 'POST'])
@login_required
def addMaker():
    form = AddMakerForm()
    form.category.choices = [(a.id, a.name_CS) for a in Category.query.all()]
    if form.validate_on_submit():
        maker = Maker()
        maker.name = form.name.data
        maker.category_id = form.category.data
        db.session.add(maker)
        db.session.commit()
        flash(gettext("New maker successfully added."))
        return redirect(url_for("makers"))
    return render_template('settings/addMaker.html',
                           title=gettext("Add New Maker"),
                           form=form)


@app.route('/editmaker/<int:id>', methods=['GET', 'POST'])
@login_required
def editMaker(id=0):
    maker = Maker.query.filter_by(id=id).first()
    if maker == None:
        flash(gettext('Maker not found.'))
        return redirect(url_for('makers'))
    form = AddMakerForm(obj=maker)
    form.category.choices = [(a.id, a.name_CS) for a in Category.query.all()]
    if form.validate_on_submit():

        #delete maker
        if 'delete' in request.form:
            db.session.delete(maker)
            db.session.commit()
            return redirect(url_for("makers"))

        #update maker
        maker.name = form.name.data
        maker.category_id = form.category.data
        db.session.add(maker)
        db.session.commit()
        flash(gettext("Maker successfully changed."))
        return redirect(url_for("makers"))

    selected = maker.category_id
    return render_template('settings/editMaker.html',
                           title=gettext("Edit Maker"),
                           maker=maker,
                           selected=selected,
                           form=form)
