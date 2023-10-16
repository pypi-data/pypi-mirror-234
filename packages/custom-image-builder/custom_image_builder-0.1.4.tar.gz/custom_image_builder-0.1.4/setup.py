# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['custom_image_builder', 'custom_image_builder.exception']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2==3.1.2',
 'MarkupSafe==2.1.3',
 'PyJWT==2.8.0',
 'certifi==2023.7.22',
 'cffi==1.15.1',
 'charset-normalizer==3.2.0',
 'cryptography==41.0.3',
 'globus-compute-sdk==2.2.0',
 'idna==3.4',
 'packaging==23.1',
 'pika==1.3.2',
 'pycparser==2.21',
 'pydantic==1.10.12',
 'requests==2.31.0',
 'tblib==1.7.0',
 'texttable==1.6.7',
 'typing_extensions==4.7.1',
 'urllib3==2.0.4',
 'websockets==10.3']

setup_kwargs = {
    'name': 'custom-image-builder',
    'version': '0.1.4',
    'description': 'A python package that enables user to build their custom singularity image on HPC cluster',
    'long_description': '# Building a singular container for HPC using globus-compute\n\n## Context\n* One of the execution configurations of [globus-compute](https://www.globus.org/compute) requires a registered container which is spun up to execute the user function on the HPC.\n\n* HPCs do not run docker containers(due to security reasons as discussed [here](https://docs.vscentrum.be/software/singularity.html)) and support only an apptainer/singularity image.\n\n* Installing the apptainer setup to build the singularity image locally is not a straightforward process especially on windows and mac systems as discussed in the [documentation](https://apptainer.org/docs/admin/main/installation.html).\n\nUsing this python library the user can specify their custom image specification to build an apptainer/singularity image \nwhich would be used to in-turn to run their functions on globus-compute. The library registers the container and \nreturns the container id which would be used by the globus-compute executor to execute the user function.\n\n\n## Prerequisite.\nA [globus-compute-endpoint](https://globus-compute.readthedocs.io/en/latest/endpoints.html) setup on HPC cluster.\n\nThe following steps can be used to create an endpoint on the NCSA Delta Cluster, you can modify the configurations based on your use-case:\n\n1. Create a conda virtual env. We have created a ```custom-image-builder``` conda env on the delta cluster as follows:\n```shell\nconda create --name custom-image-builder python=3.11\n\nconda activate custom-image-builder\n\npip install globus-compute-endpoint==2.2.0\n\npip install custom-image-builder\n```\n\n2. Creating a globus-compute endpoint:\n\n```shell\nglobus-compute-endpoint configure custom-image-builder\n```\n\nUpdate the endpoint config at ```~/.globus_compute/custom-image-builder/config.py``` to :\n```python\n\nfrom parsl.addresses import address_by_interface\nfrom parsl.launchers import SrunLauncher\nfrom parsl.providers import SlurmProvider\n\nfrom globus_compute_endpoint.endpoint.utils.config import Config\nfrom globus_compute_endpoint.executors import HighThroughputExecutor\n\n\nuser_opts = {\n    \'delta\': {\n        \'worker_init\': \'conda activate custom-image-builder\',\n        \'scheduler_options\': \'#SBATCH --account=bbmi-delta-cpu\',\n    }\n}\n\nconfig = Config(\n    executors=[\n        HighThroughputExecutor(\n            max_workers_per_node=10,\n            address=address_by_interface(\'hsn0\'),\n            scheduler_mode=\'soft\',\n            worker_mode=\'singularity_reuse\',\n            container_type=\'singularity\',\n            container_cmd_options="",\n            provider=SlurmProvider(\n                partition=\'cpu\',\n                launcher=SrunLauncher(),\n\n                # string to prepend to #SBATCH blocks in the submit\n                # script to the scheduler eg: \'#SBATCH --constraint=knl,quad,cache\'\n                scheduler_options=user_opts[\'delta\'][\'scheduler_options\'],\n                worker_init=user_opts[\'delta\'][\'worker_init\'],\n                # Command to be run before starting a worker, such as:\n                # \'module load Anaconda; source activate parsl_env\'.\n\n                # Scale between 0-1 blocks with 2 nodes per block\n                nodes_per_block=1,\n                init_blocks=0,\n                min_blocks=0,\n                max_blocks=1,\n\n                # Hold blocks for 30 minutes\n                walltime=\'00:30:00\'\n            ),\n        )\n    ],\n)\n```\n\n3. Start the endpoint and store the endpoint id to be used in the following example\n\n```shell\nglobus-compute-endpoint start custom-image-builder\n```\n\n\n## Example\n\nConsider the following use-case where the user wants to execute a pandas operation on HPC using globus-compute.\nThey need a singularity image which would be used by the globus-compute executor. The library can be leveraged as follows:\n\nLocally you need to install the following packages, you can create a virtual env as follows:\n\n\n```shell\ncd example/\n\npython3.9 -m venv venv\n\nsource venv/bin/activate\n\npip install globus-compute-sdk==2.2.0\n\npip install custom-image-builder\n```\n\n\n```python\nfrom custom_image_builder import build_and_register_container\nfrom globus_compute_sdk import Client, Executor\n\n\ndef transform():\n    import pandas as pd\n    data = {\'Column1\': [1, 2, 3],\n            \'Column2\': [4, 5, 6]}\n\n    df = pd.DataFrame(data)\n\n    return "Successfully created df"\n\n\ndef main():\n    image_builder_endpoint = "81b21a94-0e18-457d-98b5-05672a8a3b60"\n    gcc_client = Client()\n\n    container_id = build_and_register_container(gcc_client=gcc_client,\n                                                endpoint_id=image_builder_endpoint,\n                                                image_file_name="my-pandas-image",\n                                                base_image_type="docker",\n                                                base_image="python:3.8",\n                                                pip_packages=["pandas"])\n\n    print("The container id is", container_id)\n\n    example_endpoint = "0b4e042b-edd5-4951-9ce5-6608c2ef6cb8"\n\n    with Executor(endpoint_id=example_endpoint,\n                  container_id="791a75b4-c2bd-40f1-85e0-ba17458c233b") as ex:\n        fut = ex.submit(transform)\n\n    print(fut.result())\n```\n\n\n## Note.\nFor the following example to work we must use the globus-compute-sdk version of 2.2.0 while setting up our endpoint.\n\nThe singularity image require globus-compute-endpoint as one of its packages in-order to run the workers as our custom \nsingularity container, hence by default we require python as part of the image inorder to install globus-compute-endpoint. \n',
    'author': 'ritwik-deshpande',
    'author_email': 'ritwikdeshpande01@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
