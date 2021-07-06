from .models import *
from .serializer import *
from rest_framework.generics import ListAPIView


class DispatchesLocationAPI(ListAPIView):
    serializer_class = DispatchSerializer

    def get_queryset(self):
        data = User.objects.filter(is_staff=True, is_superuser=False)
        return data
