import pytest

from toolcat.database import Database, OperationalError, Session, text
from toolcat.files import append


class TestDatabase:
    def test_should_raise_a_key_error_when_environment_variable_is_not_defined(self):
        with pytest.raises(KeyError):
            _ = Database()

    def test_create_database_file_in_path_defined_by_environment_variable(
        self, tmpdir, monkeypatch
    ):
        database = tmpdir / "database_file_by_env.db"
        monkeypatch.setenv("DATABASE", str(database))

        _ = Database()

        assert database.exists()  # nosec

    def test_remove_the_database_file_when_remove_is_called(self, tmp_path):
        database_file = tmp_path / "database"
        db = Database(database_file)

        db.remove()

        database_file = tmp_path / "database.db"
        assert not database_file.exists()  # nosec


class TestDatabaseCreateWithSqlFile:
    def test_raise_custom_error_when_an_error_happens(self, tmp_path):
        sql_file = tmp_path / "sql_file.sql"
        sql_file.write_text("")

        database = Database(tmp_path, sql_file=sql_file)

        sql_stmt = "SELECT * FROM test_table;"

        with Session(database.engine) as session:
            with pytest.raises(OperationalError) as excinfo:
                session.execute(text(sql_stmt))

        assert "execute sql statement" in excinfo.value.args[0]  # nosec

    def test_create_database_given_initial_sql_file(self, tmp_path):
        sql_file = tmp_path / "sql_file.sql"
        sql_file.write_text("CREATE TABLE test_table (id INTEGER PRIMARY KEY);")

        database = Database(tmp_path, sql_file=sql_file)

        sql_stmt = "SELECT * FROM test_table;"
        with Session(database.engine) as session:
            result = session.execute(text(sql_stmt))
        assert result.fetchall() == []  # nosec

    def test_execute_multiple_sql_statements(self, tmp_path):
        sql_file = tmp_path / "sql_file.sql"
        sql_file.write_text("CREATE TABLE test_table (id INTEGER PRIMARY KEY);")
        append(sql_file, "CREATE TABLE test_table2 (id INTEGER PRIMARY KEY);")

        database = Database(tmp_path, sql_file=sql_file)

        sql_stmt = "SELECT * FROM test_table2;"
        with Session(database.engine) as session:
            result = session.execute(text(sql_stmt))
        assert result.fetchall() == []  # nosec
