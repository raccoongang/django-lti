import json
from django.db import models
from django.apps import apps
from django.contrib.auth import login
from django.contrib.auth.models import User

from ct.models import Role, Course

if apps.is_installed('social.apps.django_app.default'):
    SOCIAL = True
    from social.apps.django_app.default.models import UserSocialAuth



class LTIUser(models.Model):
    user_id = models.CharField(max_length=255, blank=False)
    consumer = models.CharField(max_length=64, blank=True)
    extra_data = models.CharField(max_length=1024, blank=False)
    django_user = models.ForeignKey(User, null=True)

    class Meta:
        unique_together = ('user_id', 'consumer')

    def create_links(self):
        extra_data = json.loads(self.extra_data)
        username = extra_data.get('lis_person_name_given', self.user_id)
        first_name = extra_data.get('lis_person_name_given', '')
        last_name = extra_data.get('lis_person_name_family', '')
        email = extra_data.get('lis_person_contact_email_primary', '')
        django_user, created = User.objects.get_or_create(username=username, first_name=first_name,
                                                          last_name=last_name, email=email)
        self.django_user = django_user
        self.save()

        if SOCIAL:
            consumer_name = extra_data.get('tool_consumer_info_product_family_code', 'lti')
            social, created = UserSocialAuth.objects.get_or_create(user=self.django_user,
                                                                   provider=consumer_name,
                                                                   uid=self.user_id)
            social.extra_data=self.extra_data
            social.save()

    def login(self, request):
        if self.django_user:
            self.django_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, self.django_user)

    def enroll(self, request_dict):
        role = request_dict.get('roles', 'Enrolled Student')
        course = Course.objects.filter(id=request_dict.get('custom_course', 1))
        if course:
            course = course[0]
        user_role, enroll_created = Role.objects.get_or_create(course=course,
                                                               user=self.django_user,
                                                               role=role)

    def is_enrolled(self, request_dict):
        role = Role.objects.filter(course=request_dict.get('custom_course', 1),
                                   user=self.django_user,
                                   role=request_dict.get('roles', 'Enrolled Student'))
        return len(role) > 0


    @property
    def is_linked(self):
        return self.django_user
