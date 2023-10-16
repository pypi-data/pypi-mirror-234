# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['temporian',
 'temporian.beam',
 'temporian.beam.io',
 'temporian.beam.io.test',
 'temporian.beam.operators',
 'temporian.beam.operators.test',
 'temporian.beam.operators.window',
 'temporian.beam.operators.window.test',
 'temporian.beam.test',
 'temporian.core',
 'temporian.core.data',
 'temporian.core.data.test',
 'temporian.core.operators',
 'temporian.core.operators.binary',
 'temporian.core.operators.calendar',
 'temporian.core.operators.scalar',
 'temporian.core.operators.test',
 'temporian.core.operators.window',
 'temporian.core.operators.window.test',
 'temporian.core.test',
 'temporian.implementation',
 'temporian.implementation.numpy',
 'temporian.implementation.numpy.data',
 'temporian.implementation.numpy.data.test',
 'temporian.implementation.numpy.operators',
 'temporian.implementation.numpy.operators.binary',
 'temporian.implementation.numpy.operators.calendar',
 'temporian.implementation.numpy.operators.scalar',
 'temporian.implementation.numpy.operators.test',
 'temporian.implementation.numpy.operators.window',
 'temporian.implementation.numpy.test',
 'temporian.implementation.numpy_cc',
 'temporian.implementation.numpy_cc.operators',
 'temporian.io',
 'temporian.io.test',
 'temporian.proto',
 'temporian.test',
 'temporian.utils',
 'temporian.utils.test']

package_data = \
{'': ['*'],
 'temporian.implementation.numpy.data.test': ['test_data/*'],
 'temporian.test': ['test_data/*', 'test_data/io/*', 'test_data/prototype/*']}

install_requires = \
['absl-py>=1.3.0,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'pandas>=1.5.2',
 'protobuf>=3.20.3']

extras_require = \
{'all': ['apache-beam>=2.48.0,<3.0.0', 'tensorflow>=2.12.0,<3.0.0'],
 'beam': ['apache-beam>=2.48.0,<3.0.0'],
 'tensorflow': ['tensorflow>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'temporian',
    'version': '0.1.5',
    'description': 'Temporian is a Python package for feature engineering of temporal data, focusing on preventing common modeling errors and providing a simple and powerful API, a first-class iterative development experience, and efficient and well-tested implementations of common and not-so-common temporal data preprocessing functions.',
    'long_description': '<img src="https://github.com/google/temporian/raw/main/docs/src/assets/banner.png" width="100%" alt="Temporian logo">\n\n[![pypi](https://img.shields.io/pypi/v/temporian?color=blue)](https://pypi.org/project/temporian/)\n[![docs](https://readthedocs.org/projects/temporian/badge/?version=stable)](https://temporian.readthedocs.io/en/stable/?badge=stable)\n![tests](https://github.com/google/temporian/actions/workflows/test.yaml/badge.svg)\n![formatting](https://github.com/google/temporian/actions/workflows/formatting.yaml/badge.svg)\n![publish](https://github.com/google/temporian/actions/workflows/publish.yaml/badge.svg)\n\nTemporian is an open-source Python library for preprocessing ⚡ and feature engineering 🛠 temporal data 📈 for machine learning applications 🤖. It is a library tailor-made to address the unique characteristics and complexities of time-related data, such as time-series and transactional data.\n\n> Temporal data is any form of data that represents a state in time. In\n> Temporian, temporal datasets contain [events](https://temporian.readthedocs.io/en/stable/user_guide/#events-and-eventsets), which consists of\n> values for one or more attributes at a given timestamp. Common\n> examples of temporal data are transaction logs, sensor signals, and\n> weather patterns. For more, see\n> [What is Temporal data](https://temporian.readthedocs.io/en/stable/user_guide/#what-is-temporal-data).\n\n## Key features\n\n- **Unified data processing** 📈: Temporian operates natively on many forms\n  of temporal data, including multivariate time-series, multi-index\n  time-series, and non-uniformly sampled data.\n\n- **Iterative and interactive development** 📊: Users can easily analyze\n  temporal data and visualize results in real-time with iterative tools like\n  notebooks. When prototyping, users can iteratively preprocess, analyze, and\n  visualize temporal data in real-time with notebooks. In production, users\n  can easily reuse, apply, and scale these implementations to larger datasets.\n\n- **Avoids future leakage** 😰: Future leakage occurs during model training\n  when a model is exposed to data from future events, which leaks information\n  that would otherwise not be available to the model and can result in\n  overfitting. Temporian operators do not create leakage by default. Users\n  can also use Temporian to programmatically detect whether specific signals\n  were exposed to future leakages.\n\n- **Flexible runtime** ☁️: Temporian programs can run seamlessly in-process in\n  Python, on large datasets using [Apache Beam](https://beam.apache.org/).\n\n- **Highly optimized** 🔥: Temporian\'s core is implemented and optimized in\n  C++, so large amounts of data can be handled in-process. In some cases,\n  Temporian is 1000x faster than other libraries.\n\n> **Note**\n> Temporian\'s development is in alpha.\n\n## QuickStart\n\n### Installation\n\nTemporian is available on [PyPI](https://pypi.org/project/temporian/). Install it with pip:\n\n```shell\npip install temporian\n```\n\n### Minimal example\n\nThe following example uses a dataset, `sales.csv`, which contains transactional data. Here is a preview of the data:\n\n```shell\n$ head sales.csv\ntimestamp,store,price,count\n2022-01-01,CA,27.42,61.9\n2022-01-01,TX,98.55,18.02\n2022-01-02,CA,32.74,14.93\n2022-01-15,TX,48.69,83.99\n...\n```\n\nThe following code calculates the weekly sales for each store, visualizes the output with a plot, and exports the data to a CSV file.\n\n```python\nimport temporian as tp\n\ninput_data = tp.from_csv("sales.csv")\n\nper_store = input_data.set_index("store")\nweekly_sum = per_store["price"].moving_sum(window_length=tp.duration.days(7))\n\n# Plot the result\nweekly_sum.plot()\n\n# Save the results\ntp.to_csv(weekly_sum, "store_sales_moving_sum.csv")\n```\n\n![](https://github.com/google/temporian/raw/main/docs/src/assets/frontpage_plot.png)\n\nCheck the [Getting Started tutorial](https://temporian.readthedocs.io/en/stable/tutorials/getting_started/) to try it out!\n\n## Next steps\n\nNew users should refer to the [3 minutes to Temporian](https://temporian.readthedocs.io/en/stable/3_minutes/) page, which provides a\nquick overview of the key concepts and operations of Temporian.\n\nAfter reading the 3 minute guide, visit the [User Guide](https://temporian.readthedocs.io/en/stable/user_guide/) for a deep dive into\nthe major concepts, operators, conventions, and practices of Temporian. For a\nhands-on learning experience, work through the [Tutorials](https://temporian.readthedocs.io/en/stable/tutorials/) or refer to the [API\nreference](https://temporian.readthedocs.io/en/stable/reference/).\n\n## Documentation\n\nThe documentation 📚 is available at [temporian.readthedocs.io](https://temporian.readthedocs.io/en/stable/). The [3 minutes to Temporian ⏰️](https://temporian.readthedocs.io/en/stable/3_minutes/) is the best way to start.\n\n## Contributing\n\nContributions to Temporian are welcome! Check out the [contributing guide](CONTRIBUTING.md) to get started.\n\n## Credits\n\nTemporian is developed in collaboration between Google and [Tryolabs](https://tryolabs.com/).\n',
    'author': 'Mathieu Guillame-Bert, Braulio Ríos, Guillermo Etchebarne, Ian Spektor, Richard Stotz',
    'author_email': 'gbm@google.com',
    'maintainer': 'Mathieu Guillame-Bert',
    'maintainer_email': 'gbm@google.com',
    'url': 'https://github.com/google/temporian',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}
from config.build import *
build(setup_kwargs)

setup(**setup_kwargs)
