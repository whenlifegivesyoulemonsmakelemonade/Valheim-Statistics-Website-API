# Valheim Dedicated Server Statistics – Website & API

A self-hosted **statistics, monitoring, and player analytics platform** for Valheim Dedicated Servers.  
This project consists of a **Linux-only backend API** and a **web-based frontend dashboard** that provides real-time and historical insights into server and player activity.

The goal is to offer **deep visibility into server health, player behavior, and world state**, with optional mod-based extensions for advanced features like map interaction and player data visualization.

---

## ✨ Features

### 📊 Server Statistics
- **Server Name**
- **Server IP / Join Code**
- **World Name**
- **Player Count**
- **Save Timestamp** (also last backup time)
- **Server Activity**
- **Server Status**
  - Launching
  - Online
  - Offline
  - Error states
- **Server Uptime**
  - Online for
  - Last online
  - Since …
- **Memory Usage**
- **CPU Usage**
- **Server Process PID**
- **Start Arguments**
- **Logs** (server & API)

---

### 👥 Player Statistics *(Completed)*
- **Profile management for each player**
- **Players online for / last online / since …**
- **Total playtime per player**

> ✅ Player-related statistics and tracking are already implemented in the API.

---

## 🧪 Planned / Mod-Based Features

These features may be added later via custom Valheim mods:

### 🗺️ Interactable Map
- Player positions
- Player inventories & active effects
- Death count per player

### 🌍 World Information
- Map seed
- World day & time

---

## 🛠️ Tech Stack

### Backend API
- **Language:** Python *(may be rewritten in C++ once feature-complete)*
- **Platform:** Linux only (for now)
- **Purpose:**
  - Collect server metrics
  - Track player activity
  - Expose a REST-style API for the frontend

### Frontend Website
- **HTML / CSS / JavaScript**
- **GLSL** for visual effects and data-driven animations
- **Purpose:**
  - Real-time dashboard
  - Historical statistics visualization
  - Player profiles

> 🚧 Work on the website has not been started yet.

---

- Can run fully **on one machine** or **split across multiple machines**
- Designed to be **self-hosted**
- Optional public exposure via Cloudflare

---

## 🚀 How to Self-Host

> *(To be completed)*

### Docker
- Docker Image / Docker Compose *(maybe coming)*
  - Configuring `.env`

### Systemd Setup
- Setup Systemd services to start:
  - Dedicated Server
  - API
  - Website

#### Deployment Options
- On the **same machine**
  - Linked
  - Separate
- On **different machines**

### Public Hosting via Cloudflare
- Setup domain
- Setup Zero Trust Tunnel

---

## 🤝 How to Contribute

> *(To be completed)*

### Documentation
- API docs
- Setup guides
- Development notes

---

## 📌 Project Status

- ✔ Player statistics implemented
- ✔ Core API structure in place
- ❌ Website not started
- ❌ Deployment automation pending
- ❌ Mod-based features not implemented

This project is actively evolving and subject to major changes.

---

## 📜 License

*(Add your license here)*
