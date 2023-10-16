from setuptools import setup, find_packages

setup(
    name="zmq_ai_client_python",
    version="1.2.0",
    packages=find_packages(),
    package_data={'zmq_ai_client_python': ['schema/*']},
    author="Fatih GENÇ",
    author_email="f.genc@qimia.de",
    description="A ZMQ client interface for llama server",
    long_description="A ZMQ client interface for llama server",
    url="http://github.com/zmq-ai-client-python",
    install_requires=[
        "pyzmq",
        "msgpack",
        "notebook",
        "pytest"
    ],
)
