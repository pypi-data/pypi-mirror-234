ARG PYTHON_VERSION=3.11-slim-bullseye
FROM python:${PYTHON_VERSION}
ARG APP_HOME=/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR ${APP_HOME}
COPY ./requirements.txt ${APP_HOME}/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . ${APP_HOME}
#CMD ["uvicorn", "spendpoint.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
CMD ["python3", "-m", "spendpoint"]
