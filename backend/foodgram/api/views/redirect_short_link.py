from django.shortcuts import redirect


def redirect_short_link(request, pk):
    return redirect(f'/recipes/{pk}/')
