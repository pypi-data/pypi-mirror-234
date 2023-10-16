from setuptools import setup, find_packages

setup(
    name='am_imaging',
    version='0.1.1',
    packages=find_packages(include=['am_imaging', 'am_imaging.*']),
    install_requires=[
        'numpy',
        'opencv-python',
    ],
    author='Aaron Moffatt, GPT',
    author_email = 'a@airvr.studio',
    description='Utility functionse for processing images and video',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # url='https://github.com/your_github_username/your_package_name',
    # classifiers=[
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.6',
    #     'Programming Language :: Python :: 3.7',
    #     'Programming Language :: Python :: 3.8',
    # ],
)
