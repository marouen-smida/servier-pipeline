FROM astrocrpublic.azurecr.io/runtime:3.0-10

# Work with the actual Astro home
ENV AIRFLOW_HOME=/usr/local/airflow

# Become root to create and chown
USER root
RUN mkdir -p ${AIRFLOW_HOME}/data/intermediary \
    && mkdir -p ${AIRFLOW_HOME}/data/processed \
    # 50000 is typical airflow user; Astro images also use a non-root user
    && chown -R 50000:0 ${AIRFLOW_HOME}/data \
    && chmod -R g+rwX ${AIRFLOW_HOME}/data

# Drop back to the airflow user (Astro’s non-root user)
USER astro
