# # Dockerfile for Astro-agent API
# FROM registry.ford.com/astro/python-3.11:v7

# WORKDIR /app
# COPY requirements-dockerfile.txt ./requirements.txt
# RUN pip3 install --no-cache-dir -r requirements.txt 
# COPY agents /app/agents
# COPY cookbook /app/cookbook
# COPY agent-api /app/agent-api
# ENV PYTHONPATH="$PYTHONPATH:/app"
# EXPOSE 8080

# CMD ["uvicorn", "agent-api.04_airflow_agent_api:app", "--host", "0.0.0.0", "--port", "8080"]

# #Dockejnujrfile for Streamlit UI APP
FROM python:3.10-slim

ARG http_proxy=http://internet.ford.com:83
ARG https_proxy=http://internet.ford.com:83

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt 

COPY . /app

ENV PYTHONPATH="$PYTHONPATH:/app"

EXPOSE 8501

CMD streamlit run str.py

