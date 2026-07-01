# Dent AI Care

Dent AI Care is a full-stack AI-powered Digital Dental Clinic Management System for a BCA final year dental cavity detection project.

## Features

- Patient registration and login
- Doctor and admin login
- Patient profile management
- Appointment booking, rescheduling, and emergency booking
- Dental/X-ray image upload
- CNN-based cavity detection using TensorFlow/Keras
- Original image and AI highlighted image visualization
- Confidence score, affected tooth area, recommendations
- PDF diagnosis report download
- Print and share report actions
- Email/SMS notification queue
- Location-based nearest clinic suggestions
- Patient, doctor, and admin dashboards

## Project Structure

```text
DentAI/
  app/
    static/
      css/style.css
      js/app.js
      uploads/
      highlights/
      reports/
    templates/
    ai_service.py
    models.py
    report_service.py
    routes.py
  dataset/
    cavity/
    normal/
  models/
  train_model.py
  run.py
  requirements.txt
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run With SQLite Demo Database

```bash
python run.py
```

Open `http://127.0.0.1:5000`.

Demo logins:

- Admin: `admin@dentaicare.com` / `admin123`
- Doctor: `doctor@dentaicare.com` / `doctor123`
- Patient: create from registration page

## Use MySQL

Create a MySQL database:

```sql
CREATE DATABASE dent_ai_care;
```

Set environment variable before running:

```bash
set DATABASE_URL=mysql+pymysql://root:your_password@localhost/dent_ai_care
python run.py
```

The tables are created automatically on first run.

## Train CNN Model

Your dataset is already arranged correctly:

```text
dataset/
  cavity/
  normal/
```

Train the model:

```bash
python train_model.py
```

The trained model is saved to:

```text
models/dent_cavity_cnn.keras
```

After that, uploads in the AI Analysis page will use the CNN model. If the model file is missing, the app still runs using a demo image-processing fallback, useful for presentation before training.

## Final Year Project Note

This project is built for academic demonstration. AI predictions should be treated as clinical decision support only. A qualified dentist should confirm the final diagnosis.
