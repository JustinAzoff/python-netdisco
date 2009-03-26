from setuptools import setup
from glob import glob

setup(name='netdisco',
    version='0.9.9',
    scripts=glob('scripts/*'),
    packages = ['netdisco'],
    package_dir = {'netdisco': 'lib'},
    install_requires=[
        "SQLAlchemy >= 0.4",
        "ieeemac",
        ],
    entry_points = {
        'console_scripts': [
            'netdisco-add     = netdisco.db:add_device_entry',
            'netdisco-refresh = netdisco.db:refresh_device_entry',
            'netdisco-wait-for-jobs = netdisco.db:wait_for_jobs',
            'netdisco-check-device  = netdisco.checkdevice:main',
        ]
    }
) 
