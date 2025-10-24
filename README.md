# coronerLite

Welcome to **coronerLite**, a stripped down lightweight version of [coroner](https://github.com/AdamUWA/coroner)... _without_ the bells and whistles. To set things up you need to get the local model server up and running and pull some models to your machine. Let's do that now.


### Ollama

First you'll need to install the Ollama model server so that we can locally interact with the generative LLMs. You can download and install Ollama from [here](https://ollama.com/).

We'll be using at least three different generative LLM models in addition to the embedding model for the vector database so you'll need to pull these models from the ollama catalog to your local machine. Once you have ollama installed and running you can start by installing the embedding model.

**NB** Once installed you can type `ollama` at the terminal to see some help info.


### Embedding Model

The embedding model we are using is [mxbai-embed-large](https://ollama.com/library/mxbai-embed-large). To install it you can use the following command:

`ollama pull mxbai-embed-large`

Once it's installed use the `ollama list` command. You should see some details about the model in the terminal.


### LLM Llama 3.2

All the LLM models we'll be using can be found [here](https://github.com/ollama/ollama/blob/main/README.md#model-library). Take note of the size of the models and the RAM requirements. The first one you'll need to install is [llama3.2](https://ollama.com/library/llama3.2) (2.0 GB) which can be installed with the following command:

`ollama pull llama3.2`


### LLM gemma3

Next install [gemma3](https://ollama.com/library/gemma3) (3.3 GB) with this command:

`ollama pull gemma3`


### LLM phi4-mini

Now install [phi4-mini](https://ollama.com/library/phi4-mini) (2.5 GB) with this command:

`ollama pull phi4-mini`


### Conda Environment

If you have the Ollama model server correctly setup and have installed all the models you can next create the Python environment with conda. If you don't already have conda installed you can follow the instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

Once conda is up and running you'll need to create the environment. To do so, open up a terminal, go into the top level directory of this repo,  and type the following command:

`conda env create -f environment.yml`

Now your ready to go. Just type `conda activate coronerLite` to activate the conda environment.


## Programmatic Interaction

To use the RAG system from within an ordinary Python script take a look at the demo modules (`demo.py`, `demo.ipynb`) where you'll find examples of how to use the `qanda.py` module for programmatic interaction.


## Preprocessing your Documents

If you have a new PDF document you'd like to work with you'll need to preprocess it. To invoke the preprocessor on your document simply add the document to the `data/` directory and then run `python preprocessor.py`. The resulting processed JSONL file will appear in the `jsondata/` directory.


## Data

The coroner's reports (and other such documents) used for the project were supplied by Dr. Matt Albrecht from the [Western Australian Centre for Road Safety Research (WACRSR)](https://www.uwa.edu.au/projects/centre-for-road-safety-research/wacrsr-site-link).


