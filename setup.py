import setuptools
import changeling.metadata


def parse_requirements():
    return open('requirements.txt').readlines()


setuptools.setup(
    name='changeling',
    version=changeling.metadata.VERSION,
    packages=['changeling'],
    install_requires=parse_requirements(),
    entry_points={
        'console_scripts': [
            'changeling-server = changeling.server:run',
        ],
    },
)
