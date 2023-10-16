from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import views
from django.shortcuts import redirect


class LoginView(views.LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        user = form.get_user()
        if user is not None and not user.is_active:
            ctx = {'to_confirm': True}
            if self.extra_context:
                self.extra_context.update(ctx)
            else:
                self.extra_context = ctx
        return super().form_invalid(form)


class LogoutView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        logout(request)
        return redirect('user:login')
