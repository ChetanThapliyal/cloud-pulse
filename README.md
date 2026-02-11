# ☁️ Cloud Pulse v2
>
> **Global Operations Monitoring Dashboard**

<div align="center">

![Cloud Pulse Banner](https://img.shields.io/badge/Status-Live-success?style=for-the-badge&logo=appsignal&logoColor=white)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Tailwind%20%7C%20SQLite-blue?style=for-the-badge&logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

</div>

> [!IMPORTANT]
> **This is a demo app created by agents in Antigravity, testing Vibe Coding with cloud and DevOps interests.**

## 📖 Overview

**Cloud Pulse** is a state-of-the-art, real-time cloud monitoring dashboard designed to provide instant visibility into your global infrastructure's health.

Built with performance and aesthetics in mind, it features a **Glassmorphism UI** that delivers critical metrics—latency, uptime, and server status—at a glance. Whether you're tracking endpoints in Tokyo, London, or New York, Cloud Pulse keeps your finger on the pulse of your network.

---

## ✨ Key Features

### 🌍 Live Threat Map

Visualize your infrastructure on a global scale.

- **Real-time Geolocation**: Servers are mapped to their physical coordinates.
- **Status Indicators**: Pulsating beacons indicate server status (🔵 Up, 🔴 Down).
- **Interactive**: Hover over nodes for instant details.

### 📊 Real-Time Analytics

Data visualizations that move as fast as your network.

- **Global Latency Stream**: Live-updating area chart tracking network performance/lag in milliseconds.
- **Uptime Health Ring**: Instant visual feedback on overall system availability.

### ⚡ Instant Diagnostics

- **Multi-Protocol Checks**: Supports standard HTTP/HTTPS health checks and ICMP Pings.
- **History Logging**: Persists performance data to a local SQLite database for historical trend analysis.
- **Async Architecture**: Non-blocking monitoring powered by Python's `asyncio` and `httpx`.

---

## 🛠️ Technology Stack

### **Frontend**

- **Core**: Vanilla HTML5, JavaScript (ES6+), Chart.js
- **Styling**: Tailwind CSS (via CDN) for rapid, utility-first design.
- **Visuals**: Chart.js for data visualization, Google Fonts (Exo 2) for typography.
- **Design System**: Custom Glassmorphism UI with translucent panels and neon accents.

### **Backend**

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High performance, easy to learn.
- **Server**: [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server.
- **Database**: SQLite (via `aiosqlite`) for lightweight, async persistence.
- **Networking**: `httpx` for asynchronous HTTP requests.

---

## 🚀 Getting Started

Follow these instructions to get your Operations Center running locally.

### Prerequisites

- Python 3.8+
- Modern Web Browser (Chrome/Firefox/Edge)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cloud-pulse.git
cd cloud-pulse
```

### 2. Backend Setup

Navigate to the server directory and install dependencies.

```bash
cd server
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Start the API server:

```bash
python main.py
# Server will start on http://0.0.0.0:8000
```

### 3. Client Setup

Open a new terminal, navigate to the client directory, and serve the frontend.

```bash
cd client
python3 -m http.server 8080
```

### 4. Access the Dashboard

Open your browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

---

## 📸 Usage Guide

1. **Global Overview**: The landing page shows the Map and Aggregated Charts.
2. **Server Health**: Click "Server Health" in the sidebar to view detailed monitored endpoints.
3. **Simulation**: To test the "Down" state, modify `services_to_monitor` in `server/main.py` to include an invalid URL or shut down a local service.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Generated with ❤️ by <b>Antigravity Agents</b>
</p>
