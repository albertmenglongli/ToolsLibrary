"""
Usage:

==================model/student.py================
from django.db import models

class Group(model.Model):
    pass

class Student(models.Model):
    name = models.CharField(_('name'), max_length=20)
    group = models.ForeignKey(Group, related_name='students')

===================admin.py=======================

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'related_group']

    @admin_foreign_key_link(field='group')
    def related_group(self, obj):
        pass

admin.site.register(Student, StudentAdmin)
"""

from functools import wraps


def admin_foreign_key_link(field):
    def decorator(func):
        @wraps(func)
        def wrapper(self, obj):
            result = func(self, obj)
            if result:
                # if function return something, we do nothing and just return;
                return result

            # most of the cases will trigger this ELSE branch;
            from django.template import Context, Template
            from django.core.urlresolvers import reverse
            from django.contrib.admin.utils import quote

            assert hasattr(obj, field)

            _field_attr = getattr(obj, field, None)
            if _field_attr is None:
                _django_template = Template('')
                _context = Context()
            else:
                _description = '{{name}} {{id}}'
                _str_template = '<a href="{{url}}">%s</a>' % _description
                _django_template = Template(_str_template)
                _pk_value = _field_attr.id
                url = reverse(
                    'admin:%s_%s_change' % (_field_attr.__class__._meta.app_label,
                                            _field_attr.__class__.__name__.lower()),
                    args=(quote(_pk_value),),
                    current_app=self.admin_site.name,
                    )
                _context = Context({'url': url,
                                    'name': _field_attr.__class__._meta.verbose_name.title(),
                                    'id': _pk_value
                                    })
            return _django_template.render(_context)

        return wrapper

    return decorator
