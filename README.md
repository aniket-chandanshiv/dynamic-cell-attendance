# Dynamic Team Operational Tracker 📊

A secure, cloud-hosted tracking application built to streamline daily operations and attendance logging for a 14-person technical team.

## 🚀 Live Application
[View the Live Tracker Here](https://dynamic-cell-attendance-9q2lq595mvnxku2vxrv9j8.streamlit.app/)

## 🏗️ Architecture & Tech Stack
* **Frontend:** Python & Streamlit (Responsive UI, Interactive Dashboards)
* **Backend Database:** Google Sheets (Event-driven data storage)
* **Authentication:** Google Cloud Platform (GCP) IAM Service Accounts 
* **Deployment:** Streamlit Community Cloud via Git integration

## ⚙️ Key Engineering Features
* **Secure API Integration:** Bypassed brittle public-URL scraping by implementing official GCP Service Account authentication, ensuring zero configuration drift and robust read/write capabilities.
* **Automated CI/CD Pipeline:** Connected the GitHub `main` branch directly to the cloud hosting environment for instant, zero-downtime updates upon code commits.
* **Data Integrity:** Engineered strict Python logic to prevent duplicate entries and handle missing data gracefully before pushing to the cloud database.
* **Credential Security:** Implemented strict `.gitignore` protocols and environment variables (TOML secrets) to keep cryptographic keys isolated from public version control.
