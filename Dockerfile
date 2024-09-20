# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy pyproject.toml, uv.lock, and README.md (if present)
COPY pyproject.toml uv.lock README.md /app/

# Install dependencies using uv with the --locked flag
RUN uv sync --locked

# Copy the rest of the application code
COPY . /app

# Set the command to run the jobs.py script using uv
CMD ["uv", "run", "python", "worker.py"]
