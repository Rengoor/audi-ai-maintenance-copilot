import streamlit as st
from vision import get_multimodal_answer
import os

st.set_page_config(page_title="Audi Tech Assistant")

st.title("Audi AI Maintenance Assistant")
st.markdown("Upload a photo of a part or ask a technical question from the manual.")

with st.sidebar:
    st.header("System Status")
    st.info("Connected to: Llama 3.2 Vision & Mistral")

# UI Layout
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Upload a part photo", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        # temp file for Ollama in ram
        with open("temp_part.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

with col2:
    user_query = st.text_input(
        "What do you need to know?",
        placeholder="e.g. What is the torque for these bolts?",
    )

    if st.button("Analyze & Consult Manual"):
        if not user_query and not uploaded_file:
            st.warning("Please provide an image or a question.")
        else:
            with st.spinner("Analyzing..."):
                img_path = "temp_part.jpg" if uploaded_file else None
                result = get_multimodal_answer(
                    user_text=user_query, image_path=img_path
                )

                if result["identified_part"]:
                    st.success(f"Identified Part: **{result['identified_part']}**")

                st.markdown("### 🤖 Technical Guidance")
                st.write(result["answer"])

                with st.expander("View Manual Sources"):
                    for doc in result["sources"]:
                        st.write(
                            f"**Page {doc.metadata.get('page', 'N/A')}:** {doc.page_content[:200]}..."
                        )
