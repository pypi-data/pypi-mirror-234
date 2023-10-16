===========================
Django rps.Milea Framework
===========================

Installation
============

* Installation ::

    pip install rps-milea-framework


* Add this at the end of settings.py ::

    # Init Milea Framework
    INSTALLED_APPS = [
        # Framwork
        'rps_milea',

        # Django
        'django.forms',

        # Third Party
        'email_users',
        'adminsortable2',

    ] + INSTALLED_APPS

    FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
    AUTH_USER_MODEL = 'email_users.User'


* Database Update ::

    python manage.py migrate


Internal Notes
==============

Publishing to PyPI::

	python -m pip install -U wheel twine setuptools
	python setup.py sdist
	python setup.py bdist_wheel
	python -m twine upload --skip-existing dist/*
