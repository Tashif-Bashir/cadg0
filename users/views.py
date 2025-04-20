from django.http import JsonResponse

def users_home(request):
    return JsonResponse({"message": "Users API is working!"})
