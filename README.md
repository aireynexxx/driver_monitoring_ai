# Driver Monitoring AI

Welcome to the Driver Monitoring AI project!

This project is a real-time AI-based **Driver Monitoring System** built to enhance road safety by detecting driver distraction and fatigue. It is designed to run on a Raspberry Pi using a camera module and leverages **MediaPipe**, **TensorFlow Lite**, and **OpenCV** for intelligent monitoring.

##  Features

- **Phone Usage Detection**  
  Detects when the driver is using a mobile phone while driving.

-  **Sleep Detection**  
  Monitors eye aspect ratio (EAR) to determine if the driver has fallen asleep.

- **Fatigue Detection (Yawning)**  
  Detects repeated yawning as a sign of drowsiness or fatigue.

  ## 📸 Requirements

- Raspberry Pi (tested on Pi 5)  
- Pi Camera module  
- Python 3

##  License

This project is licensed under the **Apache 2.0 License** – see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is a proof-of-concept project and should **not be used as a sole safety mechanism**. Always ensure multiple layers of road safety measures are in place.

## Getting Started

Follow these steps to set up and run the project:

1. **Clone the repository**

   ```bash
   git clone https://github.com/aireynexxx/driver_monitoring_ai.git
   cd driver_monitoring_ai
   ```

2. **Create a new Python virtual environment**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**

   * On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```
   * On Windows:

     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Wait for the installation to complete.**

6. **Run the application**

   ```bash
   python3 main.py
   ```

---

Happy coding! ✨
