from rest_framework.serializers import ModelSerializer
from simpellab.modules.todo.models import (
    Work
)


class WorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        exclude = [
            'deleted',
            'deleted_at',
        ]