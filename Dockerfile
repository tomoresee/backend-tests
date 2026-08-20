FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.zip \
    && unzip allure-2.29.0.zip -d /opt/ \
    && rm allure-2.29.0.zip \
    && ln -s /opt/allure-2.29.0/bin/allure /usr/local/bin/allure

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/allure-results /app/allure-report

COPY . .

CMD ["pytest", "tests/", "--alluredir=/app/allure-results"]