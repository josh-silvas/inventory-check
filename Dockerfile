FROM python:3.9.0

# Fixes a host of encoding-related bugs
ENV LC_ALL=C.UTF-8

# Set us a decent shell prompt
ENV PS1='[\u@\h \W]\$ '

ENV PATH="${PATH}:/home:/home/app"
ENV PYTHONPATH="${PYTHONPATH}:/home"

# Change the working directory to the copied script location
WORKDIR /home/app

# Copy over the scripts
COPY app /home/app
COPY requirements.txt /home/app

# Run python package requirements
RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "main.py"]
