from django.shortcuts import render
from rest_framework import generics, status
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer
# from g4f.client import Client
import requests
from .train import searchDistrict,searchProvince22,searchProvince,searchWard,searchVitri,searchJobFit,JobFitContent,NewChatPublic,StartInfoChatPublic,FilterCvForPost,FilterPostForCv
import json

# client = Client()

def my_view(request):
    
    return JsonResponse({'data': request})

@csrf_exempt
def fetch_data(request):
    # Replace with the actual API URL
    if request.method == 'GET':
        api_url = 'http://localhost:8888/api/v1/categories'

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

        data = response.json()
        return JsonResponse(data)
    elif request.method == 'POST':
        datas = json.loads(request.body)
        dataContent = datas.get('content')
        dataID = datas.get('id')
        if(dataContent and dataID):
            datasetup = {"id":dataID,"position":searchVitri(dataContent) }
            return JsonResponse({'data': datasetup})
        else:
            return JsonResponse({'data':[],'message': "Không cung cấp đủ thông tin"})

    else:
        return JsonResponse({'error': 'Unsupported request method'}, status=405)


@csrf_exempt
def SearchJobData(request):
    if request.method == 'GET':
        return JsonResponse({'message':'Successful'})
    elif request.method == 'POST':
        datas = json.loads(request.body)
        dataContent = datas.get('content')
        dataID = datas.get('id')
        if(dataContent and dataID):
            datasetup = {"id":dataID,"idJob":searchJobFit(dataContent) }
            return JsonResponse({'data': datasetup})
        else:
            return JsonResponse({'data':[],'message': "Không cung cấp đủ thông tin"})

    else:
        return JsonResponse({'message':'UnSuccessful'}, status=405)

@csrf_exempt
def ChatAi22(request):
    if request.method == 'GET':
        data = searchProvince22()
        if data is not None:
            return JsonResponse({'data': data})
        else:
            return JsonResponse({'message': 'Không thể lấy dữ liệu từ API'}, status=500)
    elif request.method == 'POST':
        datas = json.loads(request.body)
        dataId = datas.get('id')
        dataContent = datas.get('content').replace('\n',"")
        if dataContent and dataId:
            datasetup = NewChatPublic(dataId, dataContent)
            return JsonResponse({'data': datasetup})
        else:
            return JsonResponse({'data': [], 'message': "Không cung cấp đủ thông tin"})
    else:
        return JsonResponse({'message':'Unsuccessful'}, status=405)

@csrf_exempt
def SearchJobFit(request):
    if request.method == 'GET':
        return JsonResponse({'message':'Successful'})
    elif request.method == 'POST':
        datas = json.loads(request.body)
        dataContent = datas.get('content')
        if(dataContent):
            datasetup = JobFitContent(dataContent) 
            return JsonResponse({'data': datasetup})
        else:
            return JsonResponse({'data':[],'message': "Không cung cấp đủ thông tin"})

    else:
        return JsonResponse({'message':'UnSuccessful'}, status=405)        

@csrf_exempt
def ChatAi(request):
    if request.method == 'GET':
        return JsonResponse({'message':'Successful'})
    elif request.method == 'POST':
        datas = json.loads(request.body)
        dataId = datas.get('id')
        dataContent = datas.get('content').replace('\n',"")
        if(dataContent and dataId):
            datasetup = NewChatPublic(dataId,dataContent)
            return JsonResponse({'data': datasetup})
        else:
            return JsonResponse({'data':[],'message': "Không cung cấp đủ thông tin"})

    else:
        return JsonResponse({'message':'UnSuccessful'}, status=405)  
    
@csrf_exempt
def GenerateChatAi(request):
    if request.method == 'GET':
        return JsonResponse({'message':'Successful'})
    elif request.method == 'POST':
        datasetId = StartInfoChatPublic()
        return JsonResponse({'data': datasetId})

    else:
        return JsonResponse({'message':'UnSuccessful'}, status=405)  
    
@csrf_exempt
def FilterCVPost(request):
    if request.method == 'GET':
        return JsonResponse({'message':'Successful'})
    elif request.method == 'POST':
        datas = json.loads(request.body)
        dataContentPost = datas.get('contentPost')
        dataListCV = datas.get('listCV')
        if(dataContentPost and dataListCV):
            datasetup = FilterCvForPost(dataContentPost,dataListCV)
            return JsonResponse({'data': datasetup})
        else:
            return JsonResponse({'data':[],'message': "Không cung cấp đủ thông tin"})

    else:
        return JsonResponse({'message':'UnSuccessful'}, status=405)  

@csrf_exempt
def FilterPostCV(request):
    if request.method == 'GET':
        return JsonResponse({'message':'Successful'})
    elif request.method == 'POST':
        datas = json.loads(request.body)
        dataContentCV = datas.get('contentCV')
        dataListPost = datas.get('listPost')
        if(dataContentCV and dataListPost):
            datasetup = FilterPostForCv(dataContentCV,dataListPost)
            return JsonResponse({'data': datasetup})
        else:
            return JsonResponse({'data':[],'message': "Không cung cấp đủ thông tin"})

    else:
        return JsonResponse({'message':'UnSuccessful'}, status=405)  

class CreateBotAddress(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            req = serializer.data['content']                        
            datasetup = {"question":req,"content":searchVitri(req) }
            return Response(datasetup, status=status.HTTP_201_CREATED)
        else:
            print("Error creating blog post:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(request):
        print("get nha:",request.data)
        return super().get_queryset()
        
# class BlogPostListCreate(generics.ListCreateAPIView):
#     queryset = BlogPost.objects.all()
#     serializer_class = BlogPostSerializer
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             req = serializer.data['content']
            
#             nganh = "Văn phòng với id 2 Khách sạn/Nhà hàng với id 3 IT/Lập trình viên với id 4 Design với id 5 Marketing với id 6 Lao động phổ thông với id 7 Ngân hàng với id 8 Beauty & Spa với id 9 Xuất nhập khẩu với id 10 Dịch vụ với id 11 Giáo dục - Đào tạo với id 12 Dịch thuật với id 13 Khoa học - Kỹ thuật với id 14 Chuyển nhà/Vệ sinh với id 15 Ngành khác với id 17"
#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[{"role": "user", "content": 'Đây là các ngành của công ty tôi: '+ nganh +' .Hãy cho tôi biết mô tả sau hợp với ngành nào chỉ cần ghi mỗi số id của ngành đúng nhất không cần ghi gì ngoài id:' +req}],
#             )
#             datasetup = {"question":'Đây là các ngành của công ty tôi: '+ nganh +' .Hãy cho tôi biết mô tả sau hợp với ngành nào chỉ cần ghi mỗi số id của ngành đúng nhất không cần ghi gì ngoài id:' +req,"content":response.choices[0].message.content}
#             return Response(datasetup, status=status.HTTP_201_CREATED)
#         else:
#             print("Error creating blog post:", serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class BlogPostRetrieveUpdateDestory(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "pk"