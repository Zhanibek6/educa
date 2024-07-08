from rest_framework import serializers
from courses.models import Subject, Course, Module, Content, HtmlText, Text, File, Image, Video, Task
from accounts.models import StudentAnswer

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "title", "slug"]


class SubjectSerializerWithCount(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ["id", "title", "slug", "course_count"]

    def get_course_count(self, obj):
        return obj.courses.count()


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["id", "order", "title", "description"]


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "subject",
            "title",
            "slug",
            "overview",
            "created",
            "owner",
            "modules",
        ]


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()

'''
class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ["order", "item"]
'''



# Content stuff

class ContentSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    content_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['content_type', 'object_id', 'order', 'item', 'content_type_name']

    def get_content_type_name(self, obj):
        # Assuming you have a mapping of content type IDs to names
        content_type_mapping = {
            2: 'Text',
            3: 'File',
            
            5: 'Video',
            
            # confirmed
            6: 'Image',
            9: 'HtmlText',
            10: 'Task',
            # Add other mappings as necessary
        }
        return content_type_mapping.get(obj.content_type_id)

    def get_item(self, obj):
        content_type = obj.content_type.model_class()

        if content_type == HtmlText:
            serializer = HtmlTextSerializer(content_type.objects.get(id=obj.object_id))
        elif content_type == Text:
            serializer = TextSerializer(content_type.objects.get(id=obj.object_id))
        elif content_type == File:
            serializer = FileSerializer(content_type.objects.get(id=obj.object_id))
        elif content_type == Image:
            serializer = ImageSerializer(content_type.objects.get(id=obj.object_id))
        elif content_type == Video:
            serializer = VideoSerializer(content_type.objects.get(id=obj.object_id))
        elif content_type == Task:
            serializer = TaskSerializer(content_type.objects.get(id=obj.object_id))
        else:
            serializer = None

        if serializer:
            data = serializer.data
            data['type'] = content_type.__name__  # Add the type name
            return data
                
        return None

class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ["id", "order", "title", "description", "contents"]


class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "subject",
            "title",
            "slug",
            "overview",
            "created",
            "owner",
            "modules",
        ]


class HtmlTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = HtmlText
        fields = ['content']

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['content']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['file']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['url']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

# TODO maybe move to accounts.api
class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ['title', 'content', 'file', 'task_id']

class CourseEnrollSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

    def validate_course_id(self, value):
        try:
            course = Course.objects.get(id=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course not found")
        return value
