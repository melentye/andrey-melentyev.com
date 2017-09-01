FROM continuumio/miniconda3

# Install Python requirements
COPY requirements.txt /
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["--version"]
