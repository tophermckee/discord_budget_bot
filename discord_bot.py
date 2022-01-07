import json, requests, gspread, datetime

def return_spreadsheet_values(spreadsheet_name, sheet_name, range=""):
    from oauth2client.service_account import ServiceAccountCredentials
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('secrets.json', scope)
    client = gspread.authorize(creds)
    if range != '':
        return client.open(spreadsheet_name).worksheet(sheet_name).get(range)
    else:
        return client.open(spreadsheet_name).worksheet(sheet_name).get_all_values()

def return_spreadsheet(spreadsheet_name, sheet_name):
    from oauth2client.service_account import ServiceAccountCredentials
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('secrets.json', scope)
    client = gspread.authorize(creds)
    return client.open(spreadsheet_name).worksheet(sheet_name)

with open('secrets.json') as file:
    credentials = json.load(file)

def post_messsage_to_discord(message=''):
    if message == '':
        message = 'hello world'

    discord_url = credentials['webhook_url']
    payload = {'content': message}

    params = {
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        'method': "POST",
        'payload': payload,
        'muteHttpExceptions': True
    }

    response = requests.post(url=discord_url, params=params, data=payload)

output = f"`{'-' * len(datetime.datetime.now().strftime('%a, %b %y %I:%M %p'))}\n{datetime.datetime.now().strftime('%a, %b %y %I:%M %p')}\n{'-' * len(datetime.datetime.now().strftime('%a, %b %y %I:%M %p'))}`\n"
budget = 150

if datetime.datetime.now().hour < 12 and datetime.datetime.today().weekday() == 6: # if it's sunday before noon, clear the spreadsheet
    print('time to reset the spreadsheet\n')
    return_spreadsheet('NOLA LOIF', 'Weekly Spending').batch_clear([f"A3:B16"])
else:
    print('it is not time to clear the spreadsheet\n')

for row in return_spreadsheet_values('NOLA LOIF', 'Weekly Spending', 'A3:B'):
    output += f"\n{row[0]} - {row[1]}"
    budget -= int(row[1].replace('$', ''))

output += f"\n\nWe have ${budget} left this week."

post_messsage_to_discord(output)