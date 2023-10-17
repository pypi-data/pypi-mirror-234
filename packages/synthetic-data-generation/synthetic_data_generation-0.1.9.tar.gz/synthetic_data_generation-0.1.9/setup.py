from setuptools import setup, find_packages

setup(
    name='synthetic_data_generation',
    version='0.1.9',
    description='Algorithms for generating synthetic data',
    author='Daan Knoors',
    author_email='d.knoors@gmail.com',
    packages=find_packages(include=['synthesis', 'synthesis/**/*.py']),
    install_requires=[
        'diffprivlib==0.6.3',
        'dill==0.3.7',
        'dython==0.6.7',
        'joblib==1.2.0',
        'lifelines==0.27.8',
        'matplotlib==3.7.2',
        'numpy==1.26.0',
        'pandas==2.0.3',
        'pyjanitor==0.26.0',
        'pandas_flavor==0.6.0',
        'scikit_learn==1.3.0',
        'scipy==1.11.3',
        'seaborn==0.13.0',
        'thomas_core==0.1.3'
    ],
    extras_require={'interactive': ['matplotlib>=2.2.0', 'jupyter']},
)