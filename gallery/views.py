from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo


def photo_list(request):
    if request.method == "POST":
        title = request.POST.get('title')
        image = request.FILES.get('image')
        if title and image:
            Photo.objects.create(title=title, image=image)
            return redirect('photo_list')

    photos = Photo.objects.all().order_by('-uploaded_at')
    return render(request, 'gallery/index.html', {'photos': photos})


def update_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == "POST":
        photo.title = request.POST.get('title')
        if request.FILES.get('image'):
            photo.image = request.FILES.get('image')
            photo.thumbnail = None  # Reset so save() regenerates it
        photo.save()
        return redirect('photo_list')
    return render(request, 'gallery/edit.html', {'photo': photo})


def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('photo_list')