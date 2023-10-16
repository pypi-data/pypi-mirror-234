from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='pro_video_ferramentas_Drigody',
    version= 1.0,
    description='Este pacote irá fornecer ferramentas de processamento de vídeo',
    long_description=Path('README.md').read_text(),
    author='Adriana',
    author_email='adrianapcgodoy@gmail.com',
    keywords=['camera','video','processamento'],
    packages=find_packages()
    
)