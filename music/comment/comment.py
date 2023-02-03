from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo
from music.domainmodel import review
from music.domainmodel.review import Review
import music.utilities.utilities as utilities
import music.comment.services as services

from music.authentication.authentication import login_required


# Configure Blueprint.
comment_blueprint = Blueprint(
    'comment_bp', __name__)

@comment_blueprint.route('/track/<int:track_id>', methods=['GET', 'POST'])
@login_required
def comment(track_id):
    comment_track=services.get_track(track_id,repo.repo_instance)
    
    form = CommentForm()
    if form.validate_on_submit():
        review = Review(comment_track,form.comment.data,form.rating.data)
        services.add_review(review,repo.repo_instance)
    reviews = services.get_reviews(repo.repo_instance)

    return render_template(
            'comment/comment_on_track.html',
            title = comment_track.title,
            form = form,
            reviews = reviews,
            selected_tracks=utilities.get_selected_tracks()
        )

@comment_blueprint.route('/track', methods=['GET', 'POST'])
def target_track():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('comment_bp.comment', track_id=form.id.data))
    else:
        return render_template(
            'comment/track.html',
            form=form,handler_url=url_for("comment_bp.target_track"),
            selected_tracks=utilities.get_selected_tracks()
            )


class SearchForm(FlaskForm):
    id = IntegerField("No. of the track", [DataRequired()])
    submit = SubmitField("Search")

class CommentForm(FlaskForm):
    comment = TextAreaField("Comment",[DataRequired()])
    rating = IntegerField("grade from 1 to 5",[DataRequired()])
    submit = SubmitField("Upload")