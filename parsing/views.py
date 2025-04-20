from django.shortcuts import render, redirect
from django.http import JsonResponse
from .cpp_parser import parse_cpp_file
from .forms import UploadFileForm
from .models import UploadedFile, ParsedClass


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()  # Save the uploaded file
            parsed_data = parse_cpp_file(uploaded_file.file.path)  # Parse the file
            
            # Save parsed data into the database
            for item in parsed_data:
                ParsedClass.objects.create(
                    file=uploaded_file,
                    name=item["name"],
                    type=item["type"]
                )

            return JsonResponse({"message": "File parsed and saved!", "parsed_data": parsed_data})
    else:
        form = UploadFileForm()
    
    return render(request, "parsing/upload.html", {"form": form})

def view_parsed_data(request):
    parsed_classes = ParsedClass.objects.all().values("file__file", "name", "type")
    return JsonResponse(list(parsed_classes), safe=False)
