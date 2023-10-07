from setuptools import setup, find_packages


setup(
    name='mkdocs-strapi-plugin',
    version='0.1.0',
    description='This plugin is designed to fetch data from Strapi API and inject that data into the mkdocs.',
    long_description='',
    keywords='mkdocs',
    url='',
    author='Isah Enema Jacob',
    author_email='isahjacob0@gmail.com',
    license='MIT',
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1.0.4',
        'requests>=2.22.0'
    ],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-strapi-plugin = mkdocs_strapi_plugin.plugin:StrapiMkdocsPlugin'
        ]
    }
)
