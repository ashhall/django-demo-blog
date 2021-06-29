from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # create a form that is passed to the template
        if form.is_valid():
            form.save()  # save the user info, automatically hashes password
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        # request.POST passes in the posted data to update the form
        user_form = UserUpdateForm(request.POST, instance=request.user) #instance param lets django know which profile to update
        # request.FILES is needed because user might be uploading a profile pic
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account information has been updated!')
            return redirect('profile') # post get redirect pattern
    else:
        # instance = ... populates the form in the browser with the current user data
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'user_form': user_form,
               'profile_form': profile_form
               }
    return render(request, 'users/profile.html', context)
