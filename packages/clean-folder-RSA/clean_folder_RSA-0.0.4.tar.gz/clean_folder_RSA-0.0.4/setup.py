from setuptools import setup, find_namespace_packages

with open('README.md', 'r', encoding = 'utf-8') as fh:
    long_description = fh.read()
    
if __name__ == '__main__':
    setup(
    name='clean_folder_RSA',
    version='0.0.4',
    description='Home work 7 . Clean folder script',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/My-codes-future/project_dz7',
    author='Sergiy Rusetskiy',
    author_email='rusetskit1974s@ukr.net',
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"],
    packages=find_namespace_packages(),
    # package_dir={'':'src'},
    # include_package_data=True,
    entry_points={'console_scripts': ['clean-folder=src.clean_folder_RSA.clean:start']}
)
    