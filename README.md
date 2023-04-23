# Salary search

The script counts approximate average salary for 8 most popular programming languages. Script uses HeadHunter and SuperJob data about vacancies.

### How to install

To use se script you need to get SuperJob API token. Go [here](https://api.superjob.ru/), get an account and generate your personal token.

This token you should put to a ```'.env'``` file. Create the file in the directory where ``main.py`` located. Put this to the ``.env`` file:
```
SUPERJOB_TOKEN='Put_here_your_token'
```

Python3 should already be installed. 
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Start script
To execute script use terminal. Execute this command from the project directory:
```
python main.py
```
Firstly it will inform you of data downloading process. Then it will show two tables with data about average salary and numbers of vacancies found on mentioned sites.

### Project Goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).