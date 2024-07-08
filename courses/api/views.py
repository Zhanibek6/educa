from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from courses.api.serializers import SubjectSerializer, SubjectSerializerWithCount, CourseSerializer, CourseWithContentsSerializer, ModuleSerializer, ContentSerializer, CourseEnrollSerializer, StudentAnswerSerializer, TaskSerializer, ModuleWithContentsSerializer
from courses.models import Subject, Course, Module, Content, Task
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from courses.api.permissions import IsEnrolled
from accounts.models import CustomUser
from rest_framework import status
from django.utils import timezone


class SubjectListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializerWithCount


class SubjectDetailView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        subject_pk = self.kwargs.get('pk')
        return Course.objects.filter(subject_id=subject_pk)

    def list(self, request, *args, **kwargs):
        subject_pk = self.kwargs.get('pk')
        subject = get_object_or_404(Subject, pk=subject_pk)
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class StudentCourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(students=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        course_data = serializer.data

        # Replace owner id with author name
        author_id = course_data.get('owner')
        if author_id:
            try:
                author = CustomUser.objects.get(id=author_id)
                course_data['owner'] = f"{author.first_name} {author.last_name}"
            except CustomUser.DoesNotExist:
                course_data['owner'] = None

        # Include modules and their content in the response
        modules = Module.objects.filter(course=instance)
        module_serializer = ModuleSerializer(modules, many=True)
        module_data = module_serializer.data

        # Add ids for modules
        for index, module in enumerate(module_data):
            module['id'] = module['id']

        course_data['modules'] = module_data

        return Response(course_data)

'''
class ModuleDetailView(generics.RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        module_data = serializer.data

        # Include content within the module in the response
        contents = Content.objects.filter(module=instance)
        content_serializer = ContentSerializer(contents, many=True)
        module_data['contents'] = content_serializer.data

        return Response(module_data)
    '''

class ModuleDetailView(generics.RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleWithContentsSerializer 
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        course_pk = self.kwargs['course_pk']
        module_pk = self.kwargs['module_pk']
        instance = self.get_queryset().filter(course_id=course_pk, id=module_pk).first()
        if not instance:
            return Response({"detail": "Not found."}, status=404)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if not instance:
            return Response({"detail": "Not found."}, status=404)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({"enrolled": True})

    @action(
        detail=True,
        methods=["get"],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled],
        serializer_class=CourseWithContentsSerializer,
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# TODO move these to accounts.api later
class StudentEnrollCourseView(generics.GenericAPIView):
    serializer_class = CourseEnrollSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        course_id = serializer.validated_data['course_id']
        course = Course.objects.get(id=course_id)
        course.students.add(request.user)
        
        return Response({'message': 'Enrolled successfully', 'course_id': course_id})
    

class UnsubscribeCourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_pk):
        course = get_object_or_404(Course, pk=course_pk)
        if course.students.filter(pk=request.user.pk).exists():
            course.students.remove(request.user)
            return Response({"status": "success"}, status=status.HTTP_200_OK)


class StudentAnswerCreateAPIView(generics.CreateAPIView):
    serializer_class = StudentAnswerSerializer

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, id=self.kwargs['task_id'])
        self.module = Content.objects.get(content_type__model='task', object_id=self.task.pk).module
        self.course = self.module.course
        return super().dispatch(request, *args, **kwargs)

    def check_permissions(self, request):
        user = request.user
        # Check if user has already answered the task
        if user.task_answers.filter(task=self.task).exists():
            self.permission_denied(request, message="You have already answered this task.")
        
        # Check if the deadline has passed
        if self.task.deadline and self.task.deadline < timezone.now():
            self.permission_denied(request, message="The deadline for this task has passed.")
        
        # Check if the user is a student of the course
        if user not in self.course.students.all():
            self.permission_denied(request, message="You are not enrolled in this course.")

    def perform_create(self, serializer):
        serializer.save(task_id=self.kwargs['task_id'], student=self.request.user)

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        return super().create(request, *args, **kwargs)