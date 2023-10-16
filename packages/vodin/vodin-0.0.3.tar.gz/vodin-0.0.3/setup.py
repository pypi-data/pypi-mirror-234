# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odin']

package_data = \
{'': ['*']}

install_requires = \
['gdown', 'supervision', 'torch', 'tqdm', 'ultralytics']

setup_kwargs = {
    'name': 'vodin',
    'version': '0.0.3',
    'description': 'Odin - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Odin\nSuper Fast and super cheap object detection at massive scale in less than 10 lines of code!\n\n# Appreciation\n* Lucidrains\n* Agorians\n\n\n# Install\n`pip install vodin`\n\n# Usage\n\nHere are three examples demonstrating the usage of the `Odin` class from your provided code:\n\n**Example 1: Basic Usage**\n\n```python\n# Import the necessary modules and classes\nfrom odin import Odin\n\n# Initialize the Odin object with paths and thresholds\nodin = Odin(\n    source_weights_path="yolo.weights",\n    source_video_path="input_video.mp4",\n    target_video_path="output_video.mp4",\n    confidence_threshold=0.3,\n    iou_threshold=0.7\n)\n\n# Run the object to process the video\nodin.run()\n```\n\n**Example 2: Custom Parameters**\n\n```python\n# Import the necessary modules and classes\nfrom odin import Odin\n\n# Initialize the Odin object with custom parameters\nodin = Odin(\n    source_weights_path="custom_yolo.weights",\n    source_video_path="input_video.mp4",\n    target_video_path="output_video.mp4",\n    confidence_threshold=0.5,\n    iou_threshold=0.6\n)\n\n# Run the object to process the video\nodin.run()\n```\n\n**Example 3: Advanced Usage**\n\n```python\n# Import the necessary modules and classes\nfrom odin import Odin\n\n# Initialize the Odin object with paths and thresholds\nodin = Odin(\n    source_weights_path="yolo.weights",\n    source_video_path="input_video.mp4",\n    target_video_path="output_video.mp4",\n    confidence_threshold=0.3,\n    iou_threshold=0.7\n)\n\n# Customize further configurations if needed\nodin.tracker.set_max_distance(50)\nodin.box_annotator.set_box_color((0, 255, 0))\nodin.model.set_device("cuda")\n\n# Run the object to process the video\nodin.run()\n```\n\n# Architecture\n* [Odin utilizes YoloV7, weights can be downloaded here](https://drive.google.com/file/d/1yEYFq1jCIpklofMMhuqQKwyTfvj1hLQ1/view)\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/odin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
