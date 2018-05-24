FROM pypy:3

# Set the working directory
WORKDIR /pseudol10napp

# Copy the files
COPY requirements.txt /pseudol10napp/

COPY app.py /pseudol10napp/

COPY static/* /pseudol10napp/static/

COPY templates/* /pseudol10napp/templates/

# Run pip to install the required packages
RUN pip install --no-cache-dir --trusted-host=pypi.python.org -r requirements.txt

# Unblock port 8080
EXPOSE 8080

# Start the web app
ENTRYPOINT ["gunicorn", "--bind=:8080", "app:app"]
