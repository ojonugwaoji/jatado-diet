# 
FROM python:3.10.5

# 

COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app/ api_v1/app

# 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
