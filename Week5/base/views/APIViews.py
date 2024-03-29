from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status, mixins, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
import logging
from base.serializers import ProfileSerializer, UserSerializer, BlockSerializer
from base.models import Profile, Block, ProjectMember, Project

user_logger = logging.getLogger('user_logger')


class RegisterUserAPIView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_logger.info(f"{request.data.get('username')} registered!\n")
            return Response(serializer.data)
        user_logger.warning(f"{request.data.get('username')} tried to register but could not!\n")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlockList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    serializer_class = BlockSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        projects = Project.objects.filter(creator=self.request.user)
        return ProjectMember.objects.filter(project__in=projects)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BlockDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
