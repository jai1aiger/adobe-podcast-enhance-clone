# Adobe Podcast Enhance Speech - Reverse Engineering & 100% Local Clone

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jai1aiger/adobe-podcast-enhance-clone/blob/main/quick_launch.ipynb)
[![Local Quick Launch](https://img.shields.io/badge/Windows-1--Click%20Launch.bat-blue?logo=windows)](launch.bat)
[![Local Web UI](https://img.shields.io/badge/Local%20UI-http%3A%2F%2Flocalhost%3A7860-success?logo=googlechrome)](http://127.0.0.1:7860)

> Reverse-engineering analysis of **[podcast.adobe.com/en/enhance](https://podcast.adobe.com/en/enhance)** using **REA** (`morluto/rea`) and a complete 100% offline, local open-source implementation.

---

## ⚡ Quick Launch Links

| Method | Access Link | Description |
| :--- | :--- | :--- |
| **1-Click Cloud (Free GPU)** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jai1aiger/adobe-podcast-enhance-clone/blob/main/quick_launch.ipynb) | Runs in your browser via Google Colab with free T4 GPU. |
| **1-Click Windows** | Double-click [`launch.bat`](launch.bat) | Auto-installs dependencies and opens UI in default browser. |
| **Local Web Interface** | [http://127.0.0.1:7860](http://127.0.0.1:7860) | Direct browser link when server is active. |

---

## 🔍 Reverse-Engineering Findings (via REA)

* **REA Evidence ID:** `ev_fcdc0fd347c011f54fd0a3990ebbb959ea5c0bed2949639e2133bd0eceb5ea19`
* **Inventory Manifest:** `agm_14af744ed135d94d44662665340ea7f9d0f05364c4181136f388dc9989dcaa28`
* **Target:** Adobe Podcast Enhance Speech Web Client

### 1. Internal Architecture & Service Codename
* **Internal Service Name:** `Phonos`
* **Internal API Key:** `phonos-server-prod`
* **Client Architecture:** Webpack bundle (`wp_flex_index.ca7050cd2d913a41ab4a.js`) + Adobe IMS authentication (`imslib.min.js`).

### 2. Discovered AI Model System
The application client codebase contains logic handling **two distinct model versions**:
* **`ModelVersion.$.v1`**: Aggressive noise suppression and high vocal isolation.
* **`ModelVersion.$.v2`**: Upgraded neural vocoder with softer dereverberation and natural room acoustics.

### 3. Dual-Stream WebAudio Hotswapping
The instant A/B preview toggle on the website runs two parallel, phase-locked audio tracks using WebAudio:
```javascript
sourceNodePair.original.start((0, TimeHelper.X5)(when), ...);
sourceNodePair.enhanced?.start((0, TimeHelper.X5)(when), ...);
```
When the user toggles the "Enhance Speech" switch, the `hotswap()` method modulates a `GainNode` between the tracks without reloading or desyncing playback.

### 4. Client vs. Server Boundary
* `AudioWorklet`: **0 instances**
* `ONNX` / `TensorFlow.js`: **0 instances**
* **Conclusion:** Zero neural inference runs client-side. The website acts solely as an upload orchestrator; all audio processing is dispatched to server-side GPU workers.

---

## 🚀 The Local Open-Source Clone

This repository provides an offline, self-hosted clone of Adobe Enhance Speech using open-source deep generative models (**Resemble Enhance** & **DeepFilterNet**) with an interactive local Web UI.

### Features
* **100% Offline & Private:** Audio never leaves your computer.
* **No File Limits:** No 30-minute daily caps or file size restrictions.
* **Dual Engines:**
  * **Resemble Enhance:** 2-stage neural vocoder + latent diffusion (matches Adobe Podcast Studio sound).
  * **DeepFilterNet:** Ultra-fast, low-latency Rust/CPU model for laptops and PCs without dedicated GPUs.
* **Interactive Web UI:** Drag-and-drop audio with instant waveform preview.

---

## 🛠️ Manual CLI Instructions

### 1. Installation
Clone this repository and install dependencies:
```bash
git clone https://github.com/jai1aiger/adobe-podcast-enhance-clone.git
cd adobe-podcast-enhance-clone
pip install -r requirements.txt
```

*(If you have an NVIDIA GPU, install PyTorch with CUDA support first:)*
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 2. Launch Local Web UI
```bash
python app.py
```
Open your browser to `http://127.0.0.1:7860`.

### 3. Command-Line (CLI) Batch Processing
```bash
# Enhance using Resemble AI (Studio Sound)
python cli.py input_noisy.wav output_studio.wav --engine resemble

# Fast CPU Denoising (DeepFilterNet)
python cli.py input_noisy.wav output_clean.wav --engine deepfilter
```

---

## ⚖️ License & Attribution
* Reverse-engineering analysis conducted via [REA](https://github.com/morluto/rea).
* Neural vocoder implementations powered by [Resemble Enhance](https://github.com/resemble-ai/resemble-enhance) (Apache-2.0) and [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) (MIT).
* For educational and clean-room research purposes.
