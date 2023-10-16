from setuptools import (setup, find_packages)


def main():
    setup(
        name='pp_paths',
        version='1.0.1',
        author='Sagar Tiwari',
        author_email='iaansagar@gmail.com',
        url='https://github.com/amokfa/pp_paths',
        description='A python program to pretty print directory structures',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        packages=find_packages(),
        entry_points={
            'console_scripts': ['pp_paths = pp_paths.main:main']
        },
        # scripts=['scripts/pp_paths']
    )


if __name__ == '__main__':
    main()
# __magic__
