FROM apache/airflow:2.10.3

# Switch to root user to install system packages
USER root

# Update the package list and install Git
RUN apt-get update && apt-get install -y git && apt-get clean

# Switch back to the airflow user
USER airflow

# Copy the Python dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
