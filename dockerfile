
FROM python:3.8-buster
 
WORKDIR /usr/src/app/CovidDataProvider

RUN pip install --upgrade pip && apt-get update && apt-get -y install cron

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

#RUN pip install schedule
#RUN apt-get update && apt-get -y install cron
#RUN chmod 0644 ./crontab_daily
RUN touch /var/log/cron.log

# copy files required for the app to run
COPY ./ /usr/src/app/CovidDataProvider/
#COPY templates/index.html /usr/src/app/templates/

ENV PYTHONPATH /usr/src/app



# tell the port number the container should expose
EXPOSE 5000


# run the application
#CMD ["python", "/usr/src/app/CovidDataProvider/Scripts/ETL/FullLoad.py","/usr/src/app/CovidDataProvider/Scripts/API/app.py" ,"/usr/src/app/CovidDataProvider/TestAPI/RunTestCases.py"]

#CMD ["python3", "/usr/src/app/CovidDataProvider/TestAPI/RunTestCases.py"]

CMD ["sh", "/usr/src/app/CovidDataProvider/main.sh"]

#RUN python /usr/src/app/CovidDataProvider/Scripts/ETL/FullLoad.py

#RUN crontab crontab

#CMD ["crond", "-f"]
