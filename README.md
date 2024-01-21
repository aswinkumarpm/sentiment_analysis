sentiment_analysis

![image](https://github.com/aswinkumarpm/sentiment_analysis/assets/40489823/876a11de-6641-49fb-8562-d68f2618cdc8)

Steps

1. sudo apt-get update
2. sudo apt install python3-pip -y
3. sudo apt install python3.10-venv
3. git clone https://github.com/aswinkumarpm/sentiment_analysis.git
4. go to folder sentiment_analysis which is cloned now
5. create a virtual env for python3. I have created with python3.10   using the command python3.10 -m venv .venv 
6. source .venv/bin/activate
7. install the requirements transformers, django, tensorflow, torch using the command --  pip install -r requirements.txt
8. pushed my db for testing purposes
9. other wise , need to connect other databases,  please remove the database and create makemigrations and migrate . Also inorder to connect your db do the changes in settings.py


This is the AWS hosted URL 
   http://51.20.43.120:8000/
