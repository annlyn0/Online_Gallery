from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.http import JsonResponse


# @login_required
# def delete_photo(request, photo_id):
#     photo = get_object_or_404(Photo, id=photo_id)

#     if request.method == "POST":
#         photo.delete()
#         return redirect('gallery')  # Redirect back to gallery after deletion

#     return render(request, 'photos/delete_confirm.html', {'photo': photo})
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    # Delete all photos in this category first
    Photo.objects.filter(category=category).delete()
    
    # Delete the category
    category.delete()

    return redirect('gallery')

@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == "POST":
        photo.delete()
        return JsonResponse({"success": True})  # Return JSON response

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)



def loginUser(request):
    page = 'login'
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')  # Redirect to the gallery page or another page after successful login
        else:
            # Add error message when authentication fails
            messages.error(request, 'Invalid username or password')

    return render(request, 'photos/login_register.html', {'page': page})

def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)



@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})


@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)
