from distutils.core import setup
setup(name='bashcutter',
      version='0.1',
      url='https://github.com/dekelund/bashcutter',
      #py_modules=['bashcutter'],
      author = 'Daniel Ekelund',
      author_email = 'contact [at] danielekelund.info',
      packages=['bashcutter'],
      scripts=['bin/bashcutter', 'bin/cb', 'bin/lb', 'bin/mb', 'bin/pb', 'bin/rmb', 'bin/xb'],
      )

