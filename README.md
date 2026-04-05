# 🌿 PlantGuard AI — Plant Disease Detection

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Accuracy](https://img.shields.io/badge/Accuracy-96%25-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end **plant disease detection system** powered by a custom CNN. Upload or capture a leaf photo and get an instant disease diagnosis with treatment recommendations.

---

## 🚀 Features

- 📷 **Dual Input** — File upload and live webcam capture
- 🧠 **Custom CNN** — 4 Conv blocks, 458K parameters, ~96% accuracy
- 🔥 **Grad-CAM** — Visual heatmap showing what the model looks at
- 💊 **Treatment Advice** — Disease-specific recommendations
- 📊 **Top-3 Predictions** — Confidence scores for top results
- 🌐 **REST API** — Flask backend with clean JSON responses
- 🎨 **3-Page UI** — Detect, Architecture, and About pages

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Deep Learning | TensorFlow 2.x / Keras |
| Backend API | Flask |
| Frontend UI | Streamlit |
| Image Processing | OpenCV |
| Explainability | Grad-CAM |
| Dataset | PlantVillage (20,063 images) |

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| Training Accuracy | 96.32% |
| Validation Accuracy | 97.27% |
| Test Accuracy | 96.18% |
| Total Parameters | 458,063 |
| Input Size | 128 × 128 × 3 |
| Output Classes | 15 |

---

## 🏗️ Model Architecture
```
Input (128×128×3)
→ Rescaling (÷255, built-in)
→ Conv2D(32) + MaxPool  →  64×64
→ Conv2D(64) + MaxPool  →  32×32
→ Conv2D(128) + MaxPool →  16×16
→ Conv2D(256) + MaxPool →   8×8
→ GlobalAveragePooling2D
→ Dense(256) + Dropout(0.3)
→ Dense(15) + Softmax
```

---

## 📁 Project Structure
```
PlantGuard-AI/
├── model/
│   └── plant_disease_detection_model.h5
├── flask_app/
│   └── app.py                 ← REST API
├── streamlit_app/
│   └── app.py                 ← UI
├── notebook/
│   └── train_model.ipynb      ← Training notebook
└── requirements.txt
```

---

## ⚡ Quick Start

### 1. Install dependencies
```bash
pip install flask streamlit tensorflow numpy opencv-python matplotlib Pillow requests
```

### 2. Start Flask backend
```bash
cd flask_app
python app.py
# Running on http://127.0.0.1:5000
```

### 3. Start Streamlit frontend
```bash
cd streamlit_app
streamlit run app.py
# Open http://localhost:8501
```

> Both terminals must run simultaneously.

---

## 🌿 Supported Disease Classes (15)

| Plant | Classes |
|---|---|
| Bell Pepper | Bacterial Spot, Healthy |
| Potato | Early Blight, Late Blight, Healthy |
| Tomato | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy |

---

## 🔌 API Reference

### `GET /`
Health check
```json
{ "status": "Plant Disease Detection API is running!" }
```

### `POST /predict`
Send a leaf image, get prediction back.

**Request:** `multipart/form-data` with key `file`

**Response:**
```json
{
  "predicted_class": "Tomato_Early_blight",
  "confidence": 94.37,
  "recommendation": "Use fungicide spray and maintain proper spacing.",
  "top3": [
    { "class": "Tomato_Early_blight", "confidence": 94.37 },
    { "class": "Tomato_Late_blight",  "confidence": 3.21  },
    { "class": "Tomato__Target_Spot", "confidence": 1.18  }
  ]
}
```

---

## 📝 Dataset

- **Name:** PlantVillage Dataset
- **Images:** 20,063
- **Classes:** 15
- **Split:** 70% train / 15% val / 15% test
- **Source:** Open source research dataset

---

## 🔮 Future Work

- [ ] Deploy to cloud (Render / AWS / Google Cloud Run)
- [ ] Add more plant species and disease classes
- [ ] Experiment with EfficientNetV2 / MobileNetV3 transfer learning
- [ ] Build a native mobile app (Android/iOS)
- [ ] Multi-language UI support

---

## 📄 License

MIT License — feel free to use and modify.

---

*Built with TensorFlow · Flask · Streamlit*
