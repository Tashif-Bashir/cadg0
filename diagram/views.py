from django.http import JsonResponse

def diagram_home(request):
    return JsonResponse({"message": "Diagram API is working!"})
