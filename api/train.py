import requests
import re
from g4f.client import Client
client = Client()
def searchProvince():
    response2 = requests.get('http://localhost:8888/api/v1/locations/p')
    data2 = response2.json()
    dataJobFull2 = ""
    for i in data2['data']:
        dataJobFull2 = dataJobFull2 + i['full_name'] + ' với mã ID' +i['id'] +',\n'
    return "'"+ dataJobFull2 + "'"

def searchDistrict(id):
    response2 = requests.get('http://localhost:8888/api/v1/locations/d?pid='+str(id))
    data2 = response2.json()
    dataJobFull2 = ""
    for i in data2['data']:
        dataJobFull2 = dataJobFull2 + i['full_name'] + ' với mã ID' +i['id'] +',\n'
    return dataJobFull2
    

def searchWard(id):
    response2 = requests.get('http://localhost:8888/api/v1/locations/w?did='+id)
    data2 = response2.json()
    dataJobFull2 = ""
    for i in data2['data']:
        dataJobFull2 = dataJobFull2 + i['full_name'] + ' với mã ID' +i['id'] +',\n'
    return dataJobFull2

def searchJobs():
    file = open("api/data/nganh.txt", "r", encoding='utf-8')
    nganh = file.read()
    return nganh

def searchJobFit(content):
    nganh = searchJobs()
    nganh = "'"+ nganh + "'"
    req = content
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": 'Đây là các ngành của công ty tôi: '+ nganh +' .Hãy cho tôi biết mô tả sau hợp với ngành nào chỉ cần ghi mỗi số id của ngành đúng nhất không cần ghi gì ngoài id:' +req}],
    )
    pattern = r'\d+'
    match = re.search(pattern, response.choices[0].message.content)
    if match:
        number = match.group()
        return number

def searchVitri(content):
    dataProvince = searchProvince()
    contentData = re.sub(r'\d+', '', content)
    string = ""
    while True: 
        response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": 'Hãy cho tôi biết mô tả địa chỉ sau:' +contentData + '\n' +'thuộc mã nào sau đây và bạn chỉ cần trả lời là mã gì: '+ dataProvince +'\n'}],
        )
        string = response.choices[0].message.content
        if(string):
            break
    pattern = r'\d+'
    match = re.search(pattern, string)
    print(string)
    if match:
        number = match.group()
        string2 = ""
        district = searchDistrict(number)
        while True: 
            response2 = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": 'Hãy cho tôi biết mô tả địa chỉ sau:' +contentData + '\n' +'thuộc mã nào sau đây và bạn chỉ cần trả lời là mã gì: '+ district +'\n'}],
            )
            string2 = response2.choices[0].message.content
            if(string2):
                break;
        print(string2)
        match2 = re.search(pattern, string2)
        if match2:
            number2 = match2.group()
            string3 = ""
            ward = searchWard(number2)
            while True:
                response3 = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": 'Hãy cho tôi biết mô tả địa chỉ sau:' +contentData + '\n' +'thuộc mã nào sau đây và bạn chỉ cần trả lời là mã gì: '+ ward +'\n'}],
                )
                string3 = response3.choices[0].message.content
                if(string3):
                    break;
            print(string3)
            match3 = re.search(pattern, string3)
            if( match3):
                number3 = match3.group()
                print(number,number2,number3)
                return number3 or number2 or number




# text = dataJobFull2
# file = open("diachi.txt", "w", encoding='utf-8')
# file.write(text)
# file.close()