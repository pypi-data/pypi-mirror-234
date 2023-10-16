# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bunkatopics',
 'bunkatopics.bunka_logger',
 'bunkatopics.functions',
 'bunkatopics.visualisation']

package_data = \
{'': ['*']}

install_requires = \
['chromadb>=0.4.13,<0.5.0',
 'datasets>=2.14.5,<3.0.0',
 'gensim>=4.3.1,<5.0.0',
 'instructorembedding>=1.0.1,<2.0.0',
 'jupyterlab>=4.0.2,<5.0.0',
 'langchain>=0.0.206,<0.0.207',
 'loguru>=0.7.0,<0.8.0',
 'matplotlib>=3.7.2,<4.0.0',
 'openai>=0.28.0,<0.29.0',
 'pandas>=2.0.2,<3.0.0',
 'plotly>=5.15.0,<6.0.0',
 'pydantic>=1.10.9,<2.0.0',
 'pytest>=7.4.2,<8.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'sentence-transformers>=2.2.2,<3.0.0',
 'streamlit>=1.26.0,<2.0.0',
 'textacy>=0.13.0,<0.14.0',
 'torch>=2.0.1,<3.0.0',
 'umap-learn>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'bunkatopics',
    'version': '0.41',
    'description': 'Advanced Topic Visualization',
    'long_description': '[![PyPI - Python](https://img.shields.io/badge/python-v3.9+-blue.svg)](https://pypi.org/project/bertopic/)\n[![PyPI - PyPi](https://img.shields.io/pypi/v/bunkatopics)](https://pypi.org/project/bunkatopics/)\n[![Downloads](https://static.pepy.tech/badge/bunkatopics)](https://pepy.tech/project/bunkatopics)\n[![Downloads](https://static.pepy.tech/badge/bunkatopics/month)](https://pepy.tech/project/bunkatopics)\n\n# Bunkatopics\n\n<img src="images/logo.png" width="35%" height="35%" align="right" />\n\nBunkatopics is a Topic Modeling Visualisation, Frame Analysis & Retrieval Augmented Generation (RAG) package that leverages LLMs. It is built with the same philosophy as [BERTopic](https://github.com/MaartenGr/BERTopic) but goes deeper in the visualization to help users grasp quickly and intuitively the content of thousands of text, as well as giving the opportunity to the user to create its own frames.\n\nBunkatopics is built on top of [langchain](<https://python.langchain.com/docs/get_started/introduction>).\n\n## Pipeline\n\n<img src="images/pipeline.png" width="70%" height="70%" align="center" />\n\n## Installation\n\n```bash\npip install poetry\ngit clone https://github.com/charlesdedampierre/BunkaTopics.git\ncd BunkaTopics\n\n# Create the environment from the .lock file. \npoetry install # This will install all packages in the .lock file inside a virtual environmnet\n\n# Start the environment\npoetry shell\n```\n\nInstall the spacy tokenizer model for english:\n\n```bash\npython -m spacy download en_core_web_sm\n```\n\n## Quick Start\n\nWe start by Loading Trump data from HuggingFace datasets\n\n```python\n\nfrom bunkatopics.functions.clean_text import clean_tweet\nimport random\nfrom datasets import load_dataset\n\ndataset = load_dataset("rguo123/trump_tweets")["train"]["content"]\nfull_docs = random.sample(dataset, 5000)\nfull_docs = [clean_tweet(x) for x in full_docs] # Cleaning the tweets\nfull_docs = [x for x in full_docs if len(x)>50] # Removing small tweets, they are not informative enough\n\n```\n\nYou can the load any embedding model from langchain. Some of them might be large, please check the langchain [documentation](https://python.langchain.com/en/latest/reference/modules/embeddings.html)\n\n## Topic Modeling\n\n```python\nfrom bunkatopics import Bunka\nfrom langchain.embeddings import HuggingFaceEmbeddings\n\nembedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") # We use a small model\nbunka = Bunka(embedding_model=embedding_model)\nbunka.fit(full_docs)\n\n# Get the list of topics\nbunka.get_topics(n_clusters = 20)\n```\n\nThen, we can visualize the topics computed\n\n```python\nbunka.visualize_topics( width=800, height=800)\n```\n\n<img src="images/newsmap.png" width="70%" height="70%" align="center" />\n\n## Topic Modeling with GenAI Summarization of Topics\n\nYou can get the topics summarized by Generative AI.\nUse any model from Langchain. We use the 7B-instruct model of [Mistral AI](<https://mistral.ai/news/announcing-mistral-7b/>) thought [llama.cpp](<https://github.com/ggerganov/llama.cpp>) and the [langchain integration](<https://python.langchain.com/docs/integrations/llms/llamacpp>).\n\n```python\nfrom langchain.llms import LlamaCpp\n\n\ngenerative_model = LlamaCpp(\n    model_path=MODEL_PATH # Add the path on your local computer\n    n_ctx=2048,\n    temperature=0.75,\n    max_tokens=2000,\n    top_p=1,\n    verbose=False,\n) \ngenerative_model.client.verbose = False\n\nbunka.get_clean_topic_name(generative_model = generative_model)\nbunka.visualize_topics( width=800, height=800)\n\n```\n\n<img src="images/newsmap_clean.png" width="70%" height="70%" align="center" />\n\n## Retrieval Augmented Generation (RAG)\n\nIt is possible to to Retrieval Augmented Generation (RAG) thanks to langchain integration with different Generative Models.\n\n```python\nquery = \'What is the  main fight of Donald Trump ?\'\nres = bunka.rag_query(query = query, generative_model = generative_model, top_doc = 5)\nprint(res[\'result\'])\n```\n\nOUTPUT:\n\n- The main fight of Donald Trump in the presidential elections of 2016 was against Hillary Clinton. He believed he was the best candidate for president and was able to beat many other candidates in the field due to his fame and political opinions.\n\n```python\nfor doc in res[\'source_documents\']:\n    text = doc.page_content.strip()\n    print(text)\n```\n\nOUTPUT:\n\n- what do you say donald  run for president\n- why only donald trump can beat hillary/n\n- via    donald trump on who he likes for president  donald trump/n\n- if the 2016  presidential field is so deep  why is donaldtrump beating so many of their  stars\n- donald trump is a respected businessman with insightful political opinions\n\n## Bourdieu Map\n\nThe Bourdieu map display the different texts on a 2-Dimensional unsupervised scale. Every region of the map is a topic described by its most specific terms.\nCLusters are created and the names are also summarized using Generative AI.\n\nThe power of this visualisation is to constrain the axis by creating continuums and looking how the data distribute over these continuums. The inspiration is coming from the French sociologist Bourdieu, who projected items on [2 Dimensional maps](https://www.politika.io/en/notice/multiple-correspondence-analysis).\n\n```python\nbunka.visualize_bourdieu(\n    generative_model=generative_model,\n    x_left_words=["war"],\n    x_right_words=["peace"],\n    y_top_words=["men"],\n    y_bottom_words=["women"],\n    height=800,\n    width=800,\n    label_size_ratio_label=50,\n    display_percent=True,\n    clustering=True,\n    topic_n_clusters=10,\n    topic_terms=5,\n    topic_top_terms_overall=500,\n    topic_gen_name=True,\n)\n\nbourdieu_fig.show()\n```  \n\n<img src="images/bourdieu.png" width="70%" height="70%" align="center" />\n\n## One-dimentional Map\n\nIt is possible to display only the distribution of the data in one continnum\n\n```python\nbunka.visualize_bourdieu_one_dimension(\n    left=["negative", "bad"],\n    right=["positive"],\n    width=600,\n    height=600,\n    explainer=False,\n)\n\nfig_solo.show()\n```\n\n<img src="images/bourdieu_one_dimension.png" width="70%" height="70%" align="center" />\n\n## Streamlit\n\nRun Streamlit to use BunkaTopics with a nice front-end.\n\n```bash\npython -m streamlit run streamlit/app.py \n```\n\n## Multilanguage\n\nThe package use Spacy to extract meaningfull terms for the topic represenation.\n\nIf you wish to change language to french, first, download the corresponding spacy model:\n\n```bash\npython -m spacy download fr_core_news_lg\n```\n\n```python\nembedding_model = HuggingFaceEmbeddings(model_name="distiluse-base-multilingual-cased-v2")\n\nbunka = Bunka(embedding_model=embedding_model, language = \'fr_core_news_lg\')\n\nbunka.fit(full_docs)\nbunka.get_topics(n_clusters = 20)\n```  \n\n## Functionality\n\nHere are all the things you can do with Bunkatopics\n\n### Common\n\nBelow, you will find an overview of common functions in Bunkatopics.\n\n| Method | Code  |\n|-----------------------|---|\n| Fit the model    |  `.fit(docs)` |\n| Fit the model and get the topics  |  `.fit_transform(docs)` |\n| Acces the topics   | `.get_topics(n_clusters=10)`  |\n| RAG   | `.rag_query(query, generative_model)`  |\n| Access the top documents per topic    |  `.get_clean_topic_name()` |\n| Access the distribution of topics   |  `.get_topic_repartition()` |\n| Visualize the topics on a Map |  `.visualize_topics()` |\n| Visualize the topics on Natural Language Supervised axis | `.visualize_bourdieu()` |\n| Access the Coherence of Topics |  `.get_topic_coherence()` |\n| Get the closest documents to your search | `.search(\'politics\')` |\n\n### Attributes\n\nYou can access several attributes\n\n| Attribute | Description |\n|------------------------|---------------------------------------------------------------------------------------------|\n| `.docs`               | The documents stores as a Document pydantic model |\n| `.topics` | The Topics stored as a Topic pydantic model. |\n',
    'author': 'Charles De Dampierre',
    'author_email': 'charlesdedampierre@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
