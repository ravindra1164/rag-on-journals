# syntax=docker/dockerfile:1
FROM python:3.13.2
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["fastmcp", "run", "mcp/server/server.py"]