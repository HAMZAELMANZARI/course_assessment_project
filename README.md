# Online Course Application — Course Assessment Feature

A complete, runnable Django project implementing the IBM Skills Network final
project: an online course application with a new **assessment (exam) feature**.

Learners can enroll in a course, take a multiple-choice exam, submit it, and
immediately see a graded result page with pass/fail feedback and per-choice
feedback.

---

## Quick start

```bash
# 1. Create and activate a virtual environment (optional but recommended)
python3 -m venv djangoenv
source djangoenv/bin/activate        # Windows: djangoenv\Scripts\activate

# 2. Install Django
pip install -r requirements.txt

# 3. Create the database schema
python manage.py makemigrations onlinecourse
python manage.py migrate

# 4. Load demo data (users, course, lesson, exam)
python manage.py seed_data

# 5. Run the server
python manage.py runserver
```

Open http://127.0.0.1:8000/onlinecourse/ in your browser.

## Demo accounts (created by `seed_data`)

| Role    | Username | Password      |
|---------|----------|---------------|
| Admin   | `admin`  | `p@ssword123` |
| Learner | `learner`| `p@ssword123` |

## Try the full exam flow

1. Log in as **learner** (the learner is already enrolled in "Learning Django").
2. Click the course, press **Start Exam**.
3. Check **"Yes"** and press **Submit** → Congratulations, score 100/100.
4. Retake the exam, check **"No"** (or both boxes) → Failed, score 0/100, with
   red "Wrong answer" and yellow "Not selected" feedback.
5. Log in as **admin** at http://127.0.0.1:8000/admin/ to add new courses,
   lessons, questions, and choices (Questions are edited with their Choices
   inline; Courses with their Lessons inline).

## Project map

```
course_assessment_project/
├── manage.py                  # Django management entry point
├── requirements.txt
├── myproject/                 # project settings & root URLs
│   ├── settings.py            # SQLite, static/media, auth redirects
│   └── urls.py
└── onlinecourse/              # the application
    ├── models.py              # Instructor, Learner, Course, Lesson,
    │                          # Enrollment, Question, Choice, Submission
    ├── admin.py               # inlines: LessonInline, ChoiceInline,
    │                          # QuestionInline; QuestionAdmin, LessonAdmin
    ├── views.py               # course_list, course_details, enroll,
    │                          # submit, show_exam_result, extract_answers
    ├── urls.py                # routes incl. submit & exam_result
    ├── management/commands/
    │   └── seed_data.py       # demo data command
    └── templates/
        ├── onlinecourse/      # base, course list, course detail, exam result
        └── registration/login.html
```

## Key learning points (experiment with these)

- **Models**: `Question -> Course` (many-to-one), `Choice -> Question`
  (many-to-one), `Submission -> Enrollment` (many-to-one) with a many-to-many
  link to `Choice`.
- **Grading rule**: a question earns its grade only when the set of selected
  choices *exactly* equals the set of correct choices (`set(correct) ==
  set(selected)` in `show_exam_result`; see also `Question.is_get_score`).
- **Form handling without Django Forms**: checkboxes are named
  `choice_{{choice.id}}` and parsed in `extract_answers(request)`.
- **Admin inlines**: open a Question in the admin and edit its Choices on the
  same page.

## Lab submission mapping

| Lab task | File |
|---|---|
| Task 1 models | `onlinecourse/models.py` |
| Task 2 admin | `onlinecourse/admin.py` |
| Task 3 course detail template | `templates/onlinecourse/course_detail_bootstrap.html` |
| Task 5 submit + result views | `onlinecourse/views.py` |
| Task 5 URL routing | `onlinecourse/urls.py` |
| Task 6 exam result template | `templates/onlinecourse/exam_result_bootstrap.html` |

To prepare your own GitHub submission, fork the starter repo and replace the
files above with these, then commit and push.
