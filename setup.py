from setuptools import setup
from glob import glob

setup(name='netdisco',
    version='1.0.0',
    scripts=glob('scripts/*'),
    packages = ['netdisco'],
    package_dir = {'netdisco': 'lib'},
    install_requires=[
        "SQLAlchemy >= 0.4",
        "ieeemac",
        ],
    entry_points = {
        'console_scripts': [
            'nd-add     = netdisco.db:add_device_entry',
            'nd-refresh = netdisco.db:refresh_device_entry',
            'nd-wait-for-jobs = netdisco.db:wait_for_jobs',
            'nd-check-device  = netdisco.checkdevice:main',
        ]
    }
) 
