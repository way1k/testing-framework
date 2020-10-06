import pytest

from pages.action_layers.instagram_profile import ProfileInstAction
from pages.page_objects.instagram_login import LoginInstPage
from pages.action_layers.instagram_login import LoginInstAction
from pages.page_objects.instagram_profile import ProfileInstPage
# from pages.action_layers.instagram_login import do_login


# insert you email here
LOGIN = 'kek'

# insert you password here
PASSWORD = 'kek'
SEARCH = 'emiliasoko.love'


def test_like(inst):
    LoginInstPage(inst).open().do_login(LOGIN, PASSWORD)
    profile = ProfileInstPage(inst)
    profile.do_search(SEARCH)
    profile.likes()

    assert profile.is_like_exist()
    profile.unlike()
    assert profile.is_unlike_exist()


def test_login(inst_app):
    LoginInstAction(inst_app).open().do_login(LOGIN, PASSWORD)
    ProfileInstAction(inst_app).check_exist_home_button()


