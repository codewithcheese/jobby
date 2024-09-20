import os
from datetime import datetime, timezone

from greenhouse.models import GreenhouseDepartmentsResponse
from greenhouse.api import get_greenhouse_jobs
from grist.api import run_sql_query, get_table_schema, insert_records


# Query to check for existing jobs using RefId column
def check_existing_jobs(doc_id: str, company_id: str, ref_ids: list):
    ref_ids_str = ",".join(
        [f"'{ref_id}'" for ref_id in ref_ids]
    )  # Format IDs for SQL query
    check_query = f"""
    SELECT RefId FROM Job
    WHERE Company = {company_id} AND RefId IN ({ref_ids_str}) 
    """
    result = run_sql_query(doc_id, check_query)
    existing_ref_ids = [
        record["fields"]["RefId"] for record in result.get("records", [])
    ]
    return set(existing_ref_ids)


jobsite_query = """
    SELECT
        Jobsite.id AS jobsite_id,
        Jobsite.ClientId as client_id,
        Company.id AS company_id,
        Company.Name AS company_name,
        Company.Website AS company_website,
        Provider.Name AS provider_name        
    FROM Jobsite
    JOIN Company ON Jobsite.Company = Company.id
    JOIN Provider ON Jobsite.Provider = Provider.id    
"""

# WHERE Jobsite.ClientId = 'anthropic'

# Run the query
doc_id = os.environ["GRIST_DOC_ID"]
result = run_sql_query(doc_id, jobsite_query)


def insert_greenhouse_jobs(
    doc_id: str,
    company_id: str,
    response: GreenhouseDepartmentsResponse,
):
    """
    Insert Greenhouse jobs into the Grist Job table if they do not already exist.

    :param doc_id: The ID of the Grist document.
    :param company_id: The ID of the company to associate with the job.
    :param response: The Greenhouse API response containing job details.
    """
    jobs_to_insert = []
    ref_ids_to_check = [
        job.id for department in response.departments for job in department.jobs
    ]

    # Query to check for existing jobs using RefId
    existing_jobs = check_existing_jobs(doc_id, company_id, ref_ids_to_check)

    for department in response.departments:
        for job in department.jobs:
            # Only insert if job's RefId is not already present in the existing jobs
            if job.id not in existing_jobs:
                job_data = {
                    "RefId": job.id,
                    "Company": company_id,
                    "Title": job.title,
                    "Location": job.location.name,
                    "Department": department.name,
                    "CreatedAt": datetime.now(timezone.utc).isoformat(),
                }
                jobs_to_insert.append(job_data)

    # Insert only the new records
    if jobs_to_insert:
        insert_records(doc_id, "Job", jobs_to_insert)  # Insert multiple records at once
        return jobs_to_insert
    else:
        return []


for row in result["records"]:
    try:
        fields = row["fields"]
        if fields["provider_name"] == "Greenhouse":
            greenhouse_response = get_greenhouse_jobs(fields["client_id"])
            inserted = insert_greenhouse_jobs(
                doc_id,
                fields["company_id"],
                greenhouse_response,
            )
            insert_records(
                doc_id,
                "Run",
                [
                    {
                        "CreatedAt": datetime.now(timezone.utc).isoformat(),
                        "Status": "Success",
                        "Message": f"Inserted {len(inserted)} {fields['company_name']} jobs.",
                    }
                ],
            )
    except Exception as e:
        insert_records(
            doc_id,
            "Run",
            [
                {
                    "CreatedAt": datetime.now(timezone.utc).isoformat(),
                    "Status": "Error",
                    "Message": str(e),
                }
            ],
        )
