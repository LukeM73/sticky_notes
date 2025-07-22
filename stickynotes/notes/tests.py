from django.test import TestCase, Client
from django.urls import reverse
from .models import Note
from .forms import NoteForm

class NoteModelTest(TestCase):
    def test_note_creation(self):
        note = Note.objects.create(title="Test", content="Hello")
        self.assertEqual(note.title, "Test")
        self.assertTrue(note.created_at)  # Auto-set timestamp

class NoteFormTest(TestCase):
    def test_valid_form(self):
        form = NoteForm(data={"title": "Test", "content": "Hello"})
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        form = NoteForm(data={"title": "", "content": "Hello"})
        self.assertFalse(form.is_valid())

class NoteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.note = Note.objects.create(title="Test", content="Hello")

    def test_note_list_view(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")

    def test_note_create_view(self):
        response = self.client.post(reverse("note_create"), {
            "title": "New Note",
            "content": "New Content",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Note.objects.count(), 2)
