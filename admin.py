from django.contrib import admin
# Importing exactly seven model classes as requested
from .models import Course, Lesson, Learner, Enrollment, Question, Choice, Submission

class ChoiceInline(admin.StackedInline):
    """
    Allows Choices to be added and edited directly from the Question admin page.
    """
    model = Choice
    extra = 3  # Provides 3 blank choice fields by default

class QuestionInline(admin.StackedInline):
    """
    Allows Questions to be added directly from a Course or Lesson admin page 
    (depending on your exact schema).
    """
    model = Question
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    """
    Customizes the admin view for Questions, embedding the Choice options inside it.
    """
    inlines = [ChoiceInline]
    list_display = ('question_text', 'course', 'grade')
    search_fields = ['question_text']
    list_filter = ['course']

class LessonAdmin(admin.ModelAdmin):
    """
    Customizes the admin view for Lessons.
    """
    list_display = ('title', 'course')
    search_fields = ['title', 'content']
    list_filter = ['course']

# Registering the customized admin classes
admin.site.register(Question, QuestionAdmin)
admin.site.register(Lesson, LessonAdmin)

# Registering the remaining models with default admin views
admin.site.register(Course)
admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Choice)
admin.site.register(Submission)
