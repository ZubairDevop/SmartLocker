CGI Smart Locker - Overview

CGI Smart Locker is a secure Flask web application designed to automate the laptop replacement process for employees whose devices have become damaged or unusable.
The system allows users to request a replacement laptop while enabling administrators to manage laptop inventory, locker cells, replacement requests and user records through a secure web interface.
The project was developed using Python, Flask, SQLite and DevOps practices including GitHub Actions, automated testing and cloud deployment on Render.


Instructions to run application

To run SmartLocker application on local machine one will need IDE (Integrated Development Environment) such as Microsoft visual code and Python 3.13 or higher is required once installed create a virtual environment by using terminal within VS code and run script within the SmartLocker folder.

Create Virtual Environment
python -m venv venv

Activate Environment
venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Create Database
python seed.py

Run Application
python run.py

Application URL:
http://127.0.0.1:5000

requirements.txt file once executed to install all packages run command python seed_data.py to create and dump tables in DB

after this run application by command flask run. This will lunch application and gives out link for browser to open web application and in most cases  it will http://127.0.0.1:5000

this application has 29 standard users and 6 admin embedded in DB. All account can be accessed with emails and password.

Password = Password123! (passwords are kept same for easy access)

Admin Email:
zubaira123@cgi.com
clared123@cgi.com
brianc123@cgi.com
traceyb123@cgi.com
uzaira123@cgi.com
clarkk123@cgi.com


User Email:
stever123@cgi.com
bruceb123@cgi.com
natashar123@cgi.com
peterp123@cgi.com
barrya123@cgi.com
halj123@cgi.com
arthurc123@cgi.com
victors123@cgi.com
loisl123@cgi.com
selinak123@cgi.com
barbarag123@cgi.com
dickg123@cgi.com
katek123@cgi.com
johns123@cgi.com
billyb123@cgi.com
karad123@cgi.com
loganh123@cgi.com
jeang123@cgi.com
scottl123@cgi.com
wandam123@cgi.com
vision123@cgi.com
samw123@cgi.com
buckyb123@cgi.com
carold123@cgi.com
mattm123@cgi.com
frankc123@cgi.com
ororom123@cgi.com
lexl123@cgi.com
clintb123@cgi.com
emmaf123@cgi.com

Note:
These are only predefined users and admins, there no registration form so cannot register new user or admin because this service is for only existing employees.

app is host via Render and can be found on https://smartlocker-fb15.onrender.com
GitHub Repository - https://github.com/ZubairDevop/SmartLocker.git

Author
Zubair Ahmad
BSc (Hons) Digital and Technology Solutions
CGI UK
Level 6 Software Engineering & DevOps Project
2026




Have Fun :)