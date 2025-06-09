# Final Report  
**Date:** June 2025  
**By:** Tyson Watson and Diana Shadibaeva  

---

## Abstract

This project presents a **cost-effective, modular, and real-time Driver Monitoring System (DMS)** developed using a **Raspberry Pi 5**, **Camera Module V2**, **TensorFlow Lite**, and **Mediapipe**. The system detects key indicators of distracted or drowsy driving, including:

- Cell phone use  
- Yawning  
- Prolonged eye closure (microsleep)

Pop-up alerts notify the driver in real time, with cooldown logic to reduce false alarms and prevent alert spam. By using only **edge devices** and **open-source tools**, this project shows that advanced safety features can be achieved affordably, without relying on cloud infrastructure or expensive hardware.

---

## Introduction

Driver inattention is a major contributor to vehicle accidents worldwide. With rising incidents of distracted and drowsy driving, **Driver Monitoring Systems (DMS)** are becoming essential for improving road safety.

This project aims to build a **real-time, standalone DMS** using accessible, low-cost hardware and open-source software.

### Key Components:
- **Raspberry Pi 5 + Camera Module V2**  
- **TensorFlow Lite** – Detects when a driver is using a phone  
- **Mediapipe** – Tracks facial landmarks to detect yawning and eye closure  

Alerts are delivered via **graphical pop-up windows** that are persistent and hard to ignore, encouraging driver awareness and correction of unsafe behaviors.

The system is designed to be:
- **Modular**
- **Affordable**
- **Easy to deploy**  

---

## Objectives

- Detect and alert for **cell phone use** while driving  
- Detect **yawning** as a sign of fatigue  
- Detect **eye closure** to flag potential sleep/microsleep  
- Deliver **persistent warnings** to discourage unsafe behavior  
- Ensure full operation on **edge hardware** (no cloud processing)

---

## Hardware & Software Overview

###  Hardware:
- **Raspberry Pi 5** – Real-time inference on edge  
- **Camera Module V2** – Compatible and affordable  
- **32GB SD Card** – Stores OS, model files, and code  

### Software:
- **Raspberry Pi OS (64-bit)**  
- **OpenCV** – Image processing  
- **TensorFlow Lite** – Lightweight object detection  
- **Mediapipe** – Face/eye/mouth landmark detection  
- **Tkinter** – GUI alerts  
- **Picamera2** – Raspberry Pi camera interface  



---

##  Development Timeline

### Day 1 – May 26, 2025
- Chose Raspberry Pi 5 after comparing with Orange Pi and Pi Zero 2  
- Selected Camera Module V2 for cost and compatibility  
- Attempted to use YOLOv8 but ran into dependency issues → pivoted to TensorFlow Lite  
- Installed libraries: OpenCV, Ultralytics, Torch  
- Enabled camera preview  

### Day 2 – May 27, 2025
- Installed and tested Hailo AI pipelines (detection, pose, segmentation)  
- Built first version of alert system with Tkinter  
- Began Mediapipe testing on Google Colab for eye detection  

### Day 3 – May 28, 2025
- Refined Region of Interest (ROI) for phone detection  
- Installed Mediapipe and implemented EAR (Eye Aspect Ratio) logic  
- Started modularizing code and added multi-popup support  

### Day 4 – May 30, 2025
- Developed yawning detection using Mediapipe face mesh  
- Created a basic "fatigue tracker" for counting yawns  
- Started integrating all detection features into a single framework  

### Day 5 – June 2, 2025
- Improved eye detection accuracy with better landmark tuning  
- Added persistent alerts for yawning and eye closure  
- Implemented cooldown/reset logic to reduce false positives  

### Day 6 – June 5, 2025
- Tried integrating Hailo and Mediapipe (unsuccessful)  
- Replaced Hailo with TensorFlow Lite for compatibility  

### Day 7 – June 9, 2025
- Successfully integrated TensorFlow Lite object detection (phone detection)

---

## Notes

- The system is **standalone** and requires no internet connection.
- Alerts are designed to be difficult to dismiss unintentionally, promoting active correction of behavior.
- All dependencies are open source and can be installed on a fresh Raspberry Pi OS image.
- Pop-ups and treesholds are **placehorders** and can be easily changed/replaced.

---

## License

This project is open source under the **Apache 2.0 License**. See the [LICENSE](LICENSE) file for details.

---

## Authors

- **Tyson Watson**  
- **Diana Shadibaeva**

