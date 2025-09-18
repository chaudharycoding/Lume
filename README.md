# 🔥 Lume – AI-Powered Wildfire Detection  

## 🌍 Inspiration  
The **LA Wildfires** have left behind unimaginable destruction—displacing families, destroying homes, and wiping out wildlife habitats. With **climate change** fueling a global surge in wildfires, the threat is only growing. Wildfires are now responsible for nearly **one-third of global CO₂ emissions**. The key to minimizing their impact lies in **early detection** and **rapid response**.  

That’s where **Lume** comes in—a smart, **multi-point detection system** designed to spot **smoke and flames in real time** and alert emergency responders before disaster escalates.  

---

## ⚡ What It Does  
Lume is an **AI-powered wildfire monitoring system** that:  
- ✅ Detects **smoke and fire** in **images and live video feeds** using **deep learning**.  
- ✅ Processes video **frame by frame in real time**, marking fire zones with **bounding boxes**.  
- ✅ **Automatically alerts emergency services (911)** when fire is detected.  
- ✅ Features a **user confirmation system**—if the user dismisses the alert but the fire persists, the system continues prompting until resolved.  
- ✅ Includes an **interactive dashboard** (Flask + JS + HTML + CSS) for **real-time monitoring and alerts**.  

---

## 🛠️ How We Built It  
- **YOLOv8** → real-time fire detection  
- **OpenCV** → video processing and frame analysis  
- **Flask** → backend + API integrations  
- **JavaScript, HTML, CSS** → dashboard UI  
- **Twilio API** → automated emergency service alerts  

---

## 🚧 Challenges We Overcame  
- **False Positives:** Initially, YOLOv8 produced **inaccurate detections**. We improved performance by **fine-tuning the model** and applying **data augmentation** techniques (e.g., color transformations, contrast adjustment).  
- **Dependency Conflicts:** Flask dependencies were incompatible with some Python versions—resolving this required **debugging, testing, and version control adjustments**.  

---

## 📚 Key Learnings  
- Integrating **API services** for **automated emergency response** triggered by sustained fire detection (≥5 seconds across multiple frames).  
- The value of **team collaboration**—transitioning from solo projects to coordinated teamwork.  
- Improving model accuracy through **data preprocessing and augmentation**.  

---

## 🚀 What’s Next for Lume  
- 🔹 **CCTV integration** for **continuous wildfire surveillance**  
- 🔹 **Google Maps API integration** to **pinpoint fire locations** and share them with responders  
- 🔹 A **web-based detection tool** allowing users to upload **images/videos** for instant fire threat analysis  
- 🔹 **Mobile app support** for community-driven wildfire reporting  

---

## At a Glimpse!
![Demo](demo.gif)
