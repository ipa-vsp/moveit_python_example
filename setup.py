import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'moveit_python_examples'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ipa326',
    maintainer_email='vishnu.pbhat93@gmail.com',
    description='Python (moveit_py) motion planning API examples for the rox_fr3 arm.',
    license='BSD-3-Clause',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'motion_planning_api = moveit_python_examples.motion_planning_api:main',
        ],
    },
)
