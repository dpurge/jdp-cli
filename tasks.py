from invoke import task
from pathlib import Path

modules = [x for x in Path('src').iterdir() if x.is_dir()]

@task
def clean(c):
    for module in modules:
        print("Cleaning module: {name}".format(name = module.name))
        items = (module/x for x in (
            'dist',
            'build',
            '.eggs',
            'jdp_{name}.egg-info'.format(name = module.name)))
        for item in items:
            if item.exists():
                item_path = item.absolute()
                print("  Deleting: {item}".format(item = item_path))
                c.run("rmdir /s /q {item}".format(item = item_path))

@task
def build(c):
    for module in modules:
        module_path = module.absolute()
        print('Building module: {name}'.format(name = module_path))
        with c.cd(module_path):
            c.run('python setup.py bdist_wheel')

@task
def develop(c):
    for module in modules:
        module_path = module.absolute()
        print('Install module for develop: {name}'.format(name = module_path))
        with c.cd(module_path):
            c.run('python setup.py develop')
