import os
import requests

from grist.models import RecordsList


def get_records(doc_id: str, table_id: str) -> RecordsList:
    headers = {
        "Authorization": f'Bearer {os.environ["GRIST_API_KEY"]}',
    }
    response = requests.get(
        f"https://docs.getgrist.com/api/docs/{doc_id}/tables/{table_id}/records",
        headers=headers,
    )
    if response.status_code == 200:
        data = response.json()
        return RecordsList(**data)
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def get_table_schema(doc_id: str, table_id: str):
    headers = {
        "Authorization": f'Bearer {os.environ["GRIST_API_KEY"]}',
    }
    response = requests.get(
        f"https://docs.getgrist.com/api/docs/{doc_id}/tables/{table_id}/columns",
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()  # The schema will be in JSON format
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def run_sql_query(doc_id: str, sql_query: str):
    headers = {
        "Authorization": f'Bearer {os.environ["GRIST_API_KEY"]}',
        "Content-Type": "application/json",
    }
    payload = {"sql": sql_query}

    response = requests.post(
        f"https://docs.getgrist.com/api/docs/{doc_id}/sql",
        headers=headers,
        json=payload,
    )
    if response.status_code == 200:
        return response.json()  # The result of the query
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def insert_records(doc_id: str, table_id: str, records: []):
    """
    Insert a record into a specific table in a Grist document.

    :param doc_id: The ID of the Grist document.
    :param table_id: The ID of the table to insert the record into.
    :param record_data: A dictionary containing the fields and their corresponding values to insert.
    :return: Response from the Grist API containing information about the inserted record.
    """
    headers = {
        "Authorization": f'Bearer {os.environ["GRIST_API_KEY"]}',
        "Content-Type": "application/json",
    }

    # Prepare the payload as per the Grist API's required structure
    payload = {"records": [{"fields": record} for record in records]}

    # API request to insert a record
    response = requests.post(
        f"https://docs.getgrist.com/api/docs/{doc_id}/tables/{table_id}/records",
        headers=headers,
        json=payload,
    )

    # Handle the response
    if response.status_code == 200:
        print("Record inserted successfully!")
        return (
            response.json()
        )  # Returning the response, which contains the inserted row IDs
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
