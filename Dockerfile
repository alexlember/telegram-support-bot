FROM python:latest


#Labels as key value pair
LABEL Maintainer="alexlember"


# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY bot.py ./
COPY help_cmd_handler.py ./
COPY need_help.py ./
COPY ready_to_help.py ./
COPY settings.py ./
COPY storage.py ./
COPY sql/ ./sql/

COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh