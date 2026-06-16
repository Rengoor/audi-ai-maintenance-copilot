import streamlit as st
from vision import get_multimodal_answer
import os
from config import TEXT_MODEL_NAME, VISION_MODEL_NAME

st.set_page_config(page_title="Audi Tech Assistant")

st.title("Audi AI Maintenance Assistant")
st.markdown("Upload a photo of a part or ask a technical question from the manual.")

with st.sidebar:
    st.header("System Status")
    st.info(f"Connected to: {VISION_MODEL_NAME} & {TEXT_MODEL_NAME}")

# UI Layout
col1, col2 = st.columns([1, 1])

TEMP_IMG_PATH = "temp_image.jpg"

if "initialized" not in st.session_state:
    if os.path.exists(TEMP_IMG_PATH):
        os.remove(TEMP_IMG_PATH)
    st.session_state["initialized"] = True

with col1:
    uploaded_file = st.file_uploader("Upload a part photo", type=["jpg", "png", "jpeg"])

    # 2. Manual Removal Cleanup: Wipes data if user clicks the "X" button
    if not uploaded_file and os.path.exists(TEMP_IMG_PATH):
        os.remove(TEMP_IMG_PATH)

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        # 3. Sequential Upload Cleanup: Overwrites previous data instantly
        with open(TEMP_IMG_PATH, "wb") as f:
            f.write(uploaded_file.getbuffer())

with col2:
    user_query = st.text_input(
        "What do you need to know?",
        placeholder="e.g. What is the torque for these bolts?",
    )

    if st.button("Analyze & Consult Manual"):
        has_image = os.path.exists(TEMP_IMG_PATH)

        if not user_query and not has_image:
            st.warning("Please provide an image or a question.")
        else:
            with st.spinner("Analyzing..."):
                img_path = TEMP_IMG_PATH if has_image else None
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
