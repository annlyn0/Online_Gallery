from django.shortcuts import render, redirect
from .models import Category, Photo

def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all()
    # photos = Photo.objects.all()

    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

def viewPhoto(request, pk):
    photos = Photo.objects.get(id=pk)

    context = {'photo': photos}
    return render(request, 'photos/photo.html', context)

def addPhoto(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new']:
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            category = category,
            description = data['description'],
            image = image
        )
        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/Add.html', context)

