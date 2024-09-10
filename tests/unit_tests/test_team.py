from sqlalchemy import Select, select, func

from models import Team


def test_team_created(session):
    assert session.scalar(select(func.count()).select_from(Team)) == 3

def test_teams_name(session):
    team_names = session.scalars(select(Team.name)).all()
    assert "Management team" in team_names
    assert "Sales team" in team_names
    assert "Support team" in team_names
