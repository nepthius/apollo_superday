import pytest

from app import create_app


@pytest.fixture()
def app():

    #creates app with testing config
    app, db, migrate = create_app({
        "TESTING": True, 
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", 
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()
    
    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

