"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

ANIMALS = ["Dog", "Cat", "Horse", "Pig"]

@action('setup')
@action.uses(db)
def setup():
    """This simply sets up the db content for a small example."""
    db(db.animal).delete()
    for a in ANIMALS:
        db.animal.insert(animal_name=a)
    return "ok"

@action('index')
@action.uses(db, auth, 'index.html')
def index():
    return dict(
        get_animals_url = URL('get_animals', signer=url_signer),
    )

@action('get_animals')
@action.uses(db)
def get_animals():
    rows = db(db.animal).select().as_list()
    return dict(animals=rows)

@action('show_animal/<animal_id:int>')
@action.uses(db, url_signer.verify(), "show_animal.html")
def show_animal(animal_id=None):
    a = db(db.animal.id == animal_id).select().first()
    return dict(name=("Not found" if a is None else a.animal_name))
