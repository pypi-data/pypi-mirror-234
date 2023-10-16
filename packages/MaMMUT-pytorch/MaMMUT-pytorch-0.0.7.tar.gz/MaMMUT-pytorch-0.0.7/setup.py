from setuptools import setup, find_packages

setup(
  name = 'MaMMUT-pytorch',
  packages = find_packages(exclude=[]),
  version = '0.0.7',
  license='MIT',
  description = 'MaMMUT - Pytorch',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/lucidrains/MaMMUT-pytorch',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'multimodal',
    'attention mechanism',
    'contrastive learning'
  ],
  install_requires=[
    'einops>=0.6.1',
    'torch>=1.6',
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
