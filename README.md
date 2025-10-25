# 🎨 Superpixel Mosaic Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Transform any image into stunning artistic mosaics using intelligent superpixel segmentation**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [How It Works](#-how-it-works)

</div>

---

## 📸 Demo

<table>
  <tr>
    <td><img src="assets/original.jpg" alt="Original Image" width="300"/><br/><sub><b>Original Image</b></sub></td>
    <td><img src="assets/mosaic.jpg" alt="Mosaic Output" width="300"/><br/><sub><b>Mosaic Output</b></sub></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><img src="assets/segments.jpg" alt="Superpixel Segments" width="300"/><br/><sub><b>Superpixel Segmentation</b></sub></td>
  </tr>
</table>

---

## ✨ Features

### 🖼️ **Smart Segmentation**
- Object-based segmentation using SLIC (Simple Linear Iterative Clustering)
- Automatically identifies meaningful regions in images
- No grid-based cutting - preserves object boundaries

### 🎯 **Intelligent Tile Matching**
- **Color Analysis**: RGB Euclidean distance for color similarity
- **Texture Analysis**: Gabor filter convolution for pattern matching
- **Combined Scoring**: Weighted algorithm for optimal tile selection

### 🎨 **Customizable Output**
- **Adjustable Superpixels**: Control mosaic granularity (20-500 segments)
- **Alpha Blending**: Fine-tune blend between original and mosaic (0.0-1.0)
- **Interactive Preview**: Click any tile to view the original source image

### 🌐 **Dual Interface**
- **Web Application**: Beautiful Flask-based browser interface
- **Desktop Application**: Tkinter GUI for offline use

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **OpenCV** | Image processing and manipulation |
| **scikit-image** | SLIC superpixel segmentation |
| **NumPy** | Numerical computations |
| **Flask** | Web application framework |
| **Tkinter** | Desktop GUI |

---

## 📋 Prerequisites

- Python 3.8 or higher
- Anaconda (recommended) or pip
- 20+ tile images (any photos/pictures)

---

## 🚀 Installation

### Step 1: Clone the Repository
```bash