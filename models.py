from django.db import models
from django.conf import settings

# Note: This assumes you already have 'Course' and 'Enrollment' models in this app.
# If they are in a different app, you would import them or use 'appname.ModelName'.

class Question(models.Model):
    """
    Represents a specific question belonging to a course exam.
    """
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField(max_length=1000)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return f"Question: {self.question_text[:50]}..."

class Choice(models.Model):
    """
    Represents a multiple-choice option for a specific Question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.choice_text} (Correct: {self.is_correct})"

class Submission(models.Model):
    """
    Tracks a user's submitted answers for an exam.
    It links an Enrollment to the specific Choices they selected.
    """
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, related_name='submissions')
    choices = models.ManyToManyField(Choice, related_name='submissions')

    def __str__(self):
        return f"Submission ID: {self.id} for Enrollment: {self.enrollment.id}"
