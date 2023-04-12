# Using lightweight alpine image
FROM python:3.9.13

# Installing packages
RUN pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh .env app.py ./
COPY database ./database
COPY resources ./resources
COPY services ./services
COPY templates ./templates
COPY tests ./tests

# Install API dependencies
RUN pipenv install --system --deploy

# Start app
EXPOSE 3000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
