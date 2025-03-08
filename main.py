import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Options for length and language (added Spanish and German)
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "Spanish", "German"]

# Initialize FewShotPosts
fs = FewShotPosts()
tags = fs.get_tags()

# Main app layout
def main():
    st.subheader("LinkedIn Post Generator:")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_tag = st.selectbox("Topic", options=tags, key="tag")

    with col2:
        selected_length = st.selectbox("Length", options=length_options, key="length")

    with col3:
        selected_language = st.selectbox("Language", options=language_options, key="language")

    # Generate Button
    if st.button("Generate"):
        try:
            post = generate_post(selected_length, selected_language, selected_tag)
            st.write(post)
        except Exception as e:
            st.error(f"Error generating post: {e}")

# Run the app
if __name__ == "__main__":
    main()
