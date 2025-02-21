import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)

with col1:
    image = Image.open("images/photo.jpg")
    orig_width, orig_height = image.size
    scale_factor = 0.25
    new_width = int(orig_width * scale_factor)
    new_height = int(orig_height * scale_factor)
    resized_image = image.resize((new_width, new_height))
    # Convert image to bytes
    from io import BytesIO
    import base64

    buffered = BytesIO()
    resized_image.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    # Display centered image using HTML
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{img_b64}" width="{new_width}" height="{new_height}">
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.title("Ruben du Pon")
    content = """
    Hi, this is some text about me. I am a data scientist and I love to code.
    """
    st.info(content)

content2 = """
Below you can find some of the projects I have made.
Feel free to contact me!
"""
st.write("")
st.write(content2)

df = pd.read_csv("data.csv", sep=";")

col3, empty_col, col4 = st.columns([1.5, .25, 1.5])

with col3:
    for index, row in df[0::2].iterrows():
        st.header(row["title"])
        st.write(row["description"])
        st.image("images/" + row["image"])
        st.write(f"[Source Code]({row['url']})")

with col4:
    for index, row in df[1::2].iterrows():
        st.header(row["title"])
        st.write(row["description"])
        st.image("images/" + row["image"])
        st.write(f"[Source Code]({row['url']})")
