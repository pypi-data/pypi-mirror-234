from atelier.invlib import setup_from_tasks
ns = setup_from_tasks(
    globals(), "synodal",
    test_command='python -m doctest README.rst',
    revision_control_system='git')
