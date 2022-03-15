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
