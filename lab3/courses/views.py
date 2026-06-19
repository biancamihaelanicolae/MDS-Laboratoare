from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Course, Category
from .forms import CourseForm


def course_list(request):
    courses = Course.objects.all().order_by('-year', 'title')
    categories = Category.objects.all().order_by('name')
    category_id = request.GET.get('category')
    if category_id:
        courses = courses.filter(category_id=category_id)
    query = request.GET.get('q', '')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(instructor__icontains=query)
        )
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'categories': categories,
        'query': query,
    })


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})


@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Add'})


@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Edit'})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


def category_courses(request, pk):
    category = get_object_or_404(Category, pk=pk)
    courses = category.courses.all().order_by('-year', 'title')
    return render(request, 'courses/category_courses.html', {
        'category': category,
        'courses': courses,
    })


def api_courses(request):
    courses = Course.objects.all().order_by('-year', 'title')
    data = [
        {
            'id': c.pk,
            'title': c.title,
            'instructor': c.instructor,
            'year': c.year,
            'semester': c.semester,
            'credits': c.credits,
            'category': c.category.name,
        }
        for c in courses
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "GET":
        data = {
            'id': course.pk,
            'title': course.title,
            'instructor': course.instructor,
            'description': course.description,
            'year': course.year,
            'semester': course.semester,
            'credits': course.credits,
            'category': course.category.name,
        }
        return JsonResponse(data)

    elif request.method == "PUT":
        body = json.loads(request.body)
        for field in ['title', 'instructor', 'description', 'year', 'semester', 'credits']:
            if field in body:
                setattr(course, field, body[field])
        if 'category' in body:
            course.category = get_object_or_404(Category, name=body['category'])
        course.save()
        data = {
            'id': course.pk,
            'title': course.title,
            'instructor': course.instructor,
            'description': course.description,
            'year': course.year,
            'semester': course.semester,
            'credits': course.credits,
            'category': course.category.name,
        }
        return JsonResponse(data)

    elif request.method == "DELETE":
        course.delete()
        return JsonResponse({'deleted': True})
