from setuptools import (setup, find_packages)


def main():
    setup(
        name='pp_paths',
        version='1.0.0',
        author='Sagar Tiwari',
        author_email='iaansagar@gmail.com',
        description='A python program to pretty print directory structures',
        packages=find_packages(),
        entry_points={
            'console_scripts': ['pp_paths = pp_paths.main:main']
        },
        # scripts=['scripts/pp_paths']
    )


if __name__ == '__main__':
    main()
# __magic__
