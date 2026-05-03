import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2

app = Flask(__name__)

MODEL_PATH = os.path.join("E:\\", "Plant Disease Detection", "model", "plant_disease_detection_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

dummy = np.zeros((1, 128, 128, 3), dtype=np.float32)
model.predict(dummy, verbose=0)
print(" Model loaded and warmed up!")

DATASET_PATH = os.path.join("E:\\", "Plant Disease Detection", "dataset", "Plant_Village", "PlantVillage")
class_names = sorted(os.listdir(DATASET_PATH))

disease_info = {
    "Pepper__bell___Bacterial_spot": {
        "severity": "Moderate",
        "en": {
            "description": "Bacterial spot is caused by Xanthomonas bacteria. It appears as small, dark, water-soaked spots on leaves and fruits that later turn brown and necrotic.",
            "treatment": "Apply copper-based bactericide (copper oxychloride) every 7–10 days. Remove and destroy all infected leaves immediately. Avoid overhead irrigation as water spreads bacteria.",
            "prevention": "Use certified disease-free seeds. Maintain proper plant spacing for good air circulation. Rotate crops every season to prevent soil buildup of bacteria.",
            "warning": "Spreads rapidly in warm, humid conditions. Act immediately upon detection."
        },
        "hi": {
            "description": "Bacterial spot ek bacterial bimari hai jo Xanthomonas bacteria se hoti hai. Patton aur phalon par chote, kaale, paani se bhare daag dikhte hain jo baad mein bhoore aur sukhe ho jaate hain.",
            "treatment": "Copper-based dawai (copper oxychloride) 7–10 din mein lagaate rahen. Sankramit patte turant hataiye aur nashtaat karein. Upar se paani mat daalein kyunki paani se bacteria failta hai.",
            "prevention": "Certified beej ka hi istemaal karein. Podhon ke beech uchit doori rakhen taaki hawa aache se aaye. Har season mein fasl badlen taaki mitti mein bacteria na badhein.",
            "warning": "Garm aur nami wale mausam mein tezi se failta hai. Dikhte hi turant action lein."
        }
    },
    "Pepper__bell___healthy": {
        "severity": "None",
        "en": {
            "description": "Your pepper plant is perfectly healthy with no signs of disease or stress.",
            "treatment": "No treatment required. Continue your current care routine.",
            "prevention": "Water regularly at the base of the plant. Fertilize every 2–3 weeks with balanced fertilizer. Monitor regularly for early signs of pests or disease.",
            "warning": ""
        },
        "hi": {
            "description": "Aapka shimla mirch ka podha bilkul swasth hai, koi bimari ya takleef ke koi lakshan nahi hain.",
            "treatment": "Koi ilaj ki zaroorat nahi. Apni maujuda dekhbhal jaari rakhen.",
            "prevention": "Podhe ki jaad mein niyamit paani dein. Har 2–3 hafte mein balanced khad dein. Keede ya bimari ke shuruati sanket ke liye niyamit jaanch karein.",
            "warning": ""
        }
    },
    "Potato___Early_blight": {
        "severity": "Moderate",
        "en": {
            "description": "Early blight is caused by the fungus Alternaria solani. It appears as dark brown spots with concentric rings (like a target) on older leaves first, then spreads upward.",
            "treatment": "Apply Mancozeb or Chlorothalonil fungicide every 7–14 days. Remove infected lower leaves. Ensure proper drainage to avoid waterlogging around roots.",
            "prevention": "Plant certified disease-free seed potatoes. Rotate crops — do not plant potatoes in the same field for at least 2–3 years. Avoid excessive nitrogen fertilizer.",
            "warning": "If untreated, can reduce yield by 20–30%. Worse in warm days with cool nights."
        },
        "hi": {
            "description": "Early blight Alternaria solani fungus se hoti hai. Purane patton par pahle kaale-bhoore daag dikhte hain jisme concentric rings hoti hain (target jaisi). Yeh upar ki taraf failti hai.",
            "treatment": "Har 7–14 din mein Mancozeb ya Chlorothalonil fungicide lagayen. Sankramit neeche ke patte hataiye. Jadon ke aaspas paani na ruke iske liye uchit drainage sunischit karein.",
            "prevention": "Certified bimari-mukt aalu ke beej lagayen. Fasl badlen — kam se kam 2–3 saal tak usi khet mein aalu na lagayen. Zyada nitrogen khad se bachen.",
            "warning": "Ilaj na hone par paidavar 20–30% tak kam ho sakti hai. Garm din aur thandi raaton mein zyada badh ti hai."
        }
    },
    "Potato___Late_blight": {
        "severity": "Severe",
        "en": {
            "description": "Late blight, caused by Phytophthora infestans, is the most destructive potato disease. It appears as dark, water-soaked lesions on leaves with white fuzzy growth underneath. This was responsible for the Irish Potato Famine.",
            "treatment": "Apply copper-based fungicide or Metalaxyl immediately. Remove and burn all infected plants — do not compost. Stop overhead irrigation completely. In severe cases, destroy the entire crop to prevent spread.",
            "prevention": "Plant resistant varieties. Avoid planting in low-lying areas with poor drainage. Scout fields regularly, especially during cool and wet weather. Apply preventive fungicide sprays before disease onset.",
            "warning": "URGENT — Late blight can destroy an entire crop within days. Take immediate action."
        },
        "hi": {
            "description": "Late blight, Phytophthora infestans se hoti hai, yeh aalu ki sabse vinaashkari bimari hai. Patton par kaale, paani se bhare ghav dikhte hain, neeche ki taraf safed fuzzy growth hoti hai. Yahi bimari Irish Potato Famine ki wajah bani thi.",
            "treatment": "Turant copper-based fungicide ya Metalaxyl lagayen. Sankramit podhon ko nikaalein aur jalayein — khad mein mat daalein. Upar se paani dena bilkul band karein. Gambhir maamlon mein failaav rokne ke liye poori fasl nashtaat karein.",
            "prevention": "Pratirodhi kismon lagayen. Khraab drainage wali nichli jagahon par na lagayen. Kheton ki niyamit jaanch karein, khaaskar thandi aur bheegi mausam mein. Bimari shuru hone se pehle preventive fungicide sprays lagayen.",
            "warning": "ATVASHYAK — Late blight kuch hi dinon mein poori fasl barbad kar sakti hai. Turant action lein."
        }
    },
    "Potato___healthy": {
        "severity": "None",
        "en": {
            "description": "Your potato plant is healthy and growing well with no signs of disease.",
            "treatment": "No treatment required. Maintain current care.",
            "prevention": "Water consistently, avoid waterlogging. Hill soil around plants as they grow. Check regularly for Colorado potato beetle and aphids.",
            "warning": ""
        },
        "hi": {
            "description": "Aapka aalu ka podha swasth hai aur achhe se badh raha hai, bimari ke koi lakshan nahi hain.",
            "treatment": "Koi ilaj ki zaroorat nahi. Maujuda dekhbhal jaari rakhen.",
            "prevention": "Niyamit paani dein, paani bhar'ne se bachen. Badte waqt podhon ke aaspaas mitti chadhaate rahen. Colorado potato beetle aur aphids ke liye niyamit jaanch karein.",
            "warning": ""
        }
    },
    "Tomato_Bacterial_spot": {
        "severity": "Moderate",
        "en": {
            "description": "Caused by Xanthomonas bacteria, bacterial spot creates small, dark, water-soaked spots on leaves, stems, and fruits. Infected fruits have raised, scabby lesions making them unmarketable.",
            "treatment": "Spray copper-based bactericide every 5–7 days during wet weather. Remove heavily infected plant parts. Avoid working in the field when plants are wet to prevent spreading.",
            "prevention": "Use resistant tomato varieties. Disinfect all gardening tools with bleach solution. Practice crop rotation. Do not use overhead irrigation — use drip irrigation instead.",
            "warning": "Particularly damaging to fruit quality. Can cause significant economic loss in commercial farming."
        },
        "hi": {
            "description": "Xanthomonas bacteria se hoti hai, bacterial spot patton, takhnon aur phalon par chote, kaale, paani se bhare daag banata hai. Sankramit phalon par ubhre, khurdarey ghav hote hain jo unhe bechi na jane layak bana dete hain.",
            "treatment": "Bheege mausam mein har 5–7 din mein copper-based bactericide spray karein. Zyada sankramit paudhe ke hisso ko hataiye. Jab podhey bheegehon tab khet mein kaam karne se bachen taaki failaav ruke.",
            "prevention": "Pratirodhi tamatar kismon ka istemaal karein. Bleach solution se sabhi baagbaani auzon ko saaf karein. Fasl badlen. Upar se paani na dein — drip irrigation ka istemaal karein.",
            "warning": "Fhalon ki quality ke liye khaaskar haanikaarak. Vyavsayik kheti mein bhari aarthik hani ho sakti hai."
        }
    },
    "Tomato_Early_blight": {
        "severity": "Moderate",
        "en": {
            "description": "Caused by Alternaria solani fungus, early blight creates dark brown spots with yellow halos and concentric ring patterns on lower leaves first. It spreads upward as the disease progresses.",
            "treatment": "Apply fungicide containing Chlorothalonil, Mancozeb, or Copper. Remove affected lower leaves. Water plants at the base only — never from above. Ensure good air circulation around plants.",
            "prevention": "Mulch around plants to prevent soil splash. Space plants adequately (45–60 cm apart). Avoid excessive nitrogen which promotes lush growth that is more susceptible. Use drip irrigation.",
            "warning": "Common in warm humid weather. Can cause significant defoliation if not controlled early."
        },
        "hi": {
            "description": "Alternaria solani fungus se hoti hai, early blight pehle neeche ke patton par peele halos aur concentric ring patterns ke saath kaale-bhoore daag banata hai. Bimari badhne par upar ki taraf failti hai.",
            "treatment": "Chlorothalonil, Mancozeb, ya Copper wali fungicide lagayen. Prabhavit neeche ke patte hataiye. Podhon ko sirf jaad mein paani dein — upar se kabhi nahi. Podhon ke aaspaas achi hawa sunischit karein.",
            "prevention": "Mitti uchhaalne se rokne ke liye podhon ke aaspaas mulch daalein. Podhon ke beech uchit doori rakhen (45–60 cm). Zyada nitrogen se bachen jo zyada hajam sukhi growth ko badhaata hai. Drip irrigation ka istemaal karein.",
            "warning": "Garm nami mausam mein aam. Shuru mein control na karne par patte bhari taadad mein jhar sakte hain."
        }
    },
    "Tomato_Late_blight": {
        "severity": "Severe",
        "en": {
            "description": "Caused by Phytophthora infestans, late blight causes large, irregular, dark green to brown water-soaked lesions on leaves and stems. White mold may appear on leaf undersides in humid conditions.",
            "treatment": "Apply Metalaxyl or copper-based fungicide immediately. Remove and destroy all infected plant material — burn or bag it, never compost. Apply fungicide preventively during cool, wet weather even before symptoms appear.",
            "prevention": "Plant resistant varieties. Ensure excellent drainage. Avoid overhead watering. Scout crops regularly. Apply preventive copper sprays during high-risk weather periods.",
            "warning": "CRITICAL — Can destroy entire tomato crop within 7–10 days under favorable conditions. Immediate action is essential."
        },
        "hi": {
            "description": "Phytophthora infestans se hoti hai, late blight patton aur takhnon par bade, aniyamit, kaale-hare se bhoore paani se bhare ghav banata hai. Nami mausam mein patton ke neeche safed mold dikh sakta hai.",
            "treatment": "Turant Metalaxyl ya copper-based fungicide lagayen. Sankramit paudhe ki saari samagri hataiye aur nashtaat karein — jalaiye ya bag mein dalein, kabhi khad mein mat daalein. Thande, bheege mausam mein lakshan dikhne se pehle bhi preventively fungicide lagayen.",
            "prevention": "Pratirodhi kismon lagayen. Behtareen drainage sunischit karein. Upar se paani dene se bachen. Faslein niyamit dekhen. Uchch-jokhim wale mausam mein preventive copper sprays lagayen.",
            "warning": "GAMBHIR — Anukool sthitiyon mein 7–10 dinon mein poori tamatar fasl barbad ho sakti hai. Turant action zaroori hai."
        }
    },
    "Tomato_Leaf_Mold": {
        "severity": "Moderate",
        "en": {
            "description": "Caused by Passalora fulva fungus, leaf mold appears as pale green or yellow spots on upper leaf surfaces with olive-green to grayish-brown velvety mold on the undersides. Common in greenhouse tomatoes.",
            "treatment": "Improve greenhouse ventilation immediately. Apply fungicide containing Chlorothalonil or Mancozeb. Remove severely affected leaves. Reduce humidity levels below 85%.",
            "prevention": "Maintain good air circulation. Keep humidity below 85%. Avoid wetting foliage. Use resistant tomato varieties when possible. Space plants properly.",
            "warning": "Thrives in high humidity (above 85%) and temperatures between 22–25°C. Common in enclosed growing spaces."
        },
        "hi": {
            "description": "Passalora fulva fungus se hoti hai, leaf mold patte ki upar wali satah par pale green ya peele daag dikhata hai aur neeche ki taraf jaituni-hare se grayish-bhoore velvet jaise mold hoti hai. Greenhouse tamatar mein aam.",
            "treatment": "Turant greenhouse ventilation sudharen. Chlorothalonil ya Mancozeb wali fungicide lagayen. Buri tarah prabhavit patte hataiye. Nami 85% se neeche rakhen.",
            "prevention": "Achi hawa sunischit karein. Nami 85% se kam rakhen. Pattiyaan bheegane se bachen. Jab ho sake pratirodhi tamatar kismon ka istemaal karein. Podhon ke beech uchit doori rakhen.",
            "warning": "Uchch nami (85% se upar) aur 22–25°C ke beech ke temperature mein tezi se badh'ta hai. Band ugaane ki jagahon mein aam."
        }
    },
    "Tomato_Septoria_leaf_spot": {
        "severity": "Moderate",
        "en": {
            "description": "Caused by Septoria lycopersici fungus, this disease creates many small circular spots with dark borders and light gray centers on lower leaves. Tiny black fruiting bodies are visible in the center of spots.",
            "treatment": "Apply fungicide with Chlorothalonil, Mancozeb, or Copper hydroxide. Remove infected leaves. Avoid overhead watering. Stake plants to improve air circulation around lower leaves.",
            "prevention": "Rotate crops — do not grow tomatoes in same spot for 2 years. Remove crop debris after harvest. Mulch soil to prevent spore splash. Use drip irrigation.",
            "warning": "Primarily affects leaves, not fruit directly, but severe defoliation weakens plant and reduces yield."
        },
        "hi": {
            "description": "Septoria lycopersici fungus se hoti hai, yeh bimari neeche ke patton par kaale kinaron aur halke gray kendr wale bahut saare chote circular daag banati hai. Daagon ke kendr mein tiny kaale fruiting bodies dikhayi dete hain.",
            "treatment": "Chlorothalonil, Mancozeb, ya Copper hydroxide wali fungicide lagayen. Sankramit patte hataiye. Upar se paani dene se bachen. Neeche ke patton ke aaspaas hawa sudharne ke liye podhon ko stake karein.",
            "prevention": "Fasl badlen — 2 saal tak usi jagah tamatar mat ugayen. Fasal ke baad fasl ka malaab hataiye. Beejon ke uchhalne se rokne ke liye mitti mein mulch daalein. Drip irrigation ka istemaal karein.",
            "warning": "Mukhyatah patton ko prabhavit karta hai, phalon ko seedhe nahi, lekin gambhir defoliation podhe ko kamzor karta hai aur paidavar kam karta hai."
        }
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "severity": "Moderate",
        "en": {
            "description": "Two-spotted spider mites (Tetranychus urticae) are tiny pests that suck plant sap. They cause yellowing, stippling (tiny dots) on leaves, and fine webbing on the underside. Severe infestations cause leaf drop.",
            "treatment": "Spray Neem oil or Insecticidal soap every 3–5 days. Use Miticide (Abamectin or Bifenazate) for severe infestations. Spray the undersides of leaves where mites live. Strong water spray can physically remove mites.",
            "prevention": "Keep plants well-watered — mites prefer dry, dusty conditions. Introduce natural predators like ladybugs. Avoid excessive nitrogen fertilizer. Inspect new plants before introducing to garden.",
            "warning": "Reproduce rapidly in hot, dry weather. A small infestation can become severe within 1–2 weeks."
        },
        "hi": {
            "description": "Two-spotted spider mites (Tetranychus urticae) tiny keede hain jo paudhe ka ras chooste hain. Yeh patton par peelaahat, stippling (tiny dots), aur neeche ki taraf patli webbing karte hain. Gambhir infestation mein patte jhar jaate hain.",
            "treatment": "Har 3–5 din mein Neem oil ya Insecticidal soap spray karein. Gambhir infestation ke liye Miticide (Abamectin ya Bifenazate) istemaal karein. Patton ke neeche spray karein jahaan mites rehte hain. Tez paani ki dhaar se mites physically hatayi ja sakti hain.",
            "prevention": "Podhon ko achhe se paani dein — mites sukhi, dhool bhari sthitiyon ko pasand karte hain. Ladybugs jaise prakritik shikari lane ki koshish karein. Zyada nitrogen khad se bachen. Naye podhon ko bageeche mein laane se pehle jaanch karein.",
            "warning": "Garm, sukhe mausam mein tezi se paida hote hain. Chhoti infestation 1–2 hafte mein gambhir ho sakti hai."
        }
    },
    "Tomato__Target_Spot": {
        "severity": "Moderate",
        "en": {
            "description": "Caused by Corynespora cassiicola fungus, target spot creates brown lesions with concentric rings resembling a target on leaves, stems, and fruits. It can cause significant defoliation.",
            "treatment": "Apply Azoxystrobin or Chlorothalonil fungicide. Remove infected plant material. Improve air circulation. Avoid wetting foliage during irrigation.",
            "prevention": "Use disease-free transplants. Maintain proper plant spacing. Practice crop rotation. Remove plant debris after harvest. Avoid excessive nitrogen application.",
            "warning": "Can affect both leaves and fruits. Infected fruits develop sunken dark spots making them unmarketable."
        },
        "hi": {
            "description": "Corynespora cassiicola fungus se hoti hai, target spot patton, takhnon aur phalon par concentric rings wale bhoore ghav banata hai jo target jaise dikhte hain. Isse kaafi patte jhar sakte hain.",
            "treatment": "Azoxystrobin ya Chlorothalonil fungicide lagayen. Sankramit paudhe ka malaab hataiye. Hawa sudharen. Sinchaai ke dauran pattiyaan bheegane se bachen.",
            "prevention": "Bimari-mukt transplants istemaal karein. Uchit paudhe ki doori rakhen. Fasl badlen. Fasal ke baad paudhe ka malaab hataiye. Zyada nitrogen dene se bachen.",
            "warning": "Patton aur phalon dono ko prabhavit kar sakta hai. Sankramit phalon par sunken kaale daag ho jaate hain jo unhe bechi na jane layak bana dete hain."
        }
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "severity": "Severe",
        "en": {
            "description": "Tomato Yellow Leaf Curl Virus (TYLCV) is spread by whiteflies (Bemisia tabaci). Infected plants show upward curling and yellowing of leaves, stunted growth, and flower drop leading to very poor fruit set.",
            "treatment": "There is NO cure once a plant is infected. Remove and destroy infected plants immediately to prevent spread. Control whitefly population using Yellow sticky traps and Imidacloprid insecticide. Protect remaining healthy plants.",
            "prevention": "Use whitefly-resistant or TYLCV-resistant tomato varieties. Install fine mesh nets (50-mesh) over plants. Use reflective silver mulch to repel whiteflies. Monitor and control whitefly populations from early stages.",
            "warning": "CRITICAL — Virus has no cure. Focus on prevention and immediate removal of infected plants. Whiteflies can spread virus within minutes of feeding."
        },
        "hi": {
            "description": "Tomato Yellow Leaf Curl Virus (TYLCV) whiteflies (Bemisia tabaci) dwara failaaya jaata hai. Sankramit podhon mein pattiyaan upar ki taraf curl hoti hain aur peeli pad jaati hain, growth ruk jaati hai, aur phool jhar jaate hain jisse phal bahut kam lagte hain.",
            "treatment": "Ek baar paudha sankramit hone par KOI ilaj nahi hai. Failaav rokne ke liye turant sankramit podhon ko hataiye aur nashtaat karein. Yellow sticky traps aur Imidacloprid insecticide se whitefly aabadi ko control karein. Bache hue swasth podhon ki raksha karein.",
            "prevention": "Whitefly-resistant ya TYLCV-resistant tamatar kismon ka istemaal karein. Podhon ke upar fine mesh nets (50-mesh) lagayen. Whiteflies ko bhagane ke liye reflective silver mulch istemaal karein. Shuru se hi whitefly aabadi ki nigraani aur niyantran karein.",
            "warning": "GAMBHIR — Virus ka koi ilaj nahi hai. Roktham aur sankramit podhon ko turant hatane par dhyan dein. Whiteflies khane ke kuch hi minuton mein virus fail a sakti hain."
        }
    },
    "Tomato__Tomato_mosaic_virus": {
        "severity": "Severe",
        "en": {
            "description": "Tomato Mosaic Virus (ToMV) causes a mosaic pattern of light and dark green or yellow patches on leaves, leaf distortion, stunted growth, and reduced fruit quality. It spreads through infected tools, hands, and plant contact.",
            "treatment": "No cure exists for viral infections. Remove and destroy all infected plants immediately. Disinfect all tools with 10% bleach solution or 70% alcohol after use. Wash hands thoroughly before handling plants.",
            "prevention": "Use certified virus-free seeds and transplants. Disinfect tools regularly. Control aphids which can spread the virus. Do not smoke near plants as tobacco can carry related viruses. Remove infected plants immediately.",
            "warning": "Highly contagious — spreads through touch. Disinfect everything that contacts infected plants."
        },
        "hi": {
            "description": "Tomato Mosaic Virus (ToMV) patton par halke aur gahere hare ya peele patches ka mosaic pattern, patta vikriti, stunted growth, aur kam phal quality ka kaaran banta hai. Yeh sankramit auzon, haathon aur paudhe ke sampark se failta hai.",
            "treatment": "Viral infections ka koi ilaj nahi hai. Turant sabhi sankramit podhon ko hataiye aur nashtaat karein. Upayog ke baad sabhi auzon ko 10% bleach solution ya 70% alcohol se saaf karein. Podhon ko handle karne se pehle haath achhe se dhoyein.",
            "prevention": "Certified virus-mukt beej aur transplants istemaal karein. Auzon ko niyamit saaf karein. Aphids ko control karein jo virus fail a sakte hain. Podhon ke paas dhoomrapaan na karein kyunki tobacco similar viruses le jaata hai. Sankramit podhon ko turant hataiye.",
            "warning": "Bahut sankramak — sparsh se failta hai. Jo bhi cheez sankramit podhon se sampark mein aayi ho use saaf karein."
        }
    },
    "Tomato_healthy": {
        "severity": "None",
        "en": {
            "description": "Your tomato plant is in excellent health with no signs of disease, pest damage, or nutritional deficiency.",
            "treatment": "No treatment required. Your plant is doing great!",
            "prevention": "Continue regular watering at the base. Fertilize every 2–3 weeks. Stake tall plants for support. Check weekly for early signs of pests or disease. Remove suckers for better fruit production.",
            "warning": ""
        },
        "hi": {
            "description": "Aapka tamatar ka podha bahut swasth hai — bimari, keede ya poshak tatva ki kami ke koi lakshan nahi hain.",
            "treatment": "Koi ilaj ki zaroorat nahi. Aapka podha bahut achhe se badh raha hai!",
            "prevention": "Niyamit jaad mein paani dete rahen. Har 2–3 hafte mein khad dein. Lambe podhon ko sahara dein. Har hafte keede ya bimari ke shuruati sanket ki jaanch karein. Behtar phal utpadan ke liye suckers hataiye.",
            "warning": ""
        }
    }
}

IMG_SIZE = (128, 128)

def preprocess(file_bytes):
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_SIZE[1], IMG_SIZE[0]))
    return np.expand_dims(img, axis=0).astype(np.float32)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Plant Disease Detection API is running!"})

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        img_array  = preprocess(file.read())
        preds      = model.predict(img_array, verbose=0)
        pred_index = int(np.argmax(preds))
        pred_class = class_names[pred_index]
        confidence = float(np.max(preds)) * 100
        info       = disease_info.get(pred_class, {})

        top3_idx = np.argsort(preds[0])[::-1][:3]
        top3 = [
            {"class": class_names[i], "confidence": round(float(preds[0][i]) * 100, 2)}
            for i in top3_idx
        ]

        return jsonify({
            "predicted_class": pred_class,
            "confidence":      round(confidence, 2),
            "severity":        info.get("severity", "Unknown"),
            "en": info.get("en", {}),
            "hi": info.get("hi", {}),
            "top3":            top3
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
