from setuptools import find_packages, setup
import os
from collections import defaultdict

package_name = 'iris'

def collect_files_subdirs(base_dir):
    file_list = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, base_dir)
            file_list.append((full_path, rel_path))
    return file_list

def collect_if_exists(dir_path):
    if os.path.isdir(dir_path):
        return [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
    return []

# Collect models, worlds, etc. (same method as before)
model_files = collect_files_subdirs('models')
world_files = collect_files_subdirs('worlds')
config_files = collect_if_exists('config')
rviz_files = collect_if_exists('rviz')

# --- Fix: Collect launch files, preserving subfolders ---
launch_files_full = collect_files_subdirs('launch')

data_files_dict = defaultdict(list)

for full_path, rel_path in model_files:
    dest_dir = os.path.join('share', package_name, 'models', os.path.dirname(rel_path))
    data_files_dict[dest_dir].append(full_path)

for full_path, rel_path in world_files:
    dest_dir = os.path.join('share', package_name, 'worlds', os.path.dirname(rel_path))
    data_files_dict[dest_dir].append(full_path)

# Fix: For launch files, preserve subdirectory structure under launch/
for full_path, rel_path in launch_files_full:
    dest_dir = os.path.join('share', package_name, 'launch', os.path.dirname(rel_path))
    data_files_dict[dest_dir].append(full_path)

data_files_list = [
    ('share/ament_index/resource_index/packages', [f'resource/{package_name}']),
    (f'share/{package_name}', ['package.xml']),
    (f'share/{package_name}/config', config_files),
    (f'share/{package_name}/rviz', rviz_files),
    (f'share/{package_name}/env-hooks', ['env-hooks/iris.dsv']),
]

for dest_dir, files in data_files_dict.items():
    data_files_list.append((dest_dir, files))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files_list,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='srimman Maheswaran',
    maintainer_email='learningwithsri@gmail.com',
    description='This package is called Ardupilot Navigation Object also known as ANO for students to try out ardupilot without complicating things.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={},
)