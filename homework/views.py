from django.shortcuts import render

from django.http import HttpResponse
from .models import Student, Course, Score, Teacher
from django.db.models import Avg, Count, Min, Max, Sum, Q, F


def index(request):
    '''查询平均成绩大于60分的同学的ID和平均成绩'''
    students = Student.objects.annotate(score_avg=Avg(
        'score__number')).filter(score_avg__gt=60).values('id', 'score_avg')
    for student in students:
        print(student)
    return HttpResponse('success')


def index2(request):
    '''查询所有同学的ID,姓名，选课的数量，总成绩'''
    students = Student.objects.annotate(course_nums=Count('score__course'), sum=Sum('score__number')).values(
        'id', 'name', 'course_nums', 'sum')
    for student in students:
        print(student)
    return HttpResponse('success1')


def index3(request):
    ''' 查询姓“李”老师的个数'''
    nums = Teacher.objects.filter(name__startswith='李').count()
    print(nums)
    return HttpResponse('success3')


def index4(request):
    '''查询没学过“李老师”的课的所有同学的ID，姓名'''
    students = Student.objects.exclude(score__course__teacher__name='李老师').values('id', 'name')
    for student in students:
        print(student)
    return HttpResponse('success4')


def index5(request):
    '''查询学过课程ID为1和2 的所有同学的ID，姓名'''
    students = Student.objects.filter(score__course__in=[1, 2]).distinct().values('id', 'name')
    for student in students:
        print(student)
    return HttpResponse('success5')


def index6(request):
    '''查询学过“黄老师”所教的“所有课”的同学的ID，姓名'''
    students = Student.objects.annotate(nums=Count('score__course',
                                                   filter=Q(score__course__teacher__name='黄老师'))).filter(nums=
                                  Course.objects.filter(teacher__name='黄老师').count()).values('id', 'name')
    for student in students:
        print(student)
    return HttpResponse('success6')


def index7(request):
    '''查询所有课程成绩小于60分的同学的ID，姓名'''
    students = Student.objects.filter(score__number__lt=60).values('id', 'name')
    for student in students:
        print(student)
    return HttpResponse('success7')


def index8(request):
    '''查询没有学全所有课的同学的ID，姓名'''
    students = Student.objects.annotate(course_nums=Count('score__course')).filter(
        course_nums__lt=Course.objects.count()).values('id', 'name')
    for student in students:
        print(student)
    return HttpResponse('success8')


def index9(request):
    '''查询所有同学的姓名，平均分，并按照平均分由高到低排序'''
    students = Student.objects.annotate(avg=Avg('score__number')).order_by('-avg').values('name', 'avg')
    for student in students:
        print(student)
    return HttpResponse('success9')


def index10(request):
    '''查询各科成绩的最高和最低分，如下形式显示：课程ID，课程名称，最高分，最低分'''
    courses = Course.objects.annotate(max=Max('score__number'),
                                      min=Min('score__number')).values('id', 'name', 'max', 'min')
    for course in courses:
        print(course)
    return HttpResponse('success10')


def index11(request):
    '''查询每门课程的平均成绩，并按照平均成绩排序'''
    courses = Course.objects.annotate(avg=Avg('score__number')).order_by('avg').values('id', 'name', 'avg')
    for course in courses:
        print(course)
    return HttpResponse('success11')


def index12(request):
    '''统计总共多少男生，多少女生'''
    num = Student.objects.aggregate(female=Count('gender', filter=Q(gender=1)), male=Count('gender', filter=Q
    (gender=2)))
    print(num)
    return HttpResponse('success12')


def index13(request):
    '''将“黄老师”的每一门课程的都在原来的基础上加5分'''
    scores = Score.objects.filter(course__teacher__name='黄老师').update(number=F('number')+5)
    print(scores)
    return HttpResponse('success13')


def index14(request):
    '''查询两门以上不及格的同学的ID，姓名，以及不及格课程数'''
    students = Student.objects.annotate(f_nums=Count('score__course', filter=Q
        (score__number__lt=60))).filter(f_nums__gte=2).values('id', 'name', 'f_nums')
    for student in students:
        print(student)

    return HttpResponse('success14')

def index15(request):
    '''查询每门课的选课人数'''
    courses = Course.objects.annotate(num=Count('score__student')).values('id', 'name', 'num')
    for course in courses:
        print(course)
    return HttpResponse('success15')