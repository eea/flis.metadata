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
COPY flis_metadata/server/local_settings.py.example flis_metadata/server/local_settings.py
RUN ./manage.py collectstatic --noinput

# Expose needed port
EXPOSE 8004

# Expose static volume
VOLUME /metadata/public/static

#Default command
CMD gunicorn flis_metadata.server.wsgi:application --bind 0.0.0.0:8004

