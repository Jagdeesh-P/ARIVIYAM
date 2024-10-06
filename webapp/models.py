from django.db import models
'''from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Custom user model to extend user functionality
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('college_student', 'College Student'),
        ('professional', 'Professional'),
    )
    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES)
    is_blind = models.BooleanField(default=False)
    is_deaf = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=100, default='English')
    sign_language_support = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} ({self.get_user_type_display()})'

# Model for Course Categories
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Model for Courses
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    students_enrolled = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Model for Modules inside Courses
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

# Model for Lessons inside Modules
class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)  # AI-generated video content
    text_content = models.TextField()  # AI-generated text content
    accessibility_text_to_speech = models.URLField(blank=True, null=True)  # Text to Speech URL for blind users
    accessibility_sign_language_video = models.URLField(blank=True, null=True)  # Sign language video for deaf users

    def __str__(self):
        return self.title

# Model for Assessment inside Courses (Quizzes or Tests)
class Assessment(models.Model):
    course = models.ForeignKey(Course, related_name='assessments', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    max_score = models.IntegerField()

    def __str__(self):
        return self.title

# Questions for assessments
class Question(models.Model):
    assessment = models.ForeignKey(Assessment, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer = models.TextField()
    options = models.JSONField()  # Store multiple choice options

    def __str__(self):
        return f'Question {self.id} for {self.assessment.title}'

# Student progress tracking (adaptive learning system)
class Progress(models.Model):
    user = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='progress', on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    score = models.IntegerField(default=0)
    pace = models.CharField(max_length=20, choices=[('slow', 'Slow'), ('medium', 'Medium'), ('fast', 'Fast')], default='medium')  # Adaptive learning pace

    def __str__(self):
        return f'{self.user.username} Progress in {self.course.title}'

# Gamified Badges
class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='badges', blank=True)

    def __str__(self):
        return self.name

# Certificates after completing courses
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'

# Peer Collaboration and Community Interaction
class Discussion(models.Model):
    course = models.ForeignKey(Course, related_name='discussions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='discussions', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Discussion in {self.course.title}'

# AI Chatbot Query Management (for doubts and queries)
class ChatbotQuery(models.Model):
    user = models.ForeignKey(User, related_name='queries', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='queries', on_delete=models.CASCADE)
    query_text = models.TextField()
    response_text = models.TextField(blank=True, null=True)  # AI-generated response
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} query in {self.course.title}'

# Projects given after course completion
class Project(models.Model):
    course = models.ForeignKey(Course, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_industry_related = models.BooleanField(default=False)
    students = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return f'{self.title} - {self.course.title}'

# Model for project submission by students
class ProjectSubmission(models.Model):
    project = models.ForeignKey(Project, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)
    file_submission = models.FileField(upload_to='project_submissions/')
    score = models.IntegerField(blank=True, null=True)  # AI-assessed score
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} submission for {self.project.title}'''

