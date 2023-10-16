from atelier.invlib import setup_from_tasks
ns = setup_from_tasks(
    globals(), "lino_cms",
    languages="en de fr".split(),
    # tolerate_sphinx_warnings=True,
    locale_dir='lino_cms/lib/cms/locale',
    revision_control_system='git',
    cleanable_files=['docs/api/lino_cms.*'])
