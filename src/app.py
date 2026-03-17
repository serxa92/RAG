import streamlit as st

from query import ask_rag


# Configure the Streamlit page
st.set_page_config(page_title="Local RAG", layout="wide")

# Main title and short description
st.title("Local RAG Question-Answering System")
st.write("Ask a question about the indexed PDF knowledge base.")


# Text input where the user writes a question
question = st.text_input("Enter your question")

# Optional checkbox to show retrieved chunks used as context
show_sources = st.checkbox("Show retrieved chunks", value=True)


# Run the query only when the button is pressed
if st.button("Ask"):
    # Prevent empty questions
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        # Show a loading spinner while the system retrieves context
        # and generates the final answer
        with st.spinner("Generating answer..."):
            result = ask_rag(question, top_k=5)

        # Display final answer
        st.subheader("Answer")
        st.write(result["answer"])

        # Optionally show the retrieved chunks used as context
        if show_sources:
            st.subheader("Retrieved Chunks")

            for i, (doc, metadata, distance) in enumerate(
                zip(result["documents"], result["metadatas"], result["distances"]),
                start=1
            ):
                # Each chunk is displayed inside an expandable panel
                # to keep the interface cleaner
                with st.expander(
                    f"Result {i} | Source: {metadata.get('source')} | "
                    f"Chunk: {metadata.get('chunk_index')} | Distance: {distance:.4f}"
                ):
                    st.write(doc)