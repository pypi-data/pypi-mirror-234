import setuptools

version = '0.8.10'

if __name__ == '__main__':
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        name='dicomselect',
        version=version,
        author_email='Stan.Noordman@radboudumc.nl',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/DIAGNijmegen/dicomselect',
        project_urls={
            "Bug Tracker": "https://github.com/DIAGNijmegen/dicomselect"
        },
        license='MIT License',
        install_requires=[
            'pydicom~=2.3.1',
            'SimpleITK~=2.2.1',
            'tqdm~=4.65.0',
            'pandas~=2.0.0',
            'pylibjpeg~=1.4.0',
            'pylibjpeg-libjpeg~=1.3.4',
            'rapidfuzz~=3.0.0',
            'python-Levenshtein~=0.21.0',
            'treelib~=1.6.4'
        ],
        extras_require={
            'dev': [
                'pytest',
                'flake8',
            ]
        },
    )
