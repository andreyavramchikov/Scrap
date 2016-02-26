from fabric.api import env, run
from fabric.operations import sudo

# env.hosts = ['127.0.0.1:2222']
# env.user = 'vagrant'
# env.key_filename = '/home/andrey/Dropbox/playtogether/.vagrant/machines/default/virtualbox/private_key'
env.user = 'ubuntu'
env.hosts = [
    'ec2-54-209-133-98.compute-1.amazonaws.com'
]

# git@github.com:andreyavramchikov/Scrap.git

env.key_filename = '/home/andrey/Playtogether.pem'

env.project_name = 'Scrap'
env.path = '/home/ubuntu/projects_2/%(project_name)s' % env
# env.path = '/home/vagrant/projects/%(project_name)s' % env
env.env_path = '%(path)s/env' % env
env.repo_path = '%(path)s/repository' % env

# ssh -i ~/Playtogether.pem ubuntu@ec2-54-209-133-98.compute-1.amazonaws.com


def setup():
    # STILL NEED TO INSTALL MANUALLY MYSQL AND PYTHON-MYSQL ETC
    sudo('apt-get -y update ')
    sudo('apt-get -y upgrade')
    sudo('apt-get -y install python-dev')
    sudo('apt-get -y install python-virtualenv')
    sudo('apt-get -y install libmysqlclient-dev')
    sudo('pip install virtualenvwrapper')  # must update .bashrc still manually
    run('source ~/.bashrc')
    run('mkvirtualenv scrapping --no-site-packages')
    run('source ~/.virtualenvs/playtogether/bin/activate')


def deploy():
    # sudo('rm -rf projects')  # MUST REMOVE IT
    sudo('apt-get install git')
    setup_directories()
    setup_virtualenv()
    clone_repo()
    install_requirements()

    run('source %(env_path)s/bin/activate; %(env_path)s/bin/python %(repo_path)s/manage.py migrate' % env)
    # run('source %(env_path)s/bin/activate; %(env_path)s/bin/python %(repo_path)s/manage.py collectstatic' % env)


def install_requirements():
    """
    Install the required packages using pip.
    """
    run('source %(env_path)s/bin/activate; pip install -r %(repo_path)s/requirements.txt' % env)


def clone_repo():
    """
    Do initial clone of the git repository.
    """
    run('git clone https://github.com/andreyavramchikov/%(project_name)s.git %(repo_path)s' % env)


def setup_directories():
    """
    Create directories necessary for deployment.
    """
    run('mkdir -p %(path)s' % env)
    run('mkdir -p %(env_path)s' % env)


def activate_virtualenv():
    run('source %(env_path)s/bin/activate;' % env)


def setup_virtualenv():
    """
    Setup a fresh virtualenv.
    """
    run('virtualenv %(env_path)s --no-site-packages;' % env)
    run('source %(env_path)s/bin/activate;' % env)
