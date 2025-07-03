from django import forms

from game_app.models import User,Game,Review


class UserregisterForm(forms.ModelForm):
    
    class Meta:
        
        model = User
        
        fields = ["username","password","first_name","last_name","email"]
        
        
class UserloginForm(forms.Form):
    
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Enter username','class':'form-control'}))
    
    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'placeholder':'Enter password','class':'form-control'}))
    

    
class ForgotpasswordForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        
            'class': 'form-control custom-input',
            
            'placeholder': 'Enter your username',
            
        })
    )
    
class OtpForm(forms.Form):
    
    otp = forms.CharField(
        
        max_length=6,
        
        widget=forms.TextInput(attrs={
            
            'class': 'form-control',
            
            'placeholder': 'Enter OTP'
        })
    )
    
class ResetPasswordForm(forms.Form):
    
    new_password = forms.CharField(max_length=100)
    
    confirm_password = forms.CharField(max_length=100)
    

class GameForm(forms.ModelForm):
    
    class Meta:
        
        model = Game
        
        fields = "__all__"
        
        
class ReviewForm(forms.ModelForm):
    
    class Meta:
        
        model = Review
        
        fields = ['rating','comment']
        
            
    
    
    
    
    

    


        
        
    
        
    
    
    