from .models import Tweets
from django import forms
MAX_TWEET_LENGTH = 200
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = ['content']
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if(len(content)>MAX_TWEET_LENGTH):
            raise forms.ValidationError("THIS TWEET IS TOO LONG TO HANDLE")
        return content

