FROM eeacms/python:2.7-slim

# Copy code into image
RUN mkdir metadata
COPY requirements.txt requirements-dev.txt requirements-dep.txt /metadata/
WORKDIR metadata

# Install requirements
RUN pip install -U setuptools
RUN pip install -r requirements-dep.txt

# Copy code
COPY . /metadata
RUN ./manage.py migrate \
  && ./manage.py loadfixtures \
  && ./manage.py load_metadata_fixtures \
  && ./manage.py collectstatic --noinput
COPY flis_metadata/server/local_settings.py.docker flis_metadata/server/local_settings.py

# Expose needed port
EXPOSE 8000

# Expose static volume
VOLUME /metadata/public/static

#Default command
CMD gunicorn flis_metadata.server.wsgi:application --bind 0.0.0.0:8000
