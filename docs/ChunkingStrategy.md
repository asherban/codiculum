# Chunking Strategy

The purpose of chunking is to provide the RAG with enough context to answer the question, but not so much that it is overwhelming.
The embedding model we are using has a size of 8100 tokens, so we cannot exceed that.

## General

Each chunk should be a text format with the following information:
1. The filename, start line and end line of the code snippet.
2. The imports that need to be added to the top of the file to use the code snippet.
3. The brief description of the code snippet if available.
4. The detailed description of the code snippet if available.
5. The code snippet itself.
6. If there are examples of usage of the code snippet, they should be added to the chunk.

## Objects to keep in the same chunk

- Functions
- Classes
- Macros
- Enums
- Structs
- Unions

## Handling Code Snippets that are Larger than the token limit

- If a chunk is larger than the token limit, we need to split it into multiple chunks.
- When the object to split is a class or a class like object (struct, union, enum), split it to functions, but include in each chunk the imports, overall class description and at least the class constructor.
- Any other objects should be split by a logical space into multiple chunks if they exceed the token limit. Always keep the general chunk structure defined above, and indicate in a comment that
the chunk is partial. If the example contains usage of the API in the chunk, add it as well if possible based on the token limit. Otherwise it can be dropped.
