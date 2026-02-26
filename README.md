# Real-Time Fraud Detection System

An industry-grade, end-to-end Machine Learning system for real-time fraud detection, built with FastAPI and Streamlit and deployed on Render.

## Overview

This project implements a production-style fraud detection pipeline that:

- Serves real-time predictions via a FastAPI REST API  
- Applies industry-standard decision logic (Approve / Review / Block)  
- Displays results through an executive-style Streamlit dashboard  
- Is deployed and accessible via cloud infrastructure  

## Architecture

User  
→ Streamlit Frontend  
→ FastAPI Backend (Render)  
→ ML Model  

## 🛠 Tech Stack

**Backend**
- Python 3.11
- FastAPI
- Uvicorn
- SQLAlchemy

**Machine Learning**
- Scikit-learn
- Pandas, NumPy
- Joblib

**Frontend**
- Streamlit

**Deployment**
- GitHub
- Render (API)
- Streamlit Cloud (UI)

## Key Features

- **Real-Time Fraud Scoring**
- **Risk Tier Classification** (LOW / MEDIUM / HIGH)
- **Decision Mapping**
  - LOW → Approved
  - MEDIUM → Review Required
  - HIGH → Blocked
- **Confidence & Risk Explanation**
- **Executive-Style UI**

## 🔗 Live Links

- **GitHub Repository**  
  https://github.com/rishitha28-jpg/fraud-detection-fastapi

- **Backend API (Render)**  
  https://fraud-detection-fastapi-ouqr.onrender.com

- **Swagger API Docs**  
  https://fraud-detection-fastapi-ouqr.onrender.com/docs

- **Health Check**  
  https://fraud-detection-fastapi-ouqr.onrender.com/health

