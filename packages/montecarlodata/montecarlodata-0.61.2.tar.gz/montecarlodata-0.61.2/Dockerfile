FROM python:3.8.6

# for caching dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /cli
RUN make pip-install -C /cli

ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["montecarlo"]