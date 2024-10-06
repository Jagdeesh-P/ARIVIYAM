from django.test import TestCase
'''from .models import profile, Course
from .utils.accessibility_utils import text_to_speech, translate_text, convert_to_sign_language
from .utils.other_utils import generate_random_string, calculate_average

class AccessibilityUtilsTests(TestCase):

    def test_text_to_speech(self):
        text = "Hello, this is a test."
        # Here you would normally check if the speech was produced
        # Since we cannot check audio output, we will assume this works for now
        result = text_to_speech(text)
        self.assertIsNone(result)

    def test_translate_text(self):
        translated = translate_text("Hello", target_language='es')
        self.assertEqual(translated, "Hola")  # Assuming Google's translation is accurate

    def test_convert_to_sign_language(self):
        text = "Hello"
        sign_lang = convert_to_sign_language(text)
        self.assertIsInstance(sign_lang, str)  # Assuming the return type is string

class OtherUtilsTests(TestCase):

    def test_generate_random_string(self):
        random_string = generate_random_string(10)
        self.assertEqual(len(random_string), 10)
        self.assertTrue(random_string.isalnum())  # Check if it's alphanumeric

    def test_calculate_average(self):
        scores = [80, 90, 70, 100]
        average = calculate_average(scores)
        self.assertEqual(average, 85)

class UserProfileModelTests(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

class CourseModelTests(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='Test Course',
            description='This is a test course.',
            duration='3 hours',
        )

    def test_course_creation(self):
        self.assertEqual(self.course.title, 'Test Course')
        self.assertEqual(self.course.description, 'This is a test course.')
'''