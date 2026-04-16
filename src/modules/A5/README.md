# Clinic Management System 🏥

A database management system project developed for the Semester 4 DBMS coursework. This application provides a comprehensive UI and robust backend to securely manage patient clinical records, vaccination inventories, and patient logic.

## 👥 Team Members
- Dipesh Jain
- Bharadwaj Chikka
- Aditya Ekka

## 🛠️ Technology Stack
- **Frontend:** Streamlit 
- **Backend API:** Flask
- **Database:** MongoDB (PyMongo)
- **Data Visualizations:** Pandas

## 🚀 Features
- **Patient Management:** Track patient demographics, allergies, and contraindications.
- **Immunization Tracking:** Log and monitor vaccine doses safely.
- **Automated Logic Checks:** Prevent vaccines if a patient has a flagged contraindication. 
- **Analytics Dashboard:** Visual representation of key metrics and vaccination trends.

## 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-link>
   cd DBMS-Project/Chatgpt
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you have Flask, Streamlit, PyMongo, requests, and pandas installed)*

3. **Start the database:**
   Ensure your local MongoDB instance is running on port `27017` and the `clinic_db` is initialized.

4. **Run the Backend (Flask):**
   Open a terminal and run the API:
   ```bash
   python flask_app.py
   ```
   The backend will run on `http://127.0.0.1:5005`.

5. **Run the Frontend (Streamlit):**
   Open a separate terminal and run the UI:
   ```bash
   streamlit run main.py
   ```

## 📝 Future Updates
- Advanced user authentication
- Exporting reports to PDF
- Complete testing suite integration
