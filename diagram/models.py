from django.db import models

class Diagram(models.Model):
    code_file = models.ForeignKey("parsing.CodeFile", on_delete=models.CASCADE)
    diagram_image = models.ImageField(upload_to="diagrams/")
    created_at = models.DateTimeField(auto_now_add=True)
