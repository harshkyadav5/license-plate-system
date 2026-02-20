# Frontend — License Plate Recognition System

This is the **React + Tailwind CSS frontend** for the AI-powered License Plate Recognition & Smart Parking system.
It communicates with the FastAPI backend to:

* Upload vehicle images
* Detect license plates using AI
* Display OCR results
* Show parking entry/exit logs (history)

---

## Tech Stack

* React (Vite)
* Tailwind CSS
* Axios
* Context API (Authentication)
* React Router

---

## Features

* Image upload with preview
* AI detection result display
* Confidence score visualization
* Automatic history refresh
* Parking entry / exit tracking
* JWT authentication ready
* Clean modular component architecture

---

## Setup & Installation

### 1.Clone repository
```bash
git clone <repo-url>
cd frontend
```

### 2.Install dependencies
```bash
npm install
```

### 3.Start development server
```bash
npm run dev
```

App runs on:
```bash
http://localhost:5173
```
---
Backend API Integration

The frontend expects the backend to run on:
```bash
http://127.0.0.1:8000
```