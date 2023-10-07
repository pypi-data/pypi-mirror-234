from setuptools import setup

setup(name='miquido_infra_spawner',
      include_package_data=True,
      version='0.0.13',
      description='The funniest joke in the world',
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
