from tenant.forms import ModelForm
from .models import Sequence


class SequenceCreateForm(ModelForm):
    class Meta:
        model = Sequence
        fields = [
            'name',
            'nextval',
            'step'
        ]
