import pickle
import oauth2
import json
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from ims_lti_py.tool_provider import DjangoToolProvider
from django.shortcuts import render,render_to_response,redirect

from lti.models import LTIUser
from ct.models import Role, Course, Unit

@csrf_exempt
def index(request):
    if settings.LTI_DEBUG:
        print "META"
        print request.META
        print "PARAMS"
        print request.POST
    session = request.session
    session.clear()
    try:
        consumer_key = settings.CONSUMER_KEY
        secret = settings.LTI_SECRET

        tool = DjangoToolProvider(consumer_key, secret, request.POST)
        is_valid = tool.is_valid_request(request)
        session['message'] = "We are cool!"
    except oauth2.MissingSignature,e:
        is_valid = False
        session['message'] = "{}".format(e)
        pass
    except oauth2.Error,e:
        is_valid = False
        session['message'] = "{}".format(e)
        pass
    except KeyError,e:
        is_valid = False
        session['message'] = "{}".format(e)
        pass
    session['is_valid'] = is_valid
    # copy request to dictionary
    request_dict = dict()
    for r in request.POST.keys():
        request_dict[r] = request.POST[r]
    session['LTI_POST'] = pickle.dumps( request_dict )
    print('==========================================')
    print(request_dict)
    print('++++++++++++++++++++++++++++++++++++++++++')
    print(request_dict.get('custom_course', None))
    print(request_dict.get('custom_unit', None))
    print('==========================================')
    session['LTI_POST'] = pickle.dumps( request_dict )

    user, created = LTIUser.objects.get_or_create(user_id = request_dict.get('user_id', ''))
    if not user.user_fk:
        django_user, created = User.objects.get_or_create(username=request_dict.get('user_id', ''))
        user.user_fk = django_user.id
        user.all_data = json.dumps(request_dict)
        user.save()

    django_user = User.objects.get(id=user.user_fk)
    django_user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, django_user)

    print('++++++++++++++++++++++++++++++++++++++++++')
    print(user.id, ': ', user.user_fk)
    print('++++++++++++++++++++++++++++++++++++++++++')

    course = Course.objects.filter(id=request_dict.get('custom_course', None))
    if course:
        course = course[0]
    user_role, enroll_created = Role.objects.get_or_create(course=course,
                                           user=django_user, role='Enrolled Student')


    if settings.LTI_DEBUG:
        print "session: is_valid = {}".format( session['is_valid'])
        print "session: message = {}".format( session['message'])
    if not is_valid:
            return render_to_response("error.html",  RequestContext(request))
    #return redirect('AddProblem')
    if user_role:
        return redirect(reverse('ct:study_unit', args=(request_dict.get('custom_course', None),
                                                       request_dict.get('custom_unit', None),)))
    else:
        return redirect(reverse('ct:home'))

@csrf_exempt
def add_problem(request):
    session = request.session
    print(session.keys())
    if session.get('LTI_POST', None):
        try:
            request_post = pickle.loads(session['LTI_POST'])

            request_post['lis_outcome_service_url'] = fix_url(request_post['lis_outcome_service_url'])
            consumer_key = settings.CONSUMER_KEY
            secret = settings.LTI_SECRET
            tool = DjangoToolProvider(consumer_key, secret, request_post)

            result = float(request.POST.get('result'))
            if result == 5:
                score = '1.00'
            else:
                score = '0.00'
            post_result = tool.post_replace_result(score,{'message_identifier':'edX_fix'})
            print post_result.is_success()
            d = dict()
            d['score'] = score
            d['success'] = post_result.is_success()
            d['result'] = result
            d['show'] = True
            return render_to_response("index.html", d,  RequestContext(request))
        except KeyError,e:
            print(str(e))
            return render_to_response("error.html",  RequestContext(request))

def fix_url(str):
    if settings.LTI_URL_FIX:
        for old,new in settings.LTI_URL_FIX.iteritems():
            print(old, new)
            if str.find(old) == 0:
                return u"{}{}".format( new , str[len(old):])
    return str
