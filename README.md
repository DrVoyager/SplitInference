<!--
© Yongzhi Wang, 2025, All Rights Reserved.
-->

# SplitInference 🔐

**Protect inference confidentiality via enclave-based Split Inference on ODML models.**

This open‑source research prototype enables secure inference over vision-enabled deep learning models in adversarial edge settings, by splitting inference across trusted enclaves and untrusted execution layers.

---

## 🚀 Project Highlights

- **RT 1.1: Key‑management + Secure channel:**  
  Utilizes a **Quote Enclave** with Remote Attestation to dynamically negotiate **per-app symmetric encryption keys**, enabling confidential communication between each APP and enclave.

- **RT 1.2: Split Inference Architecture:**  
  Execution is partitioned into **Input**, **Intermediate (Host)**, and **Output** groups; only initial and final layers run inside enclaves—protecting both requests and responses from leakage.

- **Dual-mode Implementation on Keystone:**  
  - *Native mode*: Entire inference pipeline in C/C++ (MobileNetV1)  
  - *Hybrid mode*: Python middle layers (with PyTorch/Numpy) + enclave-only input/output layers (MobileViT)

- **Python‑friendly & model‑agnostic:**  
  The hybrid architecture supports enclave execution of **Python‑based ODML models**, making SplitInference applicable to a wide range of real-world vision models implemented in PyTorch.

- **Strong performance:**  
  Inference overheads range from **27%–430%**:
  
    - MobileNetV1‑0.7‑224 → ~71%  
    - MobileNetV1‑0.5‑224 → ~133%  
    - MobileNetV1‑0.25‑224 → ~430%  
    - MobileViT‑XXS (hybrid) → ~27%  

- **Peer‑reviewed and award‑winning:**  
  Initial work on RT 1.1 and RT 1.2 prototype was published at **FMEC 2025**, receiving the **Best Paper Award**; design details for full RT 1.2 are under preparation.

---

## 📚 Table of Contents

- [Background](#background)  
- [Design Overview](#design-overview)  
- [Implementation Details](#implementation-details)  
- [Benchmark Results](#benchmark-results)  
- [Getting Started](#getting-started)  
- [License & Acknowledgements](#license--acknowledgements)  

---

## Background

This project addresses **Research Objective 1**: defending against **direct attacks** on both inference requests and responses.  
- **RT 1.1** introduces secure key negotiation and encrypted channels via a Quote Enclave trusted by Remote Attestation.  
- **RT 1.2** enables stronger confidentiality protection using a **split‑inference** model across enclaved front/back layers and untrusted host layers.

---

## Design Overview

### 🔑 RT 1.1 – Quote Enclave & Secure Channel
- APP → (ATTEST → Enclave) via **Quote Enclave**, encrypted with `pk_QE` and signed by `sk_a`.
- Accepted enclave receives `spk_a`, proposes symmetric key `K`.
- `K` is transmitted back via enclave → APP.
- APP and enclave establish a **per-app encrypted session** for inference inputs and outputs.

### 🧠 RT 1.2 – Split Inference Architecture
- **Input Enclave**: Decrypts and runs first layer(s). Protects original input confidentiality.
- **Host (Middle Group)**: Untrusted execution of most layers in plaintext, minimizing enclave overhead.
- **Output Enclave**: Final layers—including softmax/logit—encrypts final output to return to APP.
- Even if multiple groups run outside enclaves, intermediate data cannot reconstruct inputs or outputs.

---

## Implementation Details

#### 🧰 Native Mode (C/C++)
- Translation of all layers into C/C++, compiled into Keystone enclaves.
- Used for **MobileNetV1** (variants 0.7, 0.5, 0.25 width multipliers) in controlled enclave environment.

#### 🧪 Hybrid Mode (Python + Enclave C/C++)
- Hosts PyTorch and NumPy to support Python-native model implementations.
- Only input/output enclaves require C/C++ translation.
- Successfully applied to **MobileViT V1 XXS** (~1.3M parameters), with ~27% overhead.

---

## Benchmark Results

Setup:
- **Ubuntu VM (4 vCPUs, 16 GB RAM)** on Google Cloud.
- Keystone system emulated via **QEMU** (2 GB RAM, 1 vCPU) to mimic edge hardware.
- Evaluation on models with **224×224** input images.

| Model                | Inference Overhead vs Baseline |
|----------------------|-------------------------------|
| MobileNetV1‑0.7‑224  | ~71%                          |
| MobileNetV1‑0.5‑224  | ~133%                         |
| MobileNetV1‑0.25‑224 | ~430%                         |
| MobileViT‑XXS        | ~27%                          |

The hybrid split inference approach dramatically lowers overhead compared to the native mode and prior state-of-the-art solutions (142%–577%) without sacrificing confidentiality.

---

## Getting Started

```bash
git clone https://github.com/<your-github-org>/SplitInference.git
cd SplitInference
