import setuptools
from setuptools import setup

install_deps = ['numpy>=1.22.4', 'scipy', 'natsort',
                'tifffile', 'tqdm', 'numba', 
                'torch>=1.6',
                'opencv-python-headless>4.5.5.64', 
                'fastremap', 'imagecodecs'
                ]

gui_deps = [
        'pyqtgraph>=0.12.4', 
        'PyQt6', 
        'PyQt6.sip',
        'google-cloud-storage',
        'omnipose-theme',
        # 'PyQtDarkTheme@git+https://github.com/kevinjohncutler/omnipose-theme#egg=PyQtDarkTheme',
        'superqt','colour','darkdetect'
        ]

docs_deps = [
        'sphinx>=3.0',
        'sphinxcontrib-apidoc',
        'sphinx_rtd_theme',
        ]

omni_deps = [
        'scikit-image', 
        'scikit-learn',
        'edt',
        'torch_optimizer', 
        'ncolor'
        # 'ncolor@git+https://github.com/kevinjohncutler/ncolor#egg=ncolor'
        ]

distributed_deps = [
        'dask',
        'dask_image',
        'scikit-learn',
        ]

acdc_deps = install_deps.copy()
acdc_deps.extend(omni_deps)

# conda install numba numpy tifffile imagecodecs scipy fastremap pyqtgraph
#  pip install opencv-python==4.5.3.56 

try:
    import torch
    a = torch.ones(2, 3)
    version = int(torch.__version__[2])
    if version >= 6:
        install_deps.remove('torch')
except:
    pass

with open("README.md", "r") as fh:
    long_description = fh.read()
    
    
setup(
    name="cellpose-omni-acdc",
    license="BSD",
    author="Francesco Padovani",
    author_email="padovaf@tcd.ie",
    description="cellpose fork developed for omnipose",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kevinjohncutler/cellpose",
    setup_requires=[
      'pytest-runner',
      'setuptools_scm',
    ],
    packages=setuptools.find_packages(),
    use_scm_version=True,
    install_requires = acdc_deps,
    tests_require=[
      'pytest'
    ],
    extras_require = {
      'omni': omni_deps,
      'docs': docs_deps,
      'gui': gui_deps,
      'all': gui_deps + omni_deps,
      'distributed': distributed_deps,
    },
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ),
     entry_points = {
        'console_scripts': [
          'cellpose = cellpose.__main__:main']
     }
)
