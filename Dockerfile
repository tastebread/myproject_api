#Base Image
FROM python:3.10

# set work directory
WORKDIR /app

#INSTALL dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

#Copy project file
COPY . .

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0.:8000"]