from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
import os

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.cleaned_data['file']
            save_path = os.path.join(settings.MEDIA_ROOT, file_obj.name)
            with open(save_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)
            return render(request, 'uploads/success.html', {'filename': file_obj.name})
    else:
        form = UploadFileForm()
    return render(request, 'uploads/upload.html', {'form': form})

def home(request):
    return render(request, 'uploads/index.html')