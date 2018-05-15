FROM pypy:3

# Set the working directory
WORKDIR /pseudol10napp

# Copy the files
COPY requirements.txt /pseudol10napp/

COPY app.py /pseudol10napp/

# Run pip to install the required packages
RUN pip install --no-cache-dir --trusted-host=pypi.python.org -r requirements.txt

# Unblock the default port for Flask
EXPOSE 5000

# Start the Flask app
ENTRYPOINT ["pypy3", "app.py"]
