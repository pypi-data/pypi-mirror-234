from toolcat.database import text


def test_tmp_db_session_loads_multiple_sql_files(tmp_db_session):
    sql_stmt = "SELECT * FROM test_table1;"
    result = tmp_db_session.execute(text(sql_stmt))
    assert result.fetchall() == []  # nosec

    sql_stmt = "SELECT * FROM test_table2;"
    result = tmp_db_session.execute(text(sql_stmt))
    assert result.fetchall() == []  # nosec
