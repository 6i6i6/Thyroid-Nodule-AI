import streamlit as st
from PIL import Image
import os
import sys

# ضمان إدراج المسار الحالي ليتعرف السيرفر على الملفات المجاورة
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from detector import ThyroidDetector
except Exception as e:
    ThyroidDetector = None
    import_error_msg = str(e)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Thyroid Nodule Analysis System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background:#30204a;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

h1, h2, h3, h4, h5, h6 {
    color: #2ecc71 !important;
}

p, label{
    color:white;
}

[data-testid="stHeader"]{
    background:transparent;
}

.main-card{
    background:#3a2758;
    padding:25px;
    border-radius:18px;
    border:1px solid #7c3aed;
    box-shadow:0 0 18px rgba(124,58,237,.25);
}

.project-card{
    background:#3a2758;
    padding:20px;
    border-radius:18px;
    border:1px solid #7c3aed;
    margin-top:20px;
    margin-bottom:25px;
}

.stButton>button{
    width:100%;
    height:55px;
    border-radius:12px;
    background:#7c3aed;
    color:white;
    border:none;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#9a6aff;
}

hr{
    border:1px solid #7c3aed;
}

.medical-table {
    width: 100%;
    color: white;
    font-size: 16px;
    border-collapse: collapse;
    margin-top: 15px;
}
.medical-table th {
    padding: 12px;
    text-align: left;
    background-color: #4c3575;
    border-bottom: 2px solid #7c3aed;
    color: #2ecc71;
}
.medical-table td {
    padding: 12px;
    border-bottom: 1px solid #5a3b8c;
}

[data-testid="stSidebar"] {
    background-color: #24183b !important;
    border-right: 1px solid #7c3aed;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar - Browse Dataset Test Samples
# -----------------------------
DATASET_DIR = "JPEGImages"  
image_extensions = (".png", ".jpg", ".jpeg")
image_files = []

if os.path.exists(DATASET_DIR):
    image_files = [f for f in os.listdir(DATASET_DIR) if f.lower().endswith(image_extensions)]
    image_files.sort()

selected_image_path = None

with st.sidebar:
    st.markdown("<h2 style='color:#2ecc71; text-align:center;'>📁 Dataset Samples</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#aaa;'>Found <b>{len(image_files)}</b> test cases available.</p>", unsafe_allow_html=True)
    st.write("---")

    if len(image_files) > 0:
        st.markdown("<b>🔍 Select Case for Testing</b>", unsafe_allow_html=True)
        selected_filename = st.selectbox(
            "Choose an ultrasound image:",
            options=image_files,
            index=0
        )
        selected_image_path = os.path.join(DATASET_DIR, selected_filename)
        
        st.write("")
        st.markdown("<b>🖼️ Quick Preview:</b>", unsafe_allow_html=True)
        preview_img = Image.open(selected_image_path)
        st.image(preview_img, use_container_width=True)
    else:
        st.warning(f"No images found or '{DATASET_DIR}' folder is missing.")

# -----------------------------
# Header
# -----------------------------
logo_path = "assets/zoro.png"
logo = None
if os.path.exists(logo_path):
    logo = Image.open(logo_path)

c1, c2 = st.columns([1,6])

with c1:
    if logo:
        st.image(logo, width=120)

with c2:
    st.markdown(
        "<h1 style='color:#2ecc71; margin:0;'>🩺 Thyroid Nodule Analysis System</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h4 style='color:#2ecc71; margin-top:5px;'>AI-powered Ultrasound Image Analysis</h4>",
        unsafe_allow_html=True
    )

# -----------------------------
# Project Information
# -----------------------------
st.markdown("""
<div class="project-card">
<h3 style="color:#2ecc71;">📋 Project Information</h3>
<table style="width:100%;color:white;font-size:17px">
<tr><td><b>Student</b></td><td>Shams Ghassan Allawi</td></tr>
<tr><td><b>Student ID</b></td><td>1230149</td></tr>
<tr><td><b>Supervisor</b></td><td>Dr. Abbas Al-Zubaidi</td></tr>
<tr><td><b>Course</b></td><td>AI in Healthcare</td></tr>
</table>
</div>
""", unsafe_allow_html=True)

st.divider()

# -----------------------------
# Image Source Selection
# -----------------------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.header("📤 Input Image Selection")
source_option = st.radio(
    "Choose input source:",
    options=["Use Selected Sample from Sidebar", "Upload a New Image File"]
)

uploaded_file = None
final_image = None

if source_option == "Upload a New Image File":
    uploaded_file = st.file_uploader(
        "Choose Image",
        type=["jpg","jpeg","png"]
    )
    if uploaded_file:
        final_image = Image.open(uploaded_file)
else:
    if selected_image_path:
        final_image = Image.open(selected_image_path)
        st.success(f"Loaded: {os.path.basename(selected_image_path)}")

analyze = st.button("🔍 Analyze Image")

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# Results
# -----------------------------
if final_image:
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("Original Image")
        st.image(final_image, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("Analysis Result")

        if analyze:
            if ThyroidDetector is None:
                st.error(f"Detector module layout error. Details: {import_error_msg}")
            else:
                try:
                    detector = ThyroidDetector()
                    result_image, detections = detector.detect(final_image)

                    st.image(result_image, use_container_width=True)

                    if len(detections):
                        det = detections[0]
                        confidence = det["confidence"]

                        st.success("Nodule Detected")
                        st.metric("Detection Confidence", f"{confidence}%")
                        
                        st.write("---")
                        st.subheader("📋 Structured Observations")
                        
                        comp = det.get("composition", "N/A")
                        margin = det.get("margins", "N/A")
                        echo = det.get("echogenicity", "N/A")
                        
                        comp_conf = det.get("comp_confidence", "N/A")
                        margin_conf = det.get("margin_confidence", "N/A")
                        echo_conf = det.get("echo_confidence", "N/A")

                        st.markdown(f"""
                        <table class="medical-table">
                            <tr>
                                <th>Characteristic</th>
                                <th>Observation</th>
                                <th>Confidence</th>
                            </tr>
                            <tr>
                                <td><b>Composition</b></td>
                                <td style="color:#2ecc71;">{comp}</td>
                                <td>{comp_conf}</td>
                            </tr>
                            <tr>
                                <td><b>Margins</b></td>
                                <td style="color:#2ecc71;">{margin}</td>
                                <td>{margin_conf}</td>
                            </tr>
                            <tr>
                                <td><b>Echogenicity</b></td>
                                <td style="color:#2ecc71;">{echo}</td>
                                <td>{echo_conf}</td>
                            </tr>
                        </table>
                        <br>
                        <p style="font-size:12.5px; color:#b3a2cd; font-style: italic; margin-top:10px;">
                            * Disclaimer: This application provides objective, structured visual observations to assist clinical workflows and does not provide an autonomous clinical diagnosis.
                        </p>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("No nodule detected in this sample.")
                except Exception as e:
                    st.error(str(e))
        else:
            st.info("Press Analyze Image to start.")

        st.markdown("</div>", unsafe_allow_html=True)
