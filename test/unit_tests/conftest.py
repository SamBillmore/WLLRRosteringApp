import pytest

from user_interface.app_container import App

SCOPE = "session"


@pytest.fixture(scope=SCOPE)
def app():
    app = App()
    yield app
