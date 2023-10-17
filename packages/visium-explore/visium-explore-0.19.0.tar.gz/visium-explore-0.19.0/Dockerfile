FROM python:3.9

WORKDIR /app

RUN pip install pipenv

COPY . .

RUN pipenv install --system --deploy

ENV STREAMLIT_SERVER_PORT=8080

CMD ["bash", "init.sh"]