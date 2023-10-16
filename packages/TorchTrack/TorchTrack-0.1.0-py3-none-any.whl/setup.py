from setuptools import find_packages, setup

setup(
    name="torch_track",
    packages=find_packages(include=["torch_track"]),
    version="0.1.0",
    description="TorchTrack takes your models data and training data then send it to the TrackML web application",
    author="NeuralNuts",
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='test',
)
