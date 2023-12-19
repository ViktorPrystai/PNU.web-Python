from flask import render_template, redirect, url_for,  flash
from app import db
from .forms import FeedbackForm
from .models import Feedback
from . import feedback_blueprint


@feedback_blueprint.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        message = form.message.data

        feedback = Feedback(name=name, message=message)
        db.session.add(feedback)
        db.session.commit()
        flash('Ваш відгук був збережений', 'success')
        return redirect(url_for('.feedback'))

    feedbacks = Feedback.query.all()
    return render_template('feedback/feedback.html', form=form, feedbacks=feedbacks)

@feedback_blueprint.route('/delete_feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if feedback:
        db.session.delete(feedback)
        db.session.commit()
        flash('Відгук був видалений', 'success')
    else:
        flash('Відгук не знайдено', 'danger')
    return redirect(url_for('.feedback'))