import logging

from ns_asphalt9.core import consts
from ns_asphalt9.core.page_factory import factory


def test_page():
    cases = [
        (
            """MULTIPLAYER  Race to victory and prove that you  ave the best chance to win  NEW EXCLUSIVE CARS!  NEW MULTIPLAYER SERIES  COMING SOON  :  =  =  ae  88  Te  EVENTS. PLAYER, CLUB. , RACE. SCREEN. CAREER  == Shop  el= Settings  (QQ Tabs  © Chat  @ Select  © Back""",  # noqa: E501
            consts.no_mp,
        )
    ]

    for case in cases:
        text, result = case
        page = factory.create_page(text)
        logging.info(page.name)
        assert page.name == result
