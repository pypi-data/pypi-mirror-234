from distutils.core import setup
setup(
  name = 'leviosapy',         # This package talks to a Leviosa Zone hub
  packages = ['leviosapy'],   
  version = '0.1.2',           # Use source param in SsdpAdvertisementListener()
  license='APACHE 2.0',        # https://help.github.com/articles/licensing-a-repository
  description = 'AsyncIO compatible library to talk to a Leviosa Motor Shades Zone',   
  author = 'Gerardo Castillo',
  author_email = 'gcastillo@integrahome.net',
  url = 'https://github.com/greg-ha-1990/leviosapy',   
  download_url = 'https://github.com/greg-ha-1990/leviosapy/archive/refs/tags/0.1.2.tar.gz',
  keywords = ['Communication', 'AsyncIO', 'Leviosa Zone'],   
  install_requires=[
          'aiohttp>=3.7.4',
          'async_timeout>=3.0',
          'async_upnp_client>=0.33.0' # This package is also used by HASS for SSDP
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',   # "3 - Alpha", "4 - Beta" or "5 - Production/Stable" 
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)
