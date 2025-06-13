# Step 1: Use a base Python image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file into the container
COPY requirements.txt .

# Step 4: Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the entire application into the container
COPY . .

# Step 6: Expose the port that Flask will run on
EXPOSE 5000

# Step 7: Set the environment variable to production mode
ENV FLASK_ENV=production

# Step 8: Command to run the Flask app when the container starts
CMD ["python", "app.py"]
