from setuptools import setup, find_packages
setup(
    name='gui1.py',
    version='1.0.0',
    description='Board with GUI',
    author='Meera',
    packages=find_packages(),
    install_requires=[
        'Pillow>=8.0.0',  # Pillow is the Python Imaging Library used for image processing
    ],
    package_data={
        'main': ['SimpleIO-UM.dll'],  # Replace 'your_package_name' with the actual package name
    },
)