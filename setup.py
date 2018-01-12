from setuptools import setup


install_requires = ['scipy==0.19.1',
					'numpy==1.13.1',
					'tensorflow==1.3.0',
					'scikit_learn==0.19.1',
					'Keras==2.0.6']

setup(name='robotsearch',
      author='Iain Marshall',
      author_email="mail@ijmarshall.com",
      version='0.0.1',
      install_requires=install_requires,
      entry_points = {
    	'console_scripts': [
        'robotsearch = robotsearch:main',
    	]},
      packages=setuptools.find_packages(),
)