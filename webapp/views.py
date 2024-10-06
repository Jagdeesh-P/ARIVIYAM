from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash, check_password_hash
from django.views.decorators.csrf import csrf_exempt
import openai
from django.http import JsonResponse
from django.middleware.csrf import get_token
import json


# Initialize MongoDB
db = settings.MONGO_DB

# OpenAI API key configuration
openai.api_key = ''
# Home View
def home(request):
    return render(request, 'index.html')
def personalise(request):
    return render(request, 'personalise.html')

# Intro View
def intro(request):
    return render(request, 'intro.html')
def profile(request):
    return render(request, 'profile.html')
def settings(request):
    return render(request, 'settings.html')
def courses(request):
    return render(request, 'course_generator.html')
def precourses(request):
    return render(request, 'courses.html')
def course_details(request):
    return render(request, 'course-details.html')
def enroll(request):
    return render(request, 'enroll_course.html')
def lesson(request):
    return render(request, 'lesson.html')
def testresult(request):
    return render(request, 'test-results.html')
def test(request):
    return render(request, 'test.html')
def analytics(request):
    return render(request, 'analytics.html')
def lessont(request):
    return render(request, 'lessont.html')
def projects(request):
    return render(request, 'projects.html')
# Chatbot Page
def chat_page(request):
    return render(request, 'chatbot.html')

# Chatbot Message View
@csrf_exempt
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get('message')

        # Call OpenAI's GPT-4 to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an educational instructor specializing in guiding college students and professionals. Provide clear, helpful answers, and keep responses within 100 words."},
                      {"role": "user", "content": user_message}],
            max_tokens=400,  # Restrict response to about 400 tokens
            temperature=0
        )

        bot_response = response['choices'][0]['message']['content']
        return JsonResponse({'response': bot_response})

    return JsonResponse({"error": "Invalid request"}, status=400)

# User Registration (Signup) View
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        # Hash the password for secure storage
        hashed_password = generate_password_hash(password)

        try:
            # Debug: Check what is being inserted into the database
            print(f"Attempting to insert:{email}")

            # Insert the new user into the MongoDB 'users' collection
            db.users.insert_one({
                'email': email,
                'password': hashed_password
            })

            # Debug: Log success
            print("User successfully inserted into MongoDB.")

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')

        except DuplicateKeyError:
            # Handle case where username or email already exists
            if db.users.find_one({'email': email}):
                messages.error(request, 'Email already exists.')
            return redirect('signup')

        except Exception as e:
            # Catch any other exceptions and log them
            print(f"Error during signup: {str(e)}")
            messages.error(request, 'An error occurred during registration. Please try again.')
            return redirect('signup')

    return render(request, 'signup.html')

# User Login View
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find user in MongoDB
        user = db.users.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            # Password matches, log the user in
            # Simulate a login since Django's auth system isn't tied to MongoDB
            request.session['email'] = email
            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to home page after login
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

    return render(request, 'login.html')



def logout(request):
    """Handles user logout by clearing the session."""
    if 'email' in request.session:
        # Remove the user's email from the session
        del request.session['email']
        messages.success(request, 'You have successfully logged out.')
    else:
        messages.info(request, 'You are not logged in.')

    return redirect('login')  # Redirect to the login page after logout


def course_generator(request):
    """Render the course generator page with CSRF token."""
    csrf_token = get_token(request)  # Get the CSRF token
    return render(request, 'course_generator.html', {'csrf_token': csrf_token})
# Course Generation View
@csrf_exempt
def generate_course(request):
    if request.method == "POST":
        data = json.loads(request.body)
        topic = data.get('topic')
        level = data.get('level')
        num_videos = data.get('numVideos')

        # Prepare the prompt for OpenAI based on the input
        prompt = (f"Generate detailed content scripts for {num_videos} video lessons on the topic '{topic}' targeted at the {level} level audience. Each script should include the following components: "
                  f"1. Introduction: A brief overview of the topic and its importance."
                  f"2. Main Points: Key concepts to be covered in the lesson, clearly organized and explained."
                  f"3. Examples or Case Studies: Relevant real-world applications or scenarios that illustrate the main points."
                  f"4. Conclusion: A summary of the lesson, reinforcing the key takeaways."
                  f"Ensure that the scripts are engaging and informative, suitable for the target audience's skill level. Include explanations for any essential terminology or concepts to enhance understanding"
                  )
        try:
            # Call OpenAI's API to generate the course content
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,  # Limit the number of tokens for the response
                temperature=1
            )

            course_content = response['choices'][0]['message']['content']

            # Store the generated content in MongoDB
            db.content.insert_one({
                'topic': topic,
                'level': level,
                'num_videos': num_videos,
                'content': course_content
            })

            return JsonResponse({'success': True, 'courseContent': course_content})

        except Exception as e:
            print(f"Error generating course content: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Error generating course content.'})

    return JsonResponse({"error": "Invalid request"}, status=400)

def community(request):
    # If you want to pass any context to the template, add it here
    context = {
        'discussion_topics': [
            "How to improve my programming skills?",
            "Best practices for studying Python",
            "Creating a Python project from scratch"
        ],
        'events': [
            {'name': 'Python Workshop', 'date': 'Oct 10'},
            {'name': 'Python Hackathon', 'date': 'Oct 12'}
        ],
        'profiles': [
            {'name': 'John Doe', 'description': 'AI Enthusiast | Python Developer', 'image': 'user1.jpg'},
            {'name': 'Jane Smith', 'description': 'Data Scientist | Python Lover', 'image': 'user2.jpg'}
        ]
    }
    return render(request, 'community.html', context)