FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Convert Windows CRLF to Linux LF and make executable
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

CMD ["sh", "start.sh"]
