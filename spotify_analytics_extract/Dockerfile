FROM python:3.8.13

ARG HOME=/home

# Update and install system packages
RUN apt-get update -y && \
  apt-get install --no-install-recommends -y -q \
  git libpq-dev python-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN groupadd -g 999 user && useradd -r -u 999 -g user user
WORKDIR ${HOME}

RUN chown -R user:user ${HOME}

USER user

# Install
RUN pip install -U pip

ENV VIRTUAL_ENV=${HOME}/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install google-cloud==0.34.0
RUN pip install google-cloud-storage==2.12.0
RUN pip install python-dotenv==1.0.0
RUN pip install pandas

COPY --chown=user:user ./spotify_analytics_extract/script ${HOME}
