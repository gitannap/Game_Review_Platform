from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View,TemplateView

from game_app.models import User,Game,Review,ReviewReaction

from game_app.forms import UserregisterForm,UserloginForm,ForgotpasswordForm,OtpForm,ResetPasswordForm,GameForm,ReviewForm

from django.core.mail import send_mail

from django.contrib.auth import authenticate,login,logout

from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

from django.db.models import Avg

from django.contrib import messages

from django.db.models import Avg

import random


def is_user(fn):
    
    def wrapper(request,**kwargs):
        
        id = kwargs.get("pk")
        
        data = Review.objects.get(id=id)
        
        if request.user == data.user:
            
            return fn(request,**kwargs)
        
        return redirect("login")
    
    return wrapper


class BaseView(View):
    
    def get(self,request):
        
        data = Game.objects.all()
        
        return render(request,"base.html",{'data':data})


class UserRegisterView(View):
    
    def get(self, request):
        
        form = UserregisterForm()
        
        return render(request, "register.html", {"form": form})

    def post(self, request):
        
        form = UserregisterForm(request.POST)
        
        if form.is_valid():
            
            user = User.objects.create_user(**form.cleaned_data)
            
            user.is_active = False  
            
            user.save()

            otp = random.randint(100000, 999999)
            
            request.session['otp'] = otp
            
            request.session['user_id'] = user.id

            subject = "Verify your email with Game Review Platform"
            
            message = f"Your OTP for Game Review Platform registration is: {otp}"
            
            from_email = 'annaseby5213@gmail.com'
            
            recipient_list = [form.cleaned_data.get('email')]
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect("OTP_Verification")  
        
        return render(request, "register.html", {"form": form})
    
    
class OTPVerifyView(View):
    
    def get(self, request):
        
        return render(request, "OTP_Verification.html")

    def post(self, request):
        
        entered_otp = request.POST.get("otp")
        
        if int(entered_otp) == request.session.get("otp"):
            
            user_id = request.session.get("user_id")
            
            user = User.objects.get(id=user_id)
            
            user.is_active = True
            
            user.save()
            
            del request.session['otp']
            
            del request.session['user_id']
            
            return redirect("login")
        
        else:
            
            messages.error(request, "Invalid OTP. Try again.")
            
            return render(request, "OTP_Verification.html")


class UserLoginView(View):
    
    def get(self,request):
        
        form = UserloginForm
        
        return render(request,"login.html",{"form":form})
    
    def post(self,request):
        
        form = UserloginForm(request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data.get("username")
            
            password = form.cleaned_data.get("password")
            
            user = authenticate(request,username=username,password=password)
            
            if user:
                
                login(request,user)
                
            return render(request,'base.html',{"form":form})
        

class Signout(View):
    
    def get(self,request):
        
        logout(request)
        
        print(request.user)
        
        return redirect("login")
    

class ForgotPasswordView(View):
    
    def get(self,request):
        
        form = ForgotpasswordForm
        
        return render(request,'forgot.html',{'form':form})
    
    def post(self,request):
        
        username = request.POST.get('username')
        
        user = User.objects.get(username=username)
        
        if user:
            
            otp = random.randint(1000,9999)
            
            request.session['username'] = username
            
            request.session['otp'] = otp
            
            send_mail(subject="reset password otp",message=str(otp),from_email='annaseby5213@gmail.com',recipient_list=[user.email])
            
            return redirect("otp_verify")
        

class Otp_verify(View):
    
    def get(self,request):
        
        form = OtpForm
        
        return render(request,'otp_verify.html',{'form':form})
    
    def post(self,request):
        
        new_otp = request.POST.get('otp')
        
        old_otp = request.POST.get('otp')
        
        if str(new_otp) == str(old_otp):
            
            print("matches")
            
        return redirect("reset_password")
    

class ResetPassword(View):
    
    def get(self,request):
        
        form = ResetPasswordForm
        
        return render(request,'reset_password.html',{'form':form})
    
    def post(self,request):
        
        c_password = request.POST.get("confirm_password")
        
        n_password = request.POST.get("new_password")
        
        if c_password == n_password:
            
            u_name = request.session.get("username")
            
            user = User.objects.get(username = u_name)
            
            user.set_password(n_password)
            
            user.save()
            
        return redirect("login")
    
    
class AboutUsView(View):
    
    def get(self,request):
        
        game = Game.objects.all()
        
        return render(request,"about.html",{'data':game})
    

class GameAddView(View):
    
    def get(self,request):
        
        form = GameForm
        
        return render(request,"gameadd.html",{"form":form})
    
    def post(self,request):
        
        form = GameForm(request.POST, request.FILES)
        
        print("welcome")
        
        if form.is_valid():
            
            print("hello")
            
            form.save()
            
            if request.user.is_superuser:
                
                print(form.cleaned_data)
                
                Game.objects.create(**form.cleaned_data)
                
            return redirect("game_list")
        
        return render(request,"gameadd.html",{"form":form})
    
    
class GameListView(View):
    
    def get(self,request):
        
        data = Game.objects.all()  # game object1..................objects >>> object1 ()
        
        return render(request,"gamelist.html",{"data":data})
    
    
class GameUpdateView(View):
    
    def get(self,request,**kwargs):
        
        id = kwargs.get("pk")
        
        data = Game.objects.get(id=id)
        
        form = GameForm(instance=data)
        
        return render(request,"gameupdate.html",{"form":form})
    
    def post(self,request,**kwargs):
        
        id = kwargs.get("pk")
        
        data = Game.objects.get(id=id)
        
        form = GameForm(request.POST,instance=data)
        
        if form.is_valid():
            
            if request.user.is_superuser:
                
                form.save()
                
            return redirect("game_list")
        
        return redirect("game_update")
    
    
class GameDeleteView(View):
    
    def get(self,request,**kwargs):
        
        id = kwargs.get("pk")
        
        if request.user.is_superuser:
            
            data = Game.objects.get(id=id).delete()
            
            Game.delete()
            
            return redirect("game_list")
        
        return redirect("login")


@method_decorator(login_required(login_url='login'), name='dispatch')
class ReviewAddView(View):
    
    def get(self, request, pk):
        
        form = ReviewForm()
        
        return render(request, "reviewadd.html", {"form": form, "game_id": pk})

    def post(self, request, pk):
        
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            
            review = form.save(commit=False)
            
            review.user = request.user
            
            review.game_id = pk
            
            review.save()
            
            return redirect('review_read', game_id=pk)
        
        return render(request, "reviewadd.html", {"form": form, "game_id": pk})
    

class ReviewReadView(View):
    
    def get(self, request, game_id):
        
        game = get_object_or_404(Game, pk=game_id)
        
        reviews = game.reviews.all()

        review_data = []
        
        for review in reviews:
            
            like_reactions = review.reactions.filter(is_like=True).select_related('user')
            
            dislike_reactions = review.reactions.filter(is_like=False).select_related('user')

            like_users = []
            
            dislike_users = []

            for reaction in like_reactions:
                
                if request.user.is_authenticated and reaction.user == request.user:
                    
                    like_users.append('you')
                    
                else:
                    
                    like_users.append(reaction.user.username)

            for reaction in dislike_reactions:
                
                if request.user.is_authenticated and reaction.user == request.user:
                    
                    dislike_users.append('you')
                    
                else:
                    
                    dislike_users.append(reaction.user.username)

            like_count = len(like_users)
            
            dislike_count = len(dislike_users)

            user_reaction = None
            
            if request.user.is_authenticated:
                
                reaction = review.reactions.filter(user=request.user).first()
                
                if reaction:
                    
                    user_reaction = 'like' if reaction.is_like else 'dislike'

            review_data.append({
                
                'review': review,
                'like_count': like_count,
                'dislike_count': dislike_count,
                'like_users': like_users,
                'dislike_users': dislike_users,
                'user_reaction': user_reaction,
                
            })

        return render(request, 'reviewread.html', {
            
            'game': game,
            'review_data': review_data,
            
        })



@method_decorator(login_required(login_url='login'), name='dispatch')
class ReviewUpdateView(View):
    
    def get(self,request,**kwargs):
        
        id = kwargs.get("pk")
        
        data = Review.objects.get(id=id)
        
        form = ReviewForm(instance=data)
        
        return render(request,"reviewupdate.html",{"form":form})
    
    
    def post(self,request,**kwargs):
        
        id = kwargs.get("pk")
        
        data = Review.objects.get(id=id)
        
        form = ReviewForm(request.POST,instance=data)
        
        if form.is_valid():
            
            if request.user == data.user:
                
                form.save()
                
                return redirect("review_read", game_id=data.game.id)
            
            
            print("Redirecting to review_read with pk =", data.id)


            
        return render(request,"reviewupdate.html",{"form":form})
    


@method_decorator([login_required, is_user], name="dispatch")
class ReviewDeleteView(View):
    
    def get(self, request, **kwargs):
        
        id = kwargs.get("pk")
        
        data = Review.objects.get(id=id)

        if request.user == data.user:
            
            game_pk = data.game.pk  
            
            data.delete()
            
            return redirect("review_read", game_id=game_pk)  

        return redirect("login")
    

    
class TopRatedGamesView(View):
    
    def get(self, request):
        
        games = Game.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__isnull=False).order_by('-avg_rating')[:10]

        return render(request, 'top_rated_games.html', {'games': games})
    


class GameDetailView(View):
    
    def get(self, request, pk):
        
        game = get_object_or_404(Game, pk=pk)
        
        reviews = game.reviews.all()

        # Add like/dislike count to each review
        for review in reviews:
            
            review.like_count = review.reactions.filter(is_like=True).count()
            
            review.dislike_count = review.reactions.filter(is_like=False).count()

        return render(request, 'game_detail.html', {
            
            'game': game,
            'reviews': reviews,
            
        })
    
    

@method_decorator(login_required, name='dispatch')
class LikeReviewView(View):
    
    def post(self, request, review_id):
        
        review = get_object_or_404(Review, pk=review_id)
        
        user = request.user

        # Prevent duplicate likes
        existing = ReviewReaction.objects.filter(user=user, review=review).first()
        
        if existing:
            
            if existing.is_like:
                
                existing.delete()
                
            else:
                
                existing.is_like = True
                
                existing.save()
                
        else:
            
            ReviewReaction.objects.create(user=user, review=review, is_like=True)

        return redirect('review_read', game_id=review.game.id)



@method_decorator(login_required, name='dispatch')
class DislikeReviewView(View):
    
    def post(self, request, review_id):
        
        review = get_object_or_404(Review, pk=review_id)
        
        user = request.user

        # Prevent duplicate dislikes
        existing = ReviewReaction.objects.filter(user=user, review=review).first()
        
        if existing:
            
            if not existing.is_like:
                
                existing.delete()
                
            else:
                
                existing.is_like = False
                
                existing.save()
        else:
            
            ReviewReaction.objects.create(user=user, review=review, is_like=False)

       
        return redirect('review_read', game_id=review.game.id)


    
    
class Searchfilter(View):
    
    def get(self,request):
        
        query = request.GET.get("query")
        
        game = Game.objects.none() 
        
        if query and query.lower() != "none":  
            
            game = Game.objects.filter(title__icontains=query)
        
        return render(request, 'game_search.html', {'games': game, 'query': query})
    
 

class HelpCenterView(TemplateView):
    
    template_name = 'help_center.html'
    

class PrivacyPolicyView(TemplateView):
    
    template_name = 'privacy_policy.html'
    

class TermsOfUseView(TemplateView):
    
    template_name = 'terms_of_use.html'

    