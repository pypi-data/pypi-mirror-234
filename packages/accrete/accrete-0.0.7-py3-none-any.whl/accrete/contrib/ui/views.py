from django.shortcuts import render


def form_modal(request):
    return render(request, 'ui/partials/form_modal.html')
