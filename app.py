import streamlit as st
from codeSimilarity import calculate_similarity
from Visualize import visualize
import tempfile

st.title("Code Similarity Checker")
st.write("This app checks the similarity between two Python code snippets.")

# upload 2 python files to compare
file1 = st.file_uploader("Upload the first Python file", type=["py"])
file2 = st.file_uploader("Upload the second Python file", type=["py"])

if file1 and file2:
    code1 = tempfile.NamedTemporaryFile(delete=False)
    code1.write(file1.read())
    code1.seek(0)

    code2 = tempfile.NamedTemporaryFile(delete=False)
    code2.write(file2.read())
    code2.seek(0)

    code1 = code1.read().decode()
    code2 = code2.read().decode()

    similarity_score = calculate_similarity(code1, code2)

    st.write(f"The indel similarity score is {similarity_score[0]}")
    st.write(f"The hamming similarity score is {similarity_score[1]}")
    st.write(f"The levenshtein similarity score is {similarity_score[2]}")

    st.write("Visualizing the AST of the first code snippet")
    visualize(code1)
    st.image("astree.png")

    st.write("Visualizing the AST of the second code snippet")
    visualize(code2)
    st.image("astree.png")

    st.write("The ASTs of the two code snippets are visualized above.")
