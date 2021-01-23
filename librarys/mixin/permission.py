from django.contrib.auth.mixins import AccessMixin


class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    login_url = "/login"

    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("user_name", False) and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    # 禁止未登录跳转时的next参数
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
