from django.shortcuts import render, redirect
from .models import Collection, piece
from django.views import generic
from .forms import userform
from django.contrib.auth import authenticate, login
from django.views.generic import View

class index(generic.ListView):
    template_name = "om_app1/om_templates.html"

    def get_queryset(self):
        return Collection.objects.all()


class details(generic.DetailView):
    model = Collection
    template_name = "om_app1/detailstemplate.html"


class UserformView(View):
    form_class = userform
    template_name = 'om_app1/formtemplate.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data('username')
            password = form.cleaned_data('password')
            user.set_password(password)
            user.save()
            newuser = authenticate(username=username, password=password)

            if newuser is not None:
                if newuser.is_active:
                    login(request, newuser)
                    return redirect("/om_app1")
        return render(request, self.template_name, {'form': form})
