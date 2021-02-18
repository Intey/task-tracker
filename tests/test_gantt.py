from uuid import uuid4

import pytest

from jira_proxy.entities import Gantt, Issue, User
from tests.exceptions import LogicError


def issue(estimation: int, skill=None):
    return Issue(
        key=uuid4().hex[:7],
        summary="",
        description="",
        estimation_hours=estimation,
        skill=skill,
    )


def test_fullfill_one():
    one = User(nick="one", skill="f", workdays_hours=[8, 8, 8, 8, 8, 0, 0])
    i1 = issue(2, skill="f")
    i2 = issue(2, skill="f")
    gnt = Gantt(
        from_date="2020-01-01", to_date="2020-01-30", team=[one], issues=[i1, i2],
    )
    plan = gnt.fullfill()
    assert plan.user_tasks[one] == {i1, i2}


def test_fullfill_concurrent_run():
    one = User(nick="one", skill="f", workdays_hours=[8, 8, 8, 8, 8, 0, 0])
    two = User(nick="two", skill="f", workdays_hours=[8, 8, 8, 8, 8, 0, 0])
    bitch = User(nick="joue", skill="b", workdays_hours=[8, 8, 8, 8, 8, 0, 0])
    i1 = issue(2, skill="f")
    i2 = issue(2, skill="f")
    i3 = issue(4, skill="b")
    gnt = Gantt(
        from_date="2020-01-01",
        to_date="2020-01-30",
        team=[one, two, bitch],
        issues=[i1, i2, i3],
    )
    plan = gnt.fullfill()
    assert plan.user_tasks[one] == {i1}
    assert plan.user_tasks[two] == {i2}
    assert plan.user_tasks[bitch] == {i3}


def test_hasnt_resources():
    one = User(nick="one", skill="f", workdays_hours=[8, 8, 8, 8, 8, 0, 0])
    i1 = issue(2, skill="f")
    i3 = issue(4, skill="b")
    gnt = Gantt(
        from_date="2020-01-01", to_date="2020-01-30", team=[one], issues=[i1, i3],
    )
    plan = gnt.fullfill()
    assert plan.user_tasks[one] == {i1, i3}
