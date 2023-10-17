from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist


@login_required
@permission_required("top.basic_access")
def index(request):
    try:
        # AA 4.x
        return render(request, "top/index-bs5.html")
    except TemplateDoesNotExist:
        # AA 3.x
        return render(request, "top/index.html")
