from django.db import models

class CodeFile(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class ParsedClass(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)  # Link to uploaded file
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)  # CLASS, FUNCTION, FIELD, etc.

    def __str__(self):
        return f"{self.type}: {self.name}"
