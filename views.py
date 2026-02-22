from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Question, Choice, Submission

@login_required
def submit(request, course_id):
    """
    Handles the exam submission. Calculates the user's score, creates a 
    Submission record, and redirects to the exam result page.
    """
    course = get_object_or_404(Course, pk=course_id)
    
    # Ensure the user is enrolled in the course
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course)
    except Enrollment.DoesNotExist:
        # If not enrolled, redirect back to the course details or show an error
        return render(request, 'onlinecourse/course_detail.html', {
            'course': course,
            'error_message': "You must be enrolled to take the exam."
        })

    if request.method == 'POST':
        # Create a new submission instance
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Track the score
        total_questions = course.questions.count()
        correct_answers = 0

        # Loop through all the questions in the course
        for question in course.questions.all():
            # Get the selected choice ID from the submitted form
            # The HTML form should use name="choice_{{ question.id }}" for radio buttons
            selected_choice_id = request.POST.get(f'choice_{question.id}')
            
            if selected_choice_id:
                selected_choice = Choice.objects.get(pk=selected_choice_id)
                # Link the selected choice to the submission record
                submission.choices.add(selected_choice)
                
                # Check if the answer is correct
                if selected_choice.is_correct:
                    correct_answers += 1

        # Calculate the final grade percentage
        if total_questions > 0:
            score = (correct_answers / total_questions) * 100
        else:
            score = 0
            
        # Optional: Save the score to the submission or enrollment model if you have a field for it
        # enrollment.grade = score
        # enrollment.save()

        # Redirect to the show_exam_result view, passing the course_id and submission_id
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    
    # If not a POST request, just redirect to course details
    return redirect('onlinecourse:course_details', course_id=course.id)


@login_required
def show_exam_result(request, course_id, submission_id):
    """
    Displays the results of a specific exam submission.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Calculate the score again for display, or retrieve it if you saved it to the model
    total_questions = course.questions.count()
    correct_answers = submission.choices.filter(is_correct=True).count()
    
    score = 0
    if total_questions > 0:
        score = (correct_answers / total_questions) * 100
        
    # Determine pass/fail (e.g., passing grade is 80%)
    passing_score = 80.0
    passed = score >= passing_score

    context = {
        'course': course,
        'submission': submission,
        'score': round(score, 2),
        'passed': passed,
        'total_questions': total_questions,
        'correct_answers': correct_answers
    }
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
