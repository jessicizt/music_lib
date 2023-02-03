from flask import Blueprint, request, render_template, redirect, url_for, session

import music.adapters.repository as repo
import music.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)

def get_selected_tracks(quantity=8):
    tracks = services.get_random_tracks(quantity, repo.repo_instance)  # type: ignore

    return tracks