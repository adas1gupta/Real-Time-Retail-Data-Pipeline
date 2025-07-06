FROM bitnami/spark:3.5.0
USER root
RUN install_packages python3-pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY job.py /opt/spark-apps/job.py
ENV SPARK_APPLICATION_PYTHON_LOCATION=/opt/spark-apps/job.py
CMD ["/opt/bitnami/scripts/spark/run.sh"]