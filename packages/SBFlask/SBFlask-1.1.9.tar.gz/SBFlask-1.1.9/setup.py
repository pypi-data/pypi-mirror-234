from setuptools import setup

setup(name='SBFlask',
      version='1.1.9',
      description='SanBlaze Flask webserver for vluns',
      author='Matt Holsey',
      author_email='mholsey@sanblaze.com',
      url='https://www.sanblaze.com/',
      license='SanBlaze Technology ltd',
      packages=['SBFlask', 
				'SBFlask.docs',
				'SBFlask.tests'],
	  install_requires=[
			    'flask',
                'flask_cors',
                'SBKodiak',
                'zeroconf'
		  ],
      include_package_data=True,
      zip_safe=False)