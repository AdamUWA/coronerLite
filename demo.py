
import os
import pandas as pd
from pathlib import Path

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore

from qanda import QandA
from bert_score import score


# ------------------------------------------------------------------------------ 
# Initialize a QandA object
# ------------------------------------------------------------------------------ 

# Set the file (document); generative LLM model; embedding model;
# vec db; num sources
FILE_PATH = Path("jsondata/Rodier-Finding.jsonl")
GEN_MODEL = "gemma3"
EMBED_MODEL = "mxbai-embed-large"
VDB = InMemoryVectorStore
TOP_K = 3

# Set the prompt
PROMPT = ChatPromptTemplate.from_template(
    """Context information is below.
    \n---------------------\n
    {context}
    \n---------------------\n
    Given the context information and not prior knowledge, answer the query.\n
    Query: {input}\n
    Answer:\n""",
)

# Initialize the qanda object
qanda = QandA(gen_model=GEN_MODEL,
              embed_model=EMBED_MODEL, 
              vdb=VDB,
              file_path=FILE_PATH,
              top_k=TOP_K,
              prompt=PROMPT)


# Qanda help
help(qanda)


# ------------------------------------------------------------------------------ 
# Several methods to use a qanda object
# ------------------------------------------------------------------------------ 

# ------------------------------------------------------------------------------ 
# Method 1: Just answer the questions
# ------------------------------------------------------------------------------ 

# Ask some questions
qanda.ask("Who died?")

qanda.ask("Acitvity involved in death?")

qanda.ask("Who went fishing?")


# Create a list of questions
QUESTIONS = ["Who is the coroner?",
             "Who is the deceased?",
             "What was the cause of death?"]

# Get the answers
for i, QUESTION in enumerate(QUESTIONS):
    ANSWER = qanda.ask(QUESTION)
    print(f"Answer {i + 1}: ", ANSWER)


# ------------------------------------------------------------------------------ 
# Method 2: Answer the questions and score the answers
# ------------------------------------------------------------------------------ 

# make a scores function
def calculate_bertscore_df(df):
    references = df['CORRECT_ANSWER'].tolist()
    candidates = df['LLM_ANSWER'].tolist()
    
    precision, recall, f1 = score(candidates, references, lang="en", verbose=True)
    
    df['BERT_PRECISION'] = precision.tolist()
    df['BERT_RECALL'] = recall.tolist()
    df['BERT_F1'] = f1.tolist()
    
    return df


QUESTIONS = ["Who is the coroner?",
             "Who is the deceased?",
             "What was the cause of death?"]
CORRECT_ANSWERS = ["Sarah Helen Linton",
                   "Frank Edward Rodier",
                   "unascertained"]
LLM_ANSWERS = []

for i, QUESTION in enumerate(QUESTIONS):
    ANSWER = qanda.ask(QUESTION)
    LLM_ANSWERS.append(ANSWER)
    print(f"Answer {i + 1}: ", ANSWER)

data = {
    'FILENAME': ['Rodier-Finding'] * len(QUESTIONS),
    'MODEL': ['gemma3'] * len(QUESTIONS),
    'QUESTION': QUESTIONS,
    'CORRECT_ANSWER': CORRECT_ANSWERS,
    'LLM_ANSWER': LLM_ANSWERS
}

df = pd.DataFrame(data)

scores_df = calculate_bertscore_df(df)

print(scores_df.columns)

print(scores_df)


# ------------------------------------------------------------------------------ 
# Method 3: Answer the question and provide the source context
# ------------------------------------------------------------------------------ 

QUESTION = "What activity was implicated in the cause of death?"
ANSWER, SOURCES = qanda.ask(QUESTION, verbose=True)

print(ANSWER)

print(SOURCES)

print(SOURCES[0]['text'])

print(SOURCES[0]['page'])

print(SOURCES[0]['document'])


# ------------------------------------------------------------------------------ 
# Method 4: Compare answers of different models
# ------------------------------------------------------------------------------ 

LLAMA = "llama3.2"
GEMMA = "gemma3"
PHI   = "phi4-mini"

qanda_llama = QandA(gen_model=LLAMA,
                    embed_model=EMBED_MODEL, 
                    vdb=VDB,
                    file_path=FILE_PATH,
                    top_k=TOP_K,
                    prompt=PROMPT)

qanda_gemma = QandA(gen_model=GEMMA,
                    embed_model=EMBED_MODEL, 
                    vdb=VDB,
                    file_path=FILE_PATH,
                    top_k=TOP_K,
                    prompt=PROMPT)

qanda_phi = QandA(gen_model=PHI,
                  embed_model=EMBED_MODEL, 
                  vdb=VDB,
                  file_path=FILE_PATH,
                  top_k=TOP_K,
                  prompt=PROMPT)


QUESTION = "What activity was implicated in the cause of death?"
CORRECT_ANSWER = "Fishing"
LLM_ANSWERS = []

for i, qanda_model in enumerate([qanda_llama, qanda_gemma, qanda_phi]):
    ANSWER = qanda_model.ask(QUESTION)
    LLM_ANSWERS.append(ANSWER)
    print(f"Answer {i + 1}: ", ANSWER)
    
data = {
    'FILENAME': ['Rodier-Finding'] * 3,
    'MODEL': [LLAMA, GEMMA, PHI],
    'QUESTION': [QUESTION] * 3,
    'CORRECT_ANSWER': [CORRECT_ANSWER] * 3,
    'LLM_ANSWER': LLM_ANSWERS
}

df = pd.DataFrame(data)

scores_df = calculate_bertscore_df(df)

print(scores_df.columns)

print(scores_df)

