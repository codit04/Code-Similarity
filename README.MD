# Code Similarity Score Generator

Takes in 2 python files and generates a similarity score based on the similarity of their Abstract Syntax Trees (ASTs).

The visualized AST can be seen on astree.png as well as on the streamlit app.

Preorder and Inorder traversals of the ASTs are generated and indel distance,hamming distance, levenstein distance are calculated between the traversals to generate the similarity score.

Tried using the graph edit distance algorithm but it was too slow for large files, since it is found to be NP Hard.
## Usage


    git clone www.github.com/codit04/Code-Similarity
    cd Code-Similarity
    pip install -r requirements.txt
    streamlit run app.py



