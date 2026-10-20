from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Question, Choice, Submission


def course_list(request):
    context = {}
    if request.user.is_authenticated:
        context['courses'] = Course.objects.order_by('-total_enrollment')[:10]
    else:
        context['courses'] = Course.objects.order_by('-total_enrollment')[:10]
    return render(request, 'onlinecourse/course_list_bootstrap.html', context)


def course_details(request, pk):
    context = {}
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=pk)
            if request.user.is_authenticated:
                try:
                    enrollment = Enrollment.objects.get(user=request.user, course=course)
                    course.is_enrolled = True
                except Enrollment.DoesNotExist:
                    course.is_enrolled = False
            context['course'] = course
            return render(request, 'onlinecourse/course_detail_bootstrap.html', context)
        except Course.DoesNotExist:
            return HttpResponseRedirect(reverse('onlinecourse:index'))


@login_required
def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        # Create an enrollment
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user, course=course)
        course.total_enrollment += 1
        course.save()
        return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


# <HINT> A example method to collect the selected choices from the exam form
# from the submitted request (POST) body. The keys of the selected choices
# in the request payload start with 'choice'.
def extract_answers(request):
    submitted_anwsers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_anwsers.append(choice_id)
    return submitted_anwsers


# <HINT> Create a submit view to create an exam submission record for a
# course enrollment, you may implement it based on the following logic:
# Get user and course object, then get the associated enrollment object
# created when the user enrolled the course
# Create a submission object referring to the enrollment
# Collect the selected choices from exam form
# Add each selected choice object to the submission object
# Redirect to show_exam_result with the submission id
@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    choices = extract_answers(request)
    submission.choices.set(choices)
    submission_id = submission.id
    return HttpResponseRedirect(
        reverse(viewname='onlinecourse:exam_result',
                args=(course_id, submission_id,)))


# <HINT> An example method to check if the learner passed the exam and
# show their question results and score for the exam.
# You will need to specify the template name in 'render()'
# You will need the submit object and submission id to get the exam result
@login_required
def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.get(id=submission_id)
    choices = submission.choices.all()

    total_score = 0
    questions = course.question_set.all()  # Assuming course has related questions

    for question in questions:
        correct_choices = question.choice_set.filter(is_correct=True)  # all correct choices
        selected_choices = choices.filter(question=question)  # user's selected choices

        # Award the question's grade only if the selected choices exactly
        # match the correct choices (no missing, no extra).
        if set(correct_choices) == set(selected_choices):
            total_score += question.grade  # Add the question's grade only if all correct answers are selected

    context['course'] = course
    context['grade'] = total_score
    context['choices'] = choices
    context['submission'] = submission

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
