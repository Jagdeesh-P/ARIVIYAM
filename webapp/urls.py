from django.urls import path
from .views import (
    signup,
    login as user_login,  # Renamed to avoid conflict with Django's built-in `login` method
    logout as user_logout,  # Renamed to avoid conflict with `logout` method
    send_message,
    chat_page,
    home,
    intro,
    generate_course,
    course_generator,
    personalise,
    community,
    profile,analytics,lessont,
    settings,courses,course_details,precourses,projects,enroll,lesson,test,testresult
)

urlpatterns = [
    # Introduction page
    path('', intro, name='intro'),

    # User authentication views
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),  # Renamed for clarity
    path('logout/', user_logout, name='logout'),  # Renamed for clarity

    # Home page
    path('home/', home, name='home'),
    path('personalise/', personalise, name='personalise'),
    path('community/', community, name='community'),

    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    path('courses/', courses, name='courses'),
    path('precourses/', precourses, name='precourses'),
    path('course_details/', course_details, name='course_details'),
    path('enroll/', enroll, name='enroll'),
    path('projects/', projects, name='projects'),
    path('lesson/', lesson, name='lesson'),
    path('lessont/', lessont, name='lessont'),
    path('test/', test, name='test'),
    path('testresult/', testresult, name='testresult'),
    # Chatbot views
    path('chatbot/', chat_page, name='chat_page'),
    path('analytics/', analytics, name='analytics'),
    path('send-message/', send_message, name='send_message'),

    path('course-generator/', course_generator, name='course_generator'),
    path('generate-course/', generate_course, name='generate_course'),
]
