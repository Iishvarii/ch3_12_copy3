# ============================================================
# myapp/views.py
# 這是一個「學生資料管理系統」的網頁應用程式(Django views)
# 主要功能分為兩大部分:
#   1. 一般網頁功能: 顯示/搜尋/新增/編輯/刪除學生資料 (畫面渲染 HTML)
#   2. Web API 功能 (今天新增): 提供 JSON 格式資料,給前端 AJAX 或外部程式呼叫
# ============================================================
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from myapp.models import *    # import * 表示import所有資料進來
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator

def search_list(request):
    """依姓名(cname)關鍵字搜尋學生資料; 若網址未帶cname參數,則列出全部學生資料(依cid遞減排序)"""
    if 'cname' in request.GET:
        cname = request.GET['cname']
        print(f'cname: {cname}')
        resulList = students.objects.filter(cname__icontains=cname).order_by('-cid')
        
    else:
        # orm語法, 使用 Django 的 ORM 來查詢資料庫中的 students 資料表，並依照 cid 欄位排序
        resulList = students.objects.all().order_by('-cid')  #2層資料search_list <h2>顯示student資料表的資料(第一層),<p>學號...(第二層)
        for student in resulList:          # 第9 for,10 print 行 真正在執行時要註解掉,否則會拖慢速度
            print(model_to_dict(student))  # student 物件, 把 model 物件轉換成字典格式

    # resulList = [] # 測試或無資料時 清空列表  search_list.html 要加 <h1>{{ errormessage }}</h1>
    errormessage = ""
    if not resulList:
        errormessage = "查無資料 !"
    
    # return HttpResponse("This is the search list view")
    # 將查詢結果傳遞給模板進行渲染
    # return render(request, 'search_list.html', {'resulList': resulList})
    return render(request, 'search_list.html', locals())

    
def search_name(request):
    """顯示姓名搜尋表單頁面(單純渲染表單,實際搜尋交由 search_list 處理)"""
    return render(request, 'search_name.html') # 這裡可以實現根據姓名查詢的邏輯

def index(request):
    """首頁: 顯示學生資料列表,支援site_search多關鍵字模糊搜尋(比對姓名/生日/信箱/電話/地址)與每頁3筆分頁"""
    if 'site_search' in request.GET:
        site_search = request.GET['site_search']
        site_search = site_search.strip()  # 去除前後空白
        # print(f'site_search: {site_search}')
        # 切割關鍵字, 依空白分隔
        keywords = site_search.split()  # 將關鍵字依空白分隔成列表
        print(f'keywords: {keywords}')
        # by github copilot
        # 多個關鍵字搜尋, 搜尋cname, cbirthday, cemail, cphone, caddr
        # from django.db.models import Q    (放上面了)
        query = Q()  # 初始化查詢條件
        for keyword in keywords: # query | = 等同於 i = i+1, 
            query |= (
                Q(cname__icontains=keyword) |
                Q(cbirthday__icontains=keyword) |
                Q(cemail__icontains=keyword) |
                Q(cphone__icontains=keyword) |
                Q(caddr__icontains=keyword))
        resulList = students.objects.filter(query).order_by('cid')  # 遞增顯示,  order_by('-cid')遞減顯示
        # 測試若無資料時, 清空列表
        # resulList = []
    else:
        resulList = students.objects.all().order_by('cid')  # 遞增顯示,  order_by('-cid')遞減顯示
    for student in resulList:
        print(model_to_dict(student))
    # resulList = [] # 測試若無資料時,清空列表
    status = True   # (檢查碼) 設定狀態為 True，表示資料已成功取得
    errormessage = "" # 初始化錯誤訊息為空字串
    # 如果查詢結果為空，設定錯誤訊息、狀態為 False，並將資料筆數設為 0
    if not resulList:   # 如果查詢結果為空，設定錯誤訊息、狀態為 False，並將資料筆數設為 0
        errormessage = "查無資料 !"
        status = False # 設定狀態為 False，表示資料查詢失敗
        data_count = 0 # 當查詢結果為空時，資料筆數設為 0

    else :
        data_count = resulList.count() #計算目前資料筆數


    # 分頁設定,每頁顯示3筆
    # from django.core.paginator import Paginator (放上面了)
    paginator = Paginator(resulList, 3)  # 每頁顯示3筆資料
    page_number = request.GET.get('page') # 取得當前頁碼
    page_obj = paginator.get_page(page_number) #取得當前頁的分頁物件
    


    # 說明:
    # page_obj 是一個包含該頁資料的物件
    # page_obj.number 目前頁碼
    # page_obj.paginator.num_pages 總頁數
    # page_obj.paginator.page_range 所有可用的頁碼（從 1 開始）
    # page_obj.previous_page_number 上一頁的頁碼
    # page_obj.next_page_number 下一頁的頁碼

    # page_obj.has_next 是否有下一頁
    # page_obj.has_previous 是否有上一頁
    # page_obj.object_list 該頁的資料

    
        
    # return HttpResponse("This is the index view")
    return render(request, 'index.html', locals()) # 將本地變數傳遞給模板進行渲染 

# from django.shortcuts import redirect 已經寫到最上面
def post(request):
    """新增學生資料: GET顯示空白表單(post.html),POST則將表單資料存入資料庫後導回首頁"""
    if request.method == "POST":
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f'cname: {cname}, csex: {csex}, cbirthday: {cbirthday}, cemail: {cemail}, cphone: {cphone}, caddr: {caddr}')
        add = students(
            cname=cname,
            csex=csex,
            cbirthday=cbirthday,
            cemail=cemail,
            cphone=cphone,
            caddr=caddr
        )
        add.save()  # 將新增的學生資料儲存到資料庫中
        # return HttpResponse("This is the POST request.")
        return redirect('index')  # 新增資料後重定向到首頁
    else:
        # return HttpResponse("Hello")
        return render(request, 'post.html')

def edit(request, id):
    """編輯學生資料: GET依id取出資料填入表單(edit.html),POST則依id更新資料庫後導回首頁"""
    if request.method == "POST":
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f'id: {id}')
        print(f'cname: {cname}, csex: {csex}, cbirthday: {cbirthday}, cemail: {cemail}, cphone: {cphone}, caddr: {caddr}')
        # 更新指定id的學生資料
        students.objects.filter(cid=id).update(
            cname=cname,
            csex=csex,
            cbirthday=cbirthday,
            cemail=cemail,
            cphone=cphone,
            caddr=caddr
        )
        # return HttpResponse("This is a POST request for editting student.")
        return redirect('index')  # 編輯完成後重定向到首頁
    else:
        print(f"id:{id}")
        # 取得指定id的學生資料
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        # return HttpResponse(f"This is the edit view")
        # return render(request, 'edit.html', {'student': obj})
        return render(request, 'edit.html', locals())

def delete(request, id):
    """刪除學生資料: GET依id顯示確認頁面(delete.html),POST則依id刪除資料庫紀錄後導回首頁"""
    print("test....")
    if request.method == "POST":
        print(f'id: {id}')
        students.objects.filter(cid=id).delete() # 刪除指定id的學生資料
        return redirect('index')  # 刪除完成後重定向到首頁
        # return HttpResponse("This is a POST request for deleting student.")
    else:
        print(f"id:{id}")
        # 取得指定id的學生資料
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        # return HttpResponse("This is the delete view.")
        return render(request, 'delete.html', locals())

# ============================================================
# 【今天新增】Web API 區塊
# 以下三個函式不回傳HTML頁面,而是回傳JSON格式資料,
# 讓前端 JavaScript(AJAX/fetch)或外部程式可以直接呼叫取得/新增資料。
# 對應路由設定在 urls.py 的 "web api" 區塊: getAllItems/、getItem/<id>/、createItem/
# ============================================================
from django.http import JsonResponse

def getAllItems(request):
    """Web API: 取得全部學生資料,以JSON陣列格式回傳(依cid遞增排序)"""
    resultList = students.objects.all().order_by('cid')
    # for item in resultList:
    #     print(model_to_dict(item))
    # 目的: 將queryset 轉換為list, 以便JsonResponse 可以正確處理
    resultList = list(resultList.values())   # 內部元件從QuerySet物件轉換為字典(dict)
    print(resultList)
    # return HttpResponse("This is the getAllItems view.")
    return JsonResponse(resultList, safe=False) 
# safe=Ture : 只允許傳遞 dict
# asfe=False : 允許傳遞非 dict 的資料

def getItem(request, id):
    """Web API: 依id取得單筆學生資料,找不到資料時回傳404與錯誤訊息(JSON格式)"""
    print(f'id: {id}')
    try:
        obj_data = students.objects.get(cid=id) #取得指定ID 的學生資料
        resultDict = model_to_dict(obj_data) # 將QuerySet物件轉換為字典(dict)
        return JsonResponse(resultDict, safe=True)
    except :
        return JsonResponse({'error': 'Student not found'}, status=404)
    # return HttpResponse("This is the getItem view for id.")

from django.views.decorators.csrf import csrf_exempt
# 取消 CSRF 驗證 (用於測試或外部程式呼叫 API 時), 允許跨站請求
@csrf_exempt
def createItem(request):
    """Web API: 新增學生資料,同時支援GET與POST兩種傳參方式,成功/失敗皆回傳JSON訊息"""
    try: 
        if request.method == "GET" :
            cname = request.GET['cname']
            csex = request.GET['csex']
            cbirthday = request.GET['cbirthday']
            cemail = request.GET['cemail']
            cphone = request.GET['cphone']
            caddr = request.GET['caddr']
            print("---------GET---------")
            print(f"cname: {cname}, csex: {csex}, cbirthday: {cbirthday}, cemail: {cemail}, cphone: {cphone}, caddr: {caddr}")
        elif request.method == "POST":
            cname = request.POST['cname']
            csex = request.POST['csex']
            cbirthday = request.POST['cbirthday']
            cemail = request.POST['cemail']
            cphone = request.POST['cphone']
            caddr = request.POST['caddr']
            print("---------POST-------------")
            print(f"cname: {cname}, csex: {csex}, cbirthday: {cbirthday}, cemail: {cemail}, cphone: {cphone}, caddr: {caddr}")
    except :
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try: 
        # orm 建立新的學生資料
        students.objects.create(
            cname=cname,
            csex=csex,
            cbirthday=cbirthday,
            cemail=cemail,
            cphone=cphone,
            caddr=caddr
        )
        return JsonResponse({"message": 'Student created successfully'}, safe=True)
    except :
        return JsonResponse({"message": 'Failed to create student'}, status=400)

    # return HttpResponse(f"This is the createItem view.")

@csrf_exempt
def updateItem(request, id):
    """Web API: 更新指定id的學生資料,同時支援GET與POST兩種傳參方式,成功/失敗皆回傳JSON訊息"""
    try:
        obj_data = students.objects.get(cid=id) #取得指定ID 的學生資料 
        if request.method == "GET" :
            cname = request.GET['cname']
            csex = request.GET['csex']
            cbirthday = request.GET['cbirthday']
            cemail = request.GET['cemail']
            cphone = request.GET['cphone']
            caddr = request.GET['caddr']   
        elif request.method == "POST":
            cname = request.POST['cname']
            csex = request.POST['csex']
            cbirthday = request.POST['cbirthday']
            cemail = request.POST['cemail']
            cphone = request.POST['cphone']
            caddr = request.POST['caddr']
        obj_data.cname = cname
        obj_data.csex = csex
        obj_data.cbirthday = cbirthday
        obj_data.cemail = cemail
        obj_data.cphone = cphone
        obj_data.caddr = caddr
        obj_data.save()
        return JsonResponse({"message": "Student updated successfully"}, safe=True)
    except students.DoesNotExist:
        return JsonResponse({"error": 'Student updated successfully'}, safe=True)
    except :
        return JsonResponse({'message': 'Failed to update student'}, status=400)


@csrf_exempt
def deleteItem(request, id):
    """Web API: 刪除指定id的學生資料,成功/失敗皆回傳JSON訊息"""
    try:
        obj_data = students.objects.get(cid=id) #取得指定ID 的學生資料 
        obj_data.delete()
        return JsonResponse({"message": "Student deleted successfully"}, safe=True)
    except students.DoesNotExist:
        return JsonResponse({"error": 'Student not found'}, status=404)
    except :            
        return JsonResponse({'message': 'Failed to delete student'}, status=400)
        