FROM public.ecr.aws/docker/library/python:3.10

WORKDIR /app

COPY ./src/requirements.txt .
RUN pip install -r requirements.txt

COPY ./src .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]