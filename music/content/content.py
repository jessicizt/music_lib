from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import music.adapters.repository as repo
import music.content.services as services
import music.utilities.utilities as utilities

# Configure Blueprint.
content_blueprint = Blueprint(
    'content_bp', __name__, url_prefix='/content')

@content_blueprint.route('/tracks', methods=['GET'])
def tracks():
    tracks_per_page = 20
    cursor = request.args.get('cursor')
    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)
    
    track_ids = [track.track_id for track in services.get_tracks(repo.repo_instance)]  # type: ignore
    tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page],repo.repo_instance)  # type: ignore

    first_track_url = None
    last_track_url = None
    next_track_url = None
    prev_track_url = None

    if cursor > 0:
        prev_track_url = url_for('content_bp.tracks', cursor=cursor - tracks_per_page)
        first_track_url = url_for('content_bp.tracks')
    if cursor + tracks_per_page < len(track_ids):
        next_track_url = url_for('content_bp.tracks', cursor=cursor + tracks_per_page)

        last_cursor = tracks_per_page * int(len(track_ids) / tracks_per_page)
        if len(track_ids) % tracks_per_page == 0:
            last_cursor -= tracks_per_page
        last_track_url = url_for('content_bp.tracks',cursor=last_cursor)

    return render_template(
        'content/tracklist.html',
        tracks = tracks,
        selected_tracks=utilities.get_selected_tracks(),
        first_track_url=first_track_url,
        last_track_url=last_track_url,
        prev_track_url=prev_track_url,
        next_track_url=next_track_url,
    )

@content_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        trackslist = None
        if services.get_tracks_by_album(form.keyword.data,repo.repo_instance) != []:  # type: ignore
            trackslist = services.get_tracks_by_album(form.keyword.data,repo.repo_instance)  # type: ignore

        if services.get_tracks_by_artist(form.keyword.data,repo.repo_instance) != []:  # type: ignore
            trackslist=services.get_tracks_by_artist(form.keyword.data,repo.repo_instance)  # type: ignore

        if services.get_tracks_by_genre(form.keyword.data,repo.repo_instance) != []:  # type: ignore
            trackslist = services.get_tracks_by_genre(form.keyword.data,repo.repo_instance)  # type: ignore

        if services.get_tracks_by_name(form.keyword.data,repo.repo_instance) != []: # type: ignore
            trackslist = services.get_tracks_by_name(form.keyword.data, repo.repo_instance) # type: ignore

        return render_template(
            'content/tracks.html',
            tracks = trackslist,
            selected_tracks=utilities.get_selected_tracks()
        )
    else:
        return render_template(
            'content/search.html',
            form=form,
            handler_url=url_for("content_bp.search"),
            selected_tracks=utilities.get_selected_tracks()
            )

class SearchForm(FlaskForm):
    # Task 2: Define the variables below using IntegerField and SubmitField
    keyword = StringField("Enter an keyword", [DataRequired()])
    submit = SubmitField("Search")
