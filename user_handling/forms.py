from django.forms import ModelForm
from accounts.models import ApplicationForLeave

class ApplicationForLeaveForm(ModelForm):
    class Meta:
        model = ApplicationForLeave
        fields = ('description', 'start_date', 'end_date')

