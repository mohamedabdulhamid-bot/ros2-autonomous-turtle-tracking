import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'turtle_tracking_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # This line ensures your launch files are copied to the install space
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abdulhamid',
    maintainer_email='eng.mohamed.abdulhamid404@gmail.com',
    description='Autonomous turtle tracking using turtlesim',
    license='Apache-2.0', # Updated from TODO
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'turtle_spawner_node=turtle_tracking_pkg.turtle_spawner:main',
            'turtle_controller_node=turtle_tracking_pkg.turtle_controller_:main', 
        ],
    },
)