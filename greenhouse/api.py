import requests
from pydantic import ValidationError

from greenhouse.models import GreenhouseDepartmentsResponse


def get_greenhouse_jobs(jobsite_id: str) -> GreenhouseDepartmentsResponse:
    """
    Fetch job data from the Greenhouse API for the given jobsite ID and return it parsed into Pydantic models.

    :param jobsite_id: The jobsite ID from the Greenhouse API.
    :return: Parsed response containing departments and jobs in Pydantic model form.
    """
    try:
        # Perform the API request
        url = f"https://boards-api.greenhouse.io/v1/boards/{jobsite_id}/departments"
        print(url)
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the JSON response using Pydantic models
        data = response.json()
        parsed_response = GreenhouseDepartmentsResponse(**data)
        return parsed_response

    except requests.RequestException as e:
        print(f"Error fetching data from Greenhouse: {e}")
        raise
    except ValidationError as ve:
        print(f"Data validation error: {ve}")
        raise
