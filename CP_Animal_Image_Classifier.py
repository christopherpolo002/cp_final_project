import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf

st.title("🐾 Animal Image Classifier 🦁🐶🐱")
st.write("""
Upload an image of an animal, and our AI will tell you which animal it is!
""")

@st.cache_resource
def load_model():
    # Placeholder: load your trained model here
    # For demonstration, use a MobileNetV2 pretrained on ImageNet
    model = tf.keras.applications.MobileNetV2(weights="imagenet")
    return model

model = load_model()

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image', use_container_width=True)
    st.write("")
    st.write("Classifying...")

    # Preprocess image for MobileNetV2
    img = image.resize((224, 224))
    x = np.array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

    # List of keywords to identify animal classes in ImageNet labels
    animal_keywords = [
        'dog', 'cat', 'bird', 'fish', 'horse', 'lion', 'tiger', 'leopard', 'cheetah', 'wolf', 'fox', 'bear',
        'monkey', 'ape', 'gorilla', 'chimpanzee', 'baboon', 'rabbit', 'hare', 'deer', 'cow', 'bull', 'sheep',
        'goat', 'pig', 'boar', 'mouse', 'rat', 'squirrel', 'bat', 'otter', 'ferret', 'weasel', 'mole', 'hedgehog',
        'elephant', 'zebra', 'giraffe', 'kangaroo', 'koala', 'panda', 'crocodile', 'alligator', 'snake', 'lizard',
        'turtle', 'frog', 'toad', 'dolphin', 'whale', 'shark', 'penguin', 'parrot', 'owl', 'eagle', 'hawk', 'falcon',
        'duck', 'goose', 'swan', 'chicken', 'rooster', 'hen', 'turkey', 'peacock', 'crab', 'lobster', 'shrimp',
        'spider', 'insect', 'bee', 'ant', 'butterfly', 'moth', 'beetle', 'fly', 'mosquito', 'worm', 'slug', 'snail'
    ]

    preds = model.predict(x)
    results = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=10)[0]

    # Filter predictions for animal classes
    animal_results = [(id, label, prob) for (id, label, prob) in results if any(kw in label.lower() for kw in animal_keywords)]

    if animal_results:
        # Highlight the top-1 animal prediction
        top_label = animal_results[0][1].replace('_', ' ').title()
        top_conf = animal_results[0][2]
        st.markdown(f"## 🏆 Animal: <span style='color:#0072C6'>{top_label}</span>", unsafe_allow_html=True)
        st.progress(float(top_conf))
        st.write(f"**Confidence:** {top_conf*100:.2f}%")
        # Warn if confidence is low
        if top_conf < 0.6:
            st.warning("⚠️ The model is not very confident in this prediction. Try a clearer image.")
        # Show top-3 animal predictions
        st.subheader("Other likely animals:")
        for i, (imagenet_id, label, prob) in enumerate(animal_results[:3]):
            st.write(f"{i+1}. **{label.replace('_', ' ').title()}** ({prob*100:.2f}% confidence)")
        st.success("Done!")
    else:
        st.error("No animal detected in this image. Please try another image with a clear animal.")
else:
    st.info("Please upload an image to classify.")
