from rest_framework import serializers
from base.models import *


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'password', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('projects',)

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'address', 'web_site', 'avatar')


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = '__all__'

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''

    def validate_name(self, value):
        if (len(value) >= 200 or len(value) <= 0):
            raise serializers.ValidationError('Name field must be in range 0-200 symbols')
        return value


class ProjectMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProjectMember
        fields = '__all__'


class BlockSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Block
        fields = '__all__'


# class TaskShortSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     status = serializers.IntegerField()
#     project_id = serializers.IntegerField()
#     executor = UserSerializer(read_only=True)
#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     def validate_priority(self, value):
#         if int(value) > 100 or int(value) < 1:
#             raise serializers.ValidationError('Priority field must be in range 1-100')
#         return value
#
#     def create(self, validated_data):
#         task = Task.objects.create(**validated_data)
#         return task
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.status = validated_data.get('status', instance.name)
#         instance.project_id = validated_data.get('project_id', instance.name)
#         instance.save()
#         return instance


class TaskShortSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'executor', 'creator', 'block')

    def validate_priority(self, value):
        if int(value) > 100 or int(value) < 1:
            raise serializers.ValidationError('Priority field must be in range 1-100')
        return value


class TaskFullSerializer(TaskShortSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta(TaskShortSerializer.Meta):
        fields = TaskShortSerializer.Meta.fields + ('priority', 'description',)


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskDocument
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskComment
        fields = '__all__'
