# Animal Image Classifier

**Animal Image Classifier** is an interactive web application that leverages deep learning to identify animals in user-uploaded images. Built with Streamlit and powered by a state-of-the-art MobileNetV2 model pretrained on ImageNet, the app provides instant predictions, highlighting the most likely animal species along with a confidence score. Users simply upload a photo, and the app displays the top animal match, alternative likely animals, and a visual confidence indicator.

Special features include a clean, intuitive interface, support for a wide range of animal classes, and real-time feedback on prediction confidence. The app also offers user guidance if the model is uncertain or if no animal is detected, making it accessible and informative for both casual users and those interested in AI-powered image recognition.

## Features
- Upload or drag-and-drop images
- Identifies objects in images using a powerful AI model
- Clean, intuitive interface
- Live, public deployment

## How to Run Locally
1. Install requirements: `pip install -r requirements.txt`
2. Run the app: `streamlit run CP_Animal_Image_Classifier.py`
   - This will automatically open your browser to [http://localhost:8501](http://localhost:8501).
   - If your browser does not open, manually visit [http://localhost:8501](http://localhost:8501) after running the command.

## Deployment
Ready for deployment to Streamlit Cloud, Windsurf, or similar platforms.
