from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile,SavedJob


@login_required
def profile_create(request):
    try:
        profile = request.user.profile
        is_update = True
    except Profile.DoesNotExist:
        profile = None
        is_update = False

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            # return redirect('profile_detail')

    else:
        form = ProfileForm(instance=profile)
    savedjobs = SavedJob.objects.all()
    
    return render(request, 'profile.html', {'form': form,'savedjobs': savedjobs, 'is_update': is_update})
