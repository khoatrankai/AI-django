import requests
import re
import os
# from g4f.client import Client
import google.generativeai as genai
# from .gpt4free.g4f.client import Client
# client = Client()

import unicodedata
def replace_nulls_with_empty_string(obj):
    for key, value in obj.items():
        if value is None:
            obj[key] = ""
    return obj
def remove_vietnamese_accents(text):
    # Chuẩn hóa chuỗi Unicode
    text = unicodedata.normalize('NFD', text)
    
    # Loại bỏ các dấu bằng cách chỉ giữ lại các ký tự không thuộc nhóm combining marks
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    
    # Chuyển về dạng chuẩn
    text = unicodedata.normalize('NFC', text)
    
    return text

def InfosCompany():
    current_file_path = os.path.abspath(__file__)
    data_dir = os.path.dirname(current_file_path)
    path = data_dir+'/data/infoAI.txt'
    file = open(path, "r", encoding='utf-8')
    info = file.read()
    return info.split('\n')

def ChangeDataTxt(link,content):
    with open(link, "w", encoding="utf-8") as fileNew:
      fileNew.write(content)

def fetch_geminiOption(content,listContent):
    # print(listContent)
    genai.configure(api_key="AIzaSyCbe9R6AxyCSp-lhwPNc8ceMYOZv2BYARQ")

    # Set up the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    chat_session = model.start_chat(
        history=listContent
    )
    try:
        response = chat_session.send_message(content)
        return response.text
    except Exception as e:
        return 'Xin lỗi Server AI tạm thời bảo trì...'

# def fetch_geminiFilterCV(content,listContent):
#     # print(listContent)
#     genai.configure(api_key="AIzaSyCMjfpkbb6c75SFOvRD8C2ImMLBA12jssQ")

#     # Set up the model
#     generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 8192,
#     }

#     safety_settings = [
#     {
#         "category": "HARM_CATEGORY_HARASSMENT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#     },
#     {
#         "category": "HARM_CATEGORY_HATE_SPEECH",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#     },
#     {
#         "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#     },
#     {
#         "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#     },
#     ]

#     model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
#                                 generation_config=generation_config,
#                                 safety_settings=safety_settings)

#     chat_session = model.start_chat(
#         history=listContent
#     )

#     response = chat_session.send_message(content)
#     # print(response.text)
#     return(response.text)


def listFileCustomPublic():
    current_file_path = os.path.abspath(__file__)
    data_dir = os.path.dirname(current_file_path)
    # print(data_dir)
    path = data_dir+'/data/CustomPublic'
    txt_files = []
    name_files = []
    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            txt_files.append(os.path.join(path, filename))
            name_files.append(os.path.basename(os.path.join(path, filename).replace(".txt","")))
    return {'pathDir':data_dir,'path':path,'linkFile':txt_files,'nameFile':name_files}

def StartInfoChatPublic():
    infoFile = listFileCustomPublic()
    # regex = r"\d+"
    listInfoFile = infoFile['nameFile']
    
    fileDefault = open(infoFile['pathDir']+"/data/infoAI.txt", "r", encoding='utf-8')
    infoDefault = fileDefault.read()
    idMax = 0
    if len(listInfoFile) != 0:
        numbers = [int(s.replace('custom', '')) for s in listInfoFile]
        max_number = max(numbers)
        # fileIdMax = listInfoFile[len(listInfoFile)-1].replace("custom","")
        # fileIdMax = listInfoFile[0].replace("custom","")
        idMax = max_number +1
    file_path = os.path.join(infoFile['path'], "custom"+str(idMax)+".txt")
    # if not os.path.exists(infoFile['path']):
    #   os.makedirs(infoFile['path'])
    with open(file_path, "w", encoding="utf-8") as fileNew:
      fileNew.write(infoDefault)
    return idMax

def CheckInfoChatPublic(id):
    regex = r"\d+"
    listInfo = listFileCustomPublic()
    # print(listInfo)
    linkFile = ""
    if len(listInfo['nameFile']) != 0:
        for i in range(len(listInfo['nameFile'])):
            match = re.findall(regex,listInfo['nameFile'][i])[0]
            if match == id:
                linkFile = listInfo['linkFile'][i]
                break;
    fileChat = open(linkFile, "r", encoding='utf-8')
    listChatEnding = fileChat.read()
    fileChat.close()
    listChat = listChatEnding.split('\n')
    listHistory = []
    for i in range(len(listChat)):
        if '$$userStart$$' in listChat[i]:
            textContent = listChat[i].replace("$$userStart$$","")
            textContent = textContent.replace("$$userEnd$$","")
            listHistory.append({'role':'user','parts':textContent})
        else:
            textContent = listChat[i].replace("$$modelStart$$","")
            textContent = textContent.replace("$$modelEnd$$","")
            listHistory.append({'role':'model','parts':textContent})

    return {'linkFile':linkFile,'listHistory':listHistory,'fileChatOld':listChatEnding}


def NewChatPublic(id,content):
    infoCheck = CheckInfoChatPublic(id)
    # print(infoCheck)
    # print("chu viet",infoCheck['listHistory'])
    print(content,infoCheck['listHistory'])
    newModel = fetch_geminiOption(content,infoCheck['listHistory'])
    print(newModel)
    newFileContent = infoCheck['fileChatOld'] +'\n' +"$$userStart$$"+content+"$$userEnd$$" +'\n'+ "$$modelStart$$"+newModel.replace("\n","")+"$$modelEnd$$"
    ChangeDataTxt(infoCheck['linkFile'],newFileContent)
    return newModel





def CheckInfoChatID(id):
    infoFile = FindCustomID(id)
    fileChat = open(infoFile['path'], "r", encoding='utf-8')
    listChatEnding = fileChat.read()
    fileChat.close()
    listChat = listChatEnding.split('\n')
    listHistory = []
    for i in listChat:
        if i.find('$$userStart$$') and i.find('$$userEnd$$'):
            textContent = i.replace("$$userStart$$","")
            textContent = textContent.replace("$$userEnd$$","")
            listHistory.append({'role':'user','parts':textContent})
        else:
            textContent = i.replace("$$modelStart$$","")
            textContent = textContent.replace("$$modelEnd$$","")
            listHistory.append({'role':'model','parts':textContent})

    return {'linkFile':infoFile['path'],'listHistory':listHistory,'fileChatOld':listChatEnding}

def FindCustomID(id):
    current_file_path = os.path.abspath(__file__)
    data_dir = os.path.dirname(current_file_path)
    # print(data_dir)
    path = data_dir+'\data\custom'+id

    return {'pathDir':data_dir,'path':path}

def StartInfoChatID(id):
    infoFile = FindCustomID(id)
    # regex = r"\d+"
    # listInfoFile = infoFile['nameFile']
    fileDefault = open(infoFile['pathDir']+"\data\infoAI.txt", "r", encoding='utf-8')
    infoDefault = fileDefault.read()
    # idMax = len(listInfoFile)
    # file_path = os.path.join(infoFile['path'], "custom"+str(idMax)+".txt")
    # if not os.path.exists(infoFile['path']):
    #   os.makedirs(infoFile['path'])
    with open(infoFile['path'], "w", encoding="utf-8") as fileNew:
      fileNew.write(infoDefault)
    # return idMax

def NewChatID(id,content):
    infoCheck = CheckInfoChatID(id)
    newModel = fetch_geminiOption(content,infoCheck['listHistory'])
    newFileContent = infoCheck['fileChatOld'] +'\n' +"$$userStart$$"+content+"$$userEnd$$" +'\n'+ "$$modelStart$$"+newModel.replace("\n","")+"$$modelEnd$$"
    ChangeDataTxt(infoCheck['linkFile'],newFileContent)
    return newModel

    






def fetch_gemini(content):
    genai.configure(api_key="AIzaSyCbe9R6AxyCSp-lhwPNc8ceMYOZv2BYARQ")

    # Set up the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    prompt_parts = [
    "input: "+content,
    "output: ",
    ]
    try:
        response = model.generate_content(prompt_parts)
        return response.text or response.result.candidates[0].content.parts[0].text
    except Exception as e:
        return ""

def extract_words(text):
    words = re.findall(r'\b[A-Za-z]+\b', text)
    return words

def searchProvince():
    response2 = requests.get('https://backend-hcmute-nodejs.onrender.com/api/v1/locations/p')
    data2 = response2.json()
    dataJobFull2 = ""
    for i in data2['data']:
        dataJobFull2 = dataJobFull2 + i['full_name'] + ' với mã ID' +i['id'] +',\n'
    return "'"+ dataJobFull2 + "'"

def searchProvince22():
    try:
        response2 = requests.get('https://backend-hcmute-nodejs.onrender.com/api/v1/locations/p')
        data2 = response2.json()
        return data2
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
   

def searchDistrict(id):
    response2 = requests.get('https://backend-hcmute-nodejs.onrender.com/api/v1/locations/d?pid='+str(id))
    data2 = response2.json()
    dataJobFull2 = ""
    for i in data2['data']:
        dataJobFull2 = dataJobFull2 + i['full_name'] + ' với mã ID' +i['id'] +',\n'
    return dataJobFull2
    

def searchWard(id):
    response2 = requests.get('https://backend-hcmute-nodejs.onrender.com/api/v1/locations/w?did='+id)
    data2 = response2.json()
    dataJobFull2 = ""
    for i in data2['data']:
        dataJobFull2 = dataJobFull2 + i['full_name'] + ' với mã ID' +i['id'] +',\n'
    return dataJobFull2



# def AiCompany(content):
#     infocompany = InfosCompany()
#     infoAi = []
#     for i in infocompany:
#         infoAi.append({'role':'user','parts':i})
#     return fetch_geminiOption(content,infoAi)
    


def searchJobs():
    current_file_path = os.path.abspath(__file__)
    data_dir = os.path.dirname(current_file_path)
    path = data_dir+'/data/nganh.txt'

    file = open(path, "r", encoding='utf-8')
    nganh = file.read()
    return nganh

def searchJobFit(content):
    if len(extract_words(content)):
        nganh = searchJobs()
        nganh = "'"+ nganh + "'"
        req = content
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": 'Đây là các ngành của công ty tôi: '+ nganh +' .Hãy cho tôi biết mô tả sau hợp với ngành nào chỉ cần ghi mỗi số id của ngành đúng nhất không cần ghi gì ngoài id:' +req}],
        # )
        response = fetch_gemini('Đây là các ngành của công ty tôi: '+ nganh +' .Hãy cho tôi biết mô tả sau hợp với ngành nào chỉ cần ghi mỗi số id của ngành đúng nhất không cần ghi gì ngoài id:' +req)
        print("356",response)
        pattern = r'\d+'
        # match = re.findall(pattern, response.choices[0].message.content)
        match = re.findall(pattern, response)
        if match and len(match) == 1:
            number = match[0]
            return number
    return "17"

def searchVitri(content):
    try:
        number = None
        number2 = None
        number3 = "26812"
        if content != "":
            dataProvince = searchProvince()
            contentData = content
            string = ""
            pattern = r'\d+'
            print(dataProvince)
            while True: 
                string = fetch_gemini('Hãy cho tôi biết mô tả địa chỉ sau:' +contentData + '\n' +'thuộc mã nào sau đây và bạn chỉ cần trả lời là mã gì: '+ dataProvince +'\n')
                match = re.findall(pattern, string)
                if(string != "" and len(match) > 0):
                    break
            match = re.findall(pattern, string)
            if match  and len(match) == 1:   
                number = match[0]
                string2 = ""
                district = searchDistrict(number)
                while True: 
                    string2 = fetch_gemini('Hãy cho tôi biết mô tả địa chỉ sau:'+"'" +contentData +"'"+ '\n' +'thuộc mã nào sau đây và bạn chỉ cần trả lời là mã gì: '+ district +'\n')            
                    if(string2 != "" and len(re.findall(pattern, string2)) > 0):
                        break;
                match2 = re.findall(pattern, string2)
                if match2  and len(match2) == 1:
                    number2 = match2[0]
                    string3 = ""
                    ward = searchWard(number2)
                    while True:
                        string3 = fetch_gemini('Hãy cho tôi biết mô tả địa chỉ sau:' +contentData + '\n' +'thuộc mã nào sau đây và bạn chỉ cần trả lời là mã gì: '+ ward +'\n')
                        if(string3 != "" and len(re.findall(pattern, string3)) > 0):
                            break;
                    match3 = re.findall(pattern, string3)
                    if( match3  and len(match3) == 1):
                        number3 = match3[0]
            return {'wardId':number3,'districtId':number2,'provinceId':number}                                     
        return {'wardId':number3,'districtId':number2,'provinceId':number}
    except:
        return {'wardId':"26812"}

def remove_duplicates(array):
    unique_elements = list(set(array))
    return unique_elements

def count_element(array, element):
    count = array.count(element)

    return count/len(array) * 100

def JobFitContent(dataLoad):
    idAddress = {'wardId':0}
    arrayJob = []
    for i in dataLoad:
        if i['type'] == 'info_person':
            idAddress = searchVitri(i['address'])
        elif i['type'] == 'info_project':
            if len(i['moreCvProjects']) == 0 and i['moreCvProjects'][0].get('name', '') == "" and i['moreCvProjects'][0].get('position', '') == "" and i['moreCvProjects'][0].get('functionality', '') == "" and i['moreCvProjects'][0].get('technology', '') == "":
                arrayJob.append("17")
                break
            countBreak = 0
            dataInfo = ""
            for j in i['moreCvProjects']:
                try:
                    rechangeJ = replace_nulls_with_empty_string(j)
                    if rechangeJ.get('name', '') == "" and j.get('position', '') == "" and rechangeJ.get('functionality', '') == "" and rechangeJ.get('technology', '') == "":
                        countBreak = countBreak + 1
                    dataInfo = dataInfo +rechangeJ.get('name') + ','+rechangeJ.get('position', '') + ','+rechangeJ.get('functionality', '')+','+rechangeJ.get('technology', '') +';'
                except:
                    dataInfo = ""
            if countBreak == len(i['moreCvProjects']):
                arrayJob.append("17")
            else:
                arrayJob.append(searchJobFit(dataInfo))
        else:
            if len(i['moreCvExtraInformations']) == 0 and i['moreCvExtraInformations'][0]['company'] == "" and i['moreCvExtraInformations'][0]['position'] == "" and i['moreCvExtraInformations'][0]['description']:
                arrayJob.append("17")
                break
            countBreak = 0
            dataInfo = ""
            for j in i['moreCvExtraInformations']:
                rechangeJ = replace_nulls_with_empty_string(j)
                if rechangeJ['company'] == "" and rechangeJ['position'] == "" and rechangeJ['description'] == "":
                    countBreak = countBreak + 1
                dataInfo = dataInfo +rechangeJ['company'] + ','+rechangeJ['position'] + ' , '+rechangeJ['description'] +';'
            if countBreak == len(i['moreCvExtraInformations']):
                arrayJob.append("17")
            else:
                arrayJob.append(searchJobFit(dataInfo))
            # print(arrayJob)
    dataPercent = []
    countItem = remove_duplicates(arrayJob)
    for i in countItem:
        dataPercent.append({'parentCategoryId':i,'wardId':idAddress['wardId'],'percent':count_element(arrayJob,i)})
    return dataPercent
    


def FilterCvForPost(contentPost,listCV):
    descriptionPost = "Trong các CV trên hãy sắp xếp các CV theo mức độ phù hợp từ cao đến thấp (chỉ cần ghi mỗi mã CV và sắp xếp có dấu phẩy ngăn cách) theo chỉ tiêu của bài đăng sau :"+contentPost
    arrayCV = []
    # print(listCV)
    for idataLoad in range(len(listCV)):
        descripCV = "mã CV#"+str(idataLoad+1)+":\n"+"'"
        for i in listCV[idataLoad]['cvExtraInformation']:
            dataInfo = ""
            for j in i['moreCvExtraInformation']:
                dataInfo = dataInfo +j['company'] + ' '+j['position'] + ' '+j['description'] +','
            descripCV =  descripCV + dataInfo +'\n'
        for i in listCV[idataLoad]['cvProject']:
            # print(i)
            dataInfo = ""
            for j in i['moreCvProject']:
                if(j['name']):
                    dataInfo = dataInfo+ ' '+j['name'] + ' '+j['position'] + ' '+j['participant']+ ' '+j['functionality']+ ' '+j['technology'] +','
                else:
                    dataInfo = dataInfo + ' '+j['position'] + ' '+j['participant']+ ' '+j['functionality']+ ' '+j['technology'] +','
            descripCV =  descripCV + dataInfo +'\n'
        arrayCV.append({"role":"user","parts":descripCV+"'"})
    regex = r"\d+"
    listMatch = re.findall(regex,fetch_geminiOption(descriptionPost,arrayCV))
    listRender = []
    for i in listMatch:
        listRender.append({'accountId':listCV[int(i)-1]['accountId'],'cvIndex':listCV[int(i)-1]['cvIndex']})
    # print(listRender)
    return listRender


def FilterPostForCv(contentCV,listPost):
    arrayPost = []
    descripCV = "Thông tin CV: "
    for i in contentCV:
        if i['type'] == 'info_person':
            idAddress = ""
        elif i['type'] == 'info_project':
            dataInfo = ""
            for j in i['moreCvProjects']:
                dataInfo = dataInfo +j['name'] + ' '+j['position'] + ' '+j['functionality'] +','
            descripCV =  descripCV + " - "+dataInfo +'\n'
        else:
            dataInfo = ""
            for j in i['moreCvExtraInformations']:
                dataInfo = dataInfo +j['company'] + ' '+j['position'] + ' '+j['description'] +','
            descripCV =  descripCV + dataInfo +'\n'\
            
    descriptionCV = "Trong các Post trên hãy sắp xếp các Post theo mức độ phù hợp từ cao đến thấp (chỉ cần ghi mỗi mã Post và sắp xếp có dấu phẩy ngăn cách) theo chỉ tiêu của CV sau :"+descripCV
    
    for idataLoad in listPost:
        descripPost = "mã POST#"+str(idataLoad['id'])+":\n"+"'"
        filterN = idataLoad['description'].replace('\n',' ')
        filterNumber = re.sub(r'\d+', '', filterN)
        descripPost = descripPost + filterNumber
        # print(descripPost)

        arrayPost.append({"role":"user","parts":descripPost+"'"})
    regex = r"\d+"
    listMatch = re.findall(regex,fetch_geminiOption(descriptionCV,arrayPost))
    listRender = []
    for i in listMatch:
        listRender.append({'postId':i})
    # print(listRender)
    return listRender

# def FilterPostCV(contentCV,listPost):
#     descriptionPost = "Trong các post trên hãy sắp xếp các Post theo mức độ phù hợp từ cao đến thấp (chỉ cần ghi mỗi mã Post và sắp xếp có dấu phẩy ngăn cách) theo tiêu chí của cv xin việc sau :"+contentCV
#     arrayPOST = []
#     for i in listPost:
#         descripPost = "mã POST#"+i['id']+":\n" +'"'+i['description']+'"'
#         arrayPOST.append({"role":"user","parts":descripPost})
#     regex = r"\d+"
#     listMatch = re.findall(regex,fetch_geminiOption(descriptionPost,arrayPOST))
#     listRender = []
#     # for i in listMatch:
#     #     listRender.append({'accountId':listCV[int(i)-1]['accountId'],'cvIndex':listCV[int(i)-1]['cvIndex']})
#     # print(listRender)
#     return listMatch



