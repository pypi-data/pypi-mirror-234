from pathlib import Path

import pytest

from turbofan.database import Database, Session


@pytest.fixture
def tmp_db_session(tmp_path: Path, monkeypatch):
    """
    Creates a database in the path defined by tmpdir and loads all sql files
    from the migrations folder in the project root.
    """

    # Since Database defines that the environment variable has priority over
    # all other definitions, we set it here, so during the tests, all the
    # database instances use this value for the path.
    monkeypatch.setenv("DATABASE", str(tmp_path))

    db = Database()
    for f in Path("migrations").glob("*.sql"):
        db.run_sql_file(f)

    with Session(db.engine) as session:
        yield session
