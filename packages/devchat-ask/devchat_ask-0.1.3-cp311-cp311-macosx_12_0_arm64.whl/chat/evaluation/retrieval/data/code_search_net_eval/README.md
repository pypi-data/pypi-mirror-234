# CodeSearchNet_eval.json

This dataset contains human evaluation of code snippet retrieval.
This is the dataset used to evaluate the performance of the CodeSearchNet Challenge winners with a few modifications.
First, we removed the snippets that were not accessible from GitHub anymore. Snippets that were too long (mostly minified JS) were removed.
Then we merged the multiples evaluations of the same query/snippet pair into a single average score.
You can find the original dataset [here](https://raw.githubusercontent.com/github/CodeSearchNet/bb121a/resources/annotationStore.csv).

This dataset contains 2822 query/snippet/score triple over 99 different queries.
Each entry is scored on a scale from 0 (irrelevant) to 3 (perfectly relevant).

## Results

The precision, recall and F1 score figures given here are lower bounds because non-annotated query/snippet pairs are considered as irrelevant (relevance score 0) but might in fact be relevant.
They are calculated from the top 5 retrieved documents.
The times are measured on a M1 Max MacBook Pro.


## Model: "hkunlp/instructor-base"

Here are the results for different instructions.
Strangely, the default generic instructions perform slightly better than the task-specific ones.
With the default instructions, base, large and xl models have same precision, recall and F1 scores.
Only the indexing and retrieval time per query are different, so the base model is the best choice for this dataset.

### Default instructions:

Instructions:
- query: "Represent the question for retrieving supporting documents: "
- document: "Represent the document for retrieval: "

Results:
- Precision: 0.57
- Recall: 0.68
- F1: 0.62
- Indexing time per doc (ms): 100
- Retrieval time per query (ms): 102


### Custom instructions 1:

Instructions:
- query: "Represent the code search query for retrieving supporting pieces of code: "
- document: "Represent the piece of code for code retrieval: "

Results:
- Precision: 0.55
- Recall: 0.65
- F1: 0.59
- Indexing time per doc (ms): 94
- Retrieval time per query (ms): 63


### Custom instructions 2:

Instructions:
- query: "Represent the query for retrieving supporting source code: "
- document: "Represent the source code for retrieval: "

Results:
- Precision: 0.56
- Recall: 0.67
- F1: 0.61
- Indexing time per doc (ms): 94
- Retrieval time per query (ms): 73


## Model: "hkunlp/instructor-large"

### Default instructions:

Instructions:
- query: "Represent the question for retrieving supporting documents: "
- document: "Represent the document for retrieval: "

Results:
- Precision: 0.57
- Recall: 0.68
- F1: 0.62
- Indexing time per doc (ms): 285
- Retrieval time per query (ms): 150


## Model: "hkunlp/instructor-xl"

Options:
- embed_instruction="Represent this piece of code for retrieval: ",
- query_instruction="Represent the coding question for retrieving supporting pieces of code: "

Results:
- Precision: 0.57
- Recall: 0.68
- F1: 0.62
- Indexing time per doc (ms): 940
- Retrieval time per query (ms): 402


## Model: "sentence-transformers/all-mpnet-base-v2"

Results:
- Precision: 0.58
- Recall: 0.69
- F1: 0.63
- Indexing time per doc (ms): 103
- Retrieval time per query (ms): 150


## Model: "text-embedding-ada-002"
- Precision: 0.48
- Recall: 0.57
- F1: 0.52
- Indexing time per doc (ms): 137
- Retrieval time per query (ms): 281


## Model: "intfloat/e5-large-v2"

Results:
- Precision: 0.57
- Recall: 0.67
- F1: 0.62
- Indexing time per doc (ms): 337
- Retrieval time per query (ms): 288

# Summary

| Model                                   | Precision | Recall | F1 score | Indexing time per doc (ms) | Retrieval time per query (ms) |
| --------------------------------------- | --------- | ------ | -------- | -------------------------- | ----------------------------- |
| sentence-transformers/all-mpnet-base-v2 |      0.58 |   0.69 |     0.63 |                        103 |                           150 |
| hkunlp/instructor-base                  |      0.57 |   0.68 |     0.62 |                        100 |                           102 |
| hkunlp/instructor-large                 |      0.57 |   0.68 |     0.62 |                        285 |                           150 |
| hkunlp/instructor-xl                    |      0.57 |   0.68 |     0.62 |                        940 |                           402 |
| intfloat/e5-large-v2                    |      0.57 |   0.67 |     0.62 |                        337 |                           288 |
| text-embedding-ada-002                  |      0.48 |   0.57 |     0.52 |                        137 |                           281 |


The first thing to notice is that, apart from the text-embedding-ada-002 model, which performs significantly worse than the others, all models have similar precision, recall and F1 scores.
The sentence-transformers/all-mpnet-base-v2 model has the best precision, recall and F1 scores, but the hkunlp/instructor-base model is slightly faster to retrieve.
