# Lume 

## 🔥 Inspiration  
The **LA Wildfires** have devastated local communities, and with **climate change** driving an unprecedented rise in wildfires worldwide, the impact is catastrophic. Thousands of **lives, homes, and wildlife habitats** have been lost, and wildfires contribute to nearly **one-third of global CO₂ emissions**. **Early detection** is crucial for prevention and effective crisis management. *Lume* aims to provide a **multi-point detection system** to identify **smoke and fires** quickly and alert the authorities in **real-time**.  

## ⚡ What It Does  
Lume is an **AI-powered wildfire detection system** that:  
✅ Detects **smoke and fire** in **images and videos** using **deep learning**.  
✅ **Analyzes video frames** in **real time** and highlights detected fires with **bounding boxes**.  
✅ **Automatically alerts emergency services (911)** if a fire is detected.  
✅ Provides a **user confirmation system**—if the user declines an alert but fire is still detected, the system will continue prompting.  
✅ Features a **dashboard** built with **Flask, JavaScript, HTML, and CSS** for **monitoring detections**.  

## 🛠️ How We Built It  
Lume was developed using:  
- **YOLOv8** for **real-time fire detection**.  
- **OpenCV** for **video processing and frame analysis**.  
- **Flask** to manage the **backend and API integrations**.  
- **JavaScript, HTML, and CSS** for an **interactive dashboard**.  
- **Twillo for API Key Integration** to **automatically contact emergency services** when needed.  

## 🚧 Challenges We Faced  
- **False Detections:** The **YOLOv8 model** initially struggled with **accuracy**. We fine-tuned it by preprocessing the dataset using **data augmentation techniques** like **color space transformation**.  
- **Dependency Issues:** Installing **Flask dependencies** was challenging due to **Python version incompatibility**, requiring **troubleshooting and version adjustments**.  

## 📚 What We Learned  
- How to **integrate API keys** to **automate emergency calls** after **sustained fire detection** (5 straight seconds across **5 video frames**).  
- **Collaborating as a team**—many of us had only worked on **solo projects** before this.  
- **Fine-tuning a deep learning model** through **data augmentation** to improve **accuracy**.  

## 🚀 What's Next for Lume  
🔹 **Integration with CCTV cameras** for **continuous wildfire monitoring**.  
🔹 **Google Maps API integration** to **pinpoint fire locations** and **share them with authorities**.  
🔹 **Web-based detection system**—users will be able to **upload images/videos** to check for **potential fire threats**.  
