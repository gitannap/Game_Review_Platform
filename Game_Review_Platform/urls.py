"""
URL configuration for Game_Review_Platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game_app.views import *
from django.conf.urls.static import static
from django.conf import settings

def redirect_home(request):
    
    return redirect("home")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',redirect_home),
    path('Game_Review',BaseView.as_view(),name="home"),
    path('register/',UserRegisterView.as_view(),name="register"),
    path('OTP_Verification/',OTPVerifyView.as_view(),name="OTP_Verification"),
    path('login/', UserLoginView.as_view(), name='login'),
    path('signout/',Signout.as_view(),name="logout"),
    path('forgot_password/',ForgotPasswordView.as_view(),name="forgot_password"),
    path('otp_verify/',Otp_verify.as_view(),name="otp_verify"),
    path('reset_password/',ResetPassword.as_view(),name="reset_password"),
    path('about/',AboutUsView.as_view(),name="about"),
    path('game_add/',GameAddView.as_view(),name="game_add"),
    path('game_list/',GameListView.as_view(),name="game_list"),
    path('game_update/<int:pk>',GameUpdateView.as_view(),name="game_update"),
    path('game_delete/<int:pk>',GameDeleteView.as_view(),name="game_delete"),
    path('review_add/<int:pk>/', ReviewAddView.as_view(), name='review_add'),
    path('review_update/<int:pk>/',ReviewUpdateView.as_view(),name="review_update"),
    path('review_delete/<int:pk>/',ReviewDeleteView.as_view(),name="review_delete"),
    path('top_rated_games/',TopRatedGamesView.as_view(),name="top_rated_games"),
    path('game_detail/<int:pk>/',GameDetailView.as_view(),name="game_detail"),
    path('review_read/game/<int:game_id>/', ReviewReadView.as_view(), name='review_read'),
    path('review/<int:review_id>/like/', LikeReviewView.as_view(), name='like_review'),
    path('review/<int:review_id>/dislike/', DislikeReviewView.as_view(), name='dislike_review'),
    path('search_filter/',Searchfilter.as_view(),name="search_filter"),
    path('help_center/',HelpCenterView.as_view(),name='help_center'),
    path('privacy_policy/',PrivacyPolicyView.as_view(),name='privacy_policy'),
    path('terms_of_use/',TermsOfUseView.as_view(),name='terms_of_use')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
