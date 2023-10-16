import setuptools
 
with open("README.md", "r") as fh:
  long_description = fh.read()
 
setuptools.setup(
  name = "loss_mob",
  version = "0.1.10",
  author = "WenSui Liu",
  author_email = "liuwensui@gmail.com",
  description = "Monotonic Optimal Binning for Loss Models",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://github.com/statcompute/loss_mob",
  packages = setuptools.find_packages(),
  install_requires = ['numpy', 'scipy', 'scikit-learn', 'tabulate', 'cytoolz', 'dcor'], 
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
