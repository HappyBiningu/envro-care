from rest_framework.routers import SimpleRouter
from django.urls import path
from .views.user import (CustomUserViewset, GetUserData, CustomRegisterUserViewset)
from .views.auth import (DesktopLogin, HttpOnlyLoginView, MobileLogin, Logout, XtenMobileLoginView, VerifyMobileAuthOTP)



router = SimpleRouter(trailing_slash=False)

router.register("users", CustomUserViewset, basename="users")
router.register("signup-users", CustomRegisterUserViewset, basename="signup-users")

urlpatterns = router.urls + [
    path("login/", HttpOnlyLoginView.as_view(), name="login"),
    path("desktop-login/", DesktopLogin.as_view(), name="desktop-login"),
    path("mobile-login/", MobileLogin.as_view(), name="mobile-login"),
    path("xten-mobile-login/", XtenMobileLoginView.as_view(), name="xten-mobile-login"),
    # path("verify-auth-otp/", VerifyAuthOtp.as_view(), name="verify-auth-otp"),
    path("verify-mobile-auth-otp/", VerifyMobileAuthOTP.as_view(), name="verify-mobile-auth-otp"),
    path("logout", Logout.as_view(), name="logout"),
    path("get-user-data", GetUserData.as_view(), name="get-user-data"),
    # path("verify-email", verify_email, name="verify-email"),
    # path("resend-otp", ResendOTP.as_view(), name="resend-otp"),
    # path("admin-dashboard-stats", AdminDashaboardStats.as_view(), name="admin-dashboard-stats"),

    # path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    # path('password-reset/<uid64>/<token>', reset_password, name='password-reset'),
    # path('request-reset-complete/', SetNewPassword.as_view(), name='request-reset-complete'),
    # path("check-user-authentication-status/", CheckUserAuthenticationStatus.as_view(), name='check-user-authentication-status')
]