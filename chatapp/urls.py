from rest_framework import routers
from .views import GroupMessageViewSet,playerViewSet
router = routers.DefaultRouter()
router.register(r'group-messages', GroupMessageViewSet)
router.register(r'player-Information', playerViewSet)

urlpatterns = [

 
]
urlpatterns += router.urls