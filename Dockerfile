FROM python:3.8
RUN mkdir -p /usr/src/fault_plot
WORKDIR /usr/src/fault_plot
COPY . /usr/src/fault_plot
RUN python3 -m pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3"]
CMD ["fast.py"]