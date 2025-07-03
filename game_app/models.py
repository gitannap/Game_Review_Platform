from django.db import models

from django.contrib.auth.models import User

class Game(models.Model):
    
    title = models.CharField(max_length=100)
    
    genre = models.CharField(max_length=100)
    
    platform = models.CharField(max_length=100)
    
    release_date = models.DateField(null=True)
    
    description = models.TextField(null=True)
    
    cover_image = models.ImageField(upload_to='game_covers/',blank=True,null=True)
    
    def __str__(self):
        
        return self.title
    

class Review(models.Model):
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')  
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    comment = models.TextField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Review by {self.user} for {self.game.title}'

    
    
class ReviewReaction(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='reactions')
    
    is_like = models.BooleanField()  # True = Like, False = Dislike

    class Meta:
        
        unique_together = ('user', 'review')  # Only one reaction per user per review

    
    
class Favourite(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    class Meta:
        
        unique_together = ('user','game')
    
    
    
    
    
    
    
    
    
    
    
