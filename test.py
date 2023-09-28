import time
import sys
from PyChromeDevTools import ChromeInterface
from bs4 import BeautifulSoup

def printError(e):
    error_type = type(e).__name__
    line_number = sys.exclsc_info()[-1].tb_lineno
    if e.args:
        error_name = e.args[0]
    else:
        error_name = "No additional information available"
    
    error_msg = f"Error Type: {error_type}\nError Name: {error_name}\nLine where error occurred: {line_number}"
    print(error_msg)


try:
    url = 'https://veri.bet/simulator'
    chrome = ChromeInterface(host='localhost',port=9222)
    chrome.Network.enable()
    chrome.Page.enable()

    tab_info = chrome.get_tabs()

    start_time=time.time()
    return_value, messages = chrome.Page.navigate(url=url)
    value = chrome.wait_event("Network.responseReceived", timeout=60)

    chrome.wait_event("Page.loadEventFired", timeout=5)
    end_time=time.time()
    
    print ("Page Loading Time:", end_time-start_time)

    button_selector = 'body > div:nth-child(5) > div > div > div:nth-child(1) > div > a'
    chrome.Runtime.evaluate(expression=f"document.querySelector('{button_selector}').click()")
    value = chrome.wait_event("Network.responseReceived", timeout=60)

    time.sleep(5)

    today_button_selector = 'body > div.container > div > div > div.cover-container.d-flex.mx-auto.flex-column > div > div:nth-child(2) > form > div > label > a:nth-child(3)'
    chrome.Runtime.evaluate(expression=f"document.querySelector('{today_button_selector}').click()")

    time.sleep(5)
    nfl_selector = 'today_button_selector'
    chrome.Runtime.evaluate(expression=f"document.querySelector('{nfl_selector}').click()")

    value = chrome.wait_event("Network.responseReceived", timeout=60)

    requestID = value[0]['params']['requestId']
    responses = chrome.Network.getResponseBody(requestId=requestID)
    soup = BeautifulSoup(responses[0]['result']['body'])

    print(soup)
except Exception as e:
    printError(e)

data = []
for table_index in range(2,45):
    for col_index in range(1,3):
        selector = f'#odds-picks > tbody > tr:nth-child({table_index}) > td > div > div > div > div:nth-child({col_index}) > div > div > div > div > table'
        try:
            team = {}
            table = soup.select_one(selector)
            
            row = table.select_one('tr:nth-of-type(2)')
            team_ = row.find_all('table')[0].text.strip('\n')
            price_ = row.find_all('table')[2].text.strip('\n').replace('\t','')
            spread = row.find_all('table')[3].text.replace('\t','').strip().split('\n')
            total_ = row.find_all('table')[4].text.replace('\t','').strip().split('\n')


            team['team1'] = [team_,price_,spread,total_]

            row = table.select_one('tr:nth-of-type(3)')
            team_ = row.find_all('table')[0].text.strip('\n')
            price_ = row.find_all('table')[2].text.strip('\n').replace('\t','')
            spread = row.find_all('table')[3].text.replace('\t','').strip().split('\n')
            total_ = row.find_all('table')[4].text.replace('\t','').strip().split('\n')

            team['team2'] = [team_,price_,spread,total_]

            data.append(team)
        
        except:
            continue
