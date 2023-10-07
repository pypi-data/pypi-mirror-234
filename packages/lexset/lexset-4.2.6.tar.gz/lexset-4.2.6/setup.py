from setuptools import setup


setup(name='lexset',
      version='4.2.6',
      author='F. Bitonti',
      author_email='Francis@lexset.ai',
      license='Apache 2.0',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3'
      ],
      packages=['lexset'],
      install_requires=[
          'pyjson',
          'PyYAML',
          'pyBase64',
          'tqdm',
          'requests',
          'matplotlib',
          'numpy',
          'opencv-python',
          'scikit-image',
          'scikit-learn',
          'tensorflow'
      ]
)
