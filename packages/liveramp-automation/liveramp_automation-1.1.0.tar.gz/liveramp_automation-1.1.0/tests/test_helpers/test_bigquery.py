from liveramp_automation.helpers.bigquery import BigQueryConnector

project_id = "liveramp-eng-qa-reliability"
dataset_id = "liveramp_automation_test"
table_name = "test_table"
connector = BigQueryConnector(project_id, dataset_id)
sql_query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_name}` where age > 1;"
output_csv_path = "tests/test_helpers/test.csv"
bucket_name = "liveramp_automation_test"
source_blob_name = "Unit/test.csv"


def test_connect():
    result = connector.connect()
    assert result == 0


def test_query():
    result = connector.query(sql_query)
    if result:
        for row in result:
            print(row)
    assert result


def test_query_rows():
    result = connector.query_rows(sql_query)
    assert result


def test_query_export():
    result = connector.query_export(sql_query, output_csv_path)
    assert result == 0


def test_dataset_tables():
    result = connector.dataset_tables()
    assert result


def test_insert_from_bucket():
    result = connector.insert_from_bucket(bucket_name, source_blob_name, table_name)
    assert result
