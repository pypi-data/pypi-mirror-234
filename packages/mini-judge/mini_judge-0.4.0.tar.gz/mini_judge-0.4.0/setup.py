# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mini_judge']

package_data = \
{'': ['*'], 'mini_judge': ['example_data/*']}

install_requires = \
['loguru>=0.7.2,<0.8.0',
 'openai>=0.28.1,<0.29.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'python-fire>=0.1.0,<0.2.0',
 'tqdm>=4.66.1,<5.0.0']

entry_points = \
{'console_scripts': ['mini-judge = mini_judge.main:main']}

setup_kwargs = {
    'name': 'mini-judge',
    'version': '0.4.0',
    'description': '',
    'long_description': '<h1 align="center">\n<span>Mini Judge</span>\n</h1>\n\n[![PyPI version](https://badge.fury.io/py/mini-judge.svg)](https://badge.fury.io/py/mini-judge)\n<a href="https://github.com/mrcabbage972/mini-judge/actions/workflows/pre-commit.yml">![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/mrcabbage972/mini-judge/pre-commit.yml?label=pre-commit)</a>\n\n\nSimple implementation of LLM-As-Judge for pairwise evaluation of Q&A models.\n\n# Installation\nInstall the package using pip:\n```pip install mini-judge```\n\n# Usage\nFirst, set the OPENAI_API_KEY environment variable to your OpenAI API key.\nThen, you can run the following command to evaluate the candidate answers in `candidate_answers_path` against the reference answers in `ref_answers_path` using `judge_model` as the judge model.\n```\nmini-judge \\\n--judge_model <judge_model> \\\n--questions_path <questions_path> \\\n--candidate_answers_path <candidate_answers_path> \\\n--ref_answers_path <ref_answers_path> \\\n--output_path <output_path>\n```\n\nTo run a quick demo, use the following command to evaluate the candidate answers in `example_data/candidate_answers.jsonl` against the reference answers in `example_data/ref_answers.jsonl` using GPT-4 as the judge model.\n```\nmini_judge --output_path <output_path>\n```\n# Data Format\nAll input data files are presumed to be in [jsonl](https://jsonlines.org/) format.\n\nThe `candidate_answers` and `ref_answers` files should have each line as a json with an `answer` tag.\n\nSimilarly, the questions file should have json lines with a `question` tag.\n\nAll other tags will be ignored.\n\n# References\nLianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric. P Xing, Hao Zhang, Joseph E. Gonzalez, & Ion Stoica. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena [ArXiv](https://arxiv.org/abs/2306.05685).\n',
    'author': 'mrcabbage972',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
