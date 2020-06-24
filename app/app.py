from flask import Flask, request, render_template
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from multiprocessing import Pool
import time

app = Flask(__name__)

title = ''

dates = []
date = datetime.date.today()
end = datetime.date(2021, 2, 1)
date += datetime.timedelta(days=1)
dates.append(date)
count = 2 #for 1,7,7,15,30,30... make count=1
while(date < end):
    if count < 3:
        date += datetime.timedelta(days=7)
    elif count == 3:
        date += datetime.timedelta(days=15)
    else:
        date += datetime.timedelta(days=30)
    count += 1
    if date > end:
    	break
    dates.append(date)
    
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = None
service = None

def login():
    global creds
    global service
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    service = build('calendar', 'v3', credentials=creds)

def addEvent(date = None):
    event = {
        'summary': title,
        'start': {
            'dateTime': date.strftime('%Y-%m-%d')+'T21:00:00',
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': date.strftime('%Y-%m-%d')+'T22:00:00',
            'timeZone': 'Asia/Kolkata',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    
def createEvent():
    print(title)
    p = Pool(10)
    p.map(addEvent,dates)
    p.terminate()
    p.join()

@app.route('/', methods=['GET', 'POST'])
def index():
    global title
    if not creds:
        login()
    if request.method == 'POST':
        title = request.form['topic']
        start = time.time()
        createEvent()
        print(time.time()-start)
        return '<h1>👋 Done!</h1>'
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
