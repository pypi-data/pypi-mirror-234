# -*- coding: UTF-8 -*-
# Copyright 2022-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# Some content of this file is explicitly modified by `getlino startproject`.
# Please check for consistency with getlino.startproject.py file before you
# modify anything.

SETUP_INFO = dict(
    name='lino-cms',
    version='23.10.0',
    install_requires=['lino-xl'],
    description=('Manage the content of your website'),
    long_description="""\

**Lino CMS** is a Content Management System à la Lino.

- Source code: https://gitlab.com/lino-framework/cms

- Documentation: https://lino-framework.gitlab.io/cms/

- This project is part of the Lino framework, which is documented
  at https://www.lino-framework.org

- Changelog: https://lino-framework.gitlab.io/cms/changes.html

- For introductions, commercial information and hosting solutions
  see https://www.saffre-rumma.net

- This is a sustainably free open-source project. Your contributions are
  welcome.  See https://community.lino-framework.org for details.


""",
    author='Rumma & Ko Ltd',
    author_email='info@lino-framework.org',
    url="https://gitlab.com/lino-framework/cms",
    license_files=['COPYING'],
    test_suite='tests')

SETUP_INFO.update(classifiers="""
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 1 - Planning
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
Topic :: Database :: Front-Ends
Topic :: Office/Business
Topic :: Software Development :: Libraries :: Application Frameworks
""".format(**SETUP_INFO).strip().splitlines())
SETUP_INFO.update(packages=[
    'lino_cms',
    'lino_cms.lib',
    'lino_cms.lib.cal',
    'lino_cms.lib.cal.fixtures',
    'lino_cms.lib.cms',
    'lino_cms.lib.users',
    'lino_cms.lib.users.fixtures',
])

SETUP_INFO.update(message_extractors={
    'lino_cms': [
        ('**/cache/**', 'ignore', None),
        ('**.py', 'python', None),
        ('**.js', 'javascript', None),
        ('**/config/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(include_package_data=True)

# SETUP_INFO.update(package_data=dict())
#
# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l
#
# l = add_package_data('lino_cms.lib.cms')
# for lng in 'de fr'.split():
#     l.append('lino_cms/lib/cms/locale/%s/LC_MESSAGES/*.mo' % lng)
