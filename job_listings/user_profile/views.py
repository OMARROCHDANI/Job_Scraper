from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile,SavedJob
from django.shortcuts import get_object_or_404


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
                # Check if a saved job needs to be deleted
        if 'delete_saved_job' in request.POST:
            job_id_to_delete = request.POST.get('delete_saved_job')
            saved_job_to_delete = get_object_or_404(SavedJob, id=job_id_to_delete)
            saved_job_to_delete.delete()

    else:
        form = ProfileForm(instance=profile)
    savedjobs = SavedJob.objects.all()
    
    return render(request, 'profile.html', {'form': form,'savedjobs': savedjobs, 'is_update': is_update})
