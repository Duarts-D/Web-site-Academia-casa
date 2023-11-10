from django.shortcuts import render

# Create your views here.
def handler404(request, exception):
    return render(request,'nout_found_404.html',{'geral':'geral'}, status=404)