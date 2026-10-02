# Natural Language Processing (AI-310)

Natural Language Processing (NLP) enables computers to understand, interpret, and generate human language.

## Common tasks
Text classification, sentiment analysis, named entity recognition (NER), machine translation, summarization, and question answering.

## Typical pipeline
Tokenization, converting tokens to numerical representations (embeddings), then modelling with a Transformer. Important models include Word2Vec, BERT, and GPT.

## Embeddings and LLMs
Embeddings map text to vectors so that texts with similar meaning are close together. Large Language Models (LLMs) are very large Transformers trained to predict text. A known weakness of LLMs is hallucination, where they produce fluent but false statements. Retrieval-Augmented Generation (RAG) reduces this by supplying retrieved documents to the model as context.

## Tools
Hugging Face Transformers, Sentence-Transformers, spaCy, and NLTK.

## Course details at NIT
AI-310 Natural Language Processing is worth 3 credit hours and is taken in Semester 6. The prerequisite is AI-301. The course project is to build a retrieval-augmented question answering system using embeddings and a vector index.
