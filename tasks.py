from invoke import task

from src.chdman_gui.main import main


# Python reqs
@task
def update_app_reqs(c):
    c.run("pip-compile src/requirements.in")


@task
def update_combined_reqs(c):
    c.run(
        "pip-compile src/requirements.in requirements-dev.in -o requirements-combined.txt"
    )


@task
def run(c):
    main()


@task
def compile(c):
    c.run(
        "nuitka --onefile --include-data-dir=src/chdman_gui/resources=chdman_gui/resources --plugin-enable=pyside6 src/chdman_gui/main.py"
    )
