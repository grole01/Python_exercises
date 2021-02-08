import requests
import pandas as pd

#cookies = {
#    'BIGipServerdirectory.ntschools.net_443.app~directory.ntschools.net_443_pool': '360972810.20480.0000',
#}

def school_code():
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'Accept': 'application/json',
        'X-Requested-With': 'Fetch',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://directory.ntschools.net/',
        'Accept-Language': 'hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    response = requests.get('https://directory.ntschools.net/api/System/GetAllSchools', headers=headers) #cookies=cookies)

    json_response=response.json()
    return json_response


    #print(len(json_response))

    #for school in json_response:
    #    return  school['itSchoolCode']

school_code=school_code()





#code=[i['itSchoolCode']for i in school_code ]

#ad_Id=123
#print(f'{ad_Id}')

#def get_school(code):
def get_school(i):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '^\\^Google',
        'Accept': 'application/json',
        'X-Requested-With': 'Fetch',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://directory.ntschools.net/',
        'Accept-Language': 'hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('itSchoolCode',  f'{i}'),
    )
    #print(f'{code}')

    response = requests.get('https://directory.ntschools.net/api/System/GetSchool', headers=headers, params=params)#, cookies=cookies)
    #print(response.status_code)
    return  response.json()
        #print(data)

        #school_data={

        #"Name :": data['name'],
        #"Adress :": data['physicalAddress']['displayAddress'],
        #"Phone :" : data['telephoneNumber']}

        #print( school_data)

get_school_list=[]

for i in school_code[0:5]:
    code=i['itSchoolCode']
    #print(code)

    get_school_list.append(get_school(code))#
data_=[]
for data in get_school_list:
    school_data={

    "Name ": data['name'],
    "Adress ": data['physicalAddress']['displayAddress'],
    "Phone " : data['telephoneNumber']}

    #print( school_data)
    data_.append(school_data)

df=pd.DataFrame(data_)
print(df)

#get_school()