from setuptools import setup, find_packages

setup(
    name='up_jsprit',
    version='1.0.0',
    packages=find_packages(include=['up_jsprit', 'jar', 'output']),
    package_data={
        'up_jsprit': ['jar/*.jar'],
    },
    install_requires=[
        'jpype1', 'unified_planning', 'typing', 'requests', 'folium', 'polyline' # and other dependencies
    ],
    author='Paolo Petrinca',
    author_email='up_jsprit@gmail.com',
    description='Liabray for Integration of JSprit toolkit with Unified Planning Library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ppablo78/up-jsprit',  # if you have a github repo
        classifiers=[
        'Programming Language :: Python :: 3',
        # other classifiers
    ],
)
