from setuptools import setup

setup(name='miquido_infra_spawner',
      include_package_data=True,
      version='0.0.15',
      description='This project is meant to automate creation of new terraform repositories. Running the script will create a git repo in miquidos gitlab and start the pipeline deploying new environment',
      author_email='marek.moscichowski@miquido.com',
      author='Marek',
      license='MIT',
      packages=['miquido_infra_spawner'],
      zip_safe=False,
      install_requires=[
          'requests',
          'python-dateutil'
      ]
      )
