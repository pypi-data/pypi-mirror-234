from setuptools import setup, find_packages

setup(
    name='poseutil',
    version='0.2.8',
    description='pose engine utils',
    author='jyj902',
    author_email='jyj902@naver.com',
    url='',
    requires=['sklearn','pandas','numpy','cv2','pickle'],
    py_modules=['utils'],
    packages=['utils'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
