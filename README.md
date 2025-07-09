# EOTSS Hosting Recommendation System

A decision-support tool for the Executive Office of Technology Services and Security (EOTSS), Commonwealth of Massachusetts. This project helps users determine the most suitable hosting environment (AWS, on-prem cloud, or physical infrastructure) for their application based on technical and business criteria.

## Features
- **CLI/GUI Tool**: Interactive command-line and desktop GUI for assessments
- **Web App**: Modern, accessible web interface with progress tracking, print/copy features, and government-style design
- **Customizable**: Easily extend questions and logic
- **Export/Print**: Copy or print results for reporting

---

## Prerequisites
- Python 3.7+
- pip (Python package manager)

---

## Installation
1. **Clone or download the repository**
2. **Navigate to the project folder**
3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Command-Line Interface (CLI) & GUI Tool

The CLI/GUI tool is in `eotss_hosting_recommendation_with_app_age.py`.

#### **Run the CLI Tool**
```sh
python eotss_hosting_recommendation_with_app_age.py
```
- Answer the questions in your terminal.
- Review, edit, and save your results as prompted.

#### **Run the GUI Tool**
```sh
python eotss_hosting_recommendation_with_app_age.py --gui
```
- A desktop window will open for you to complete the assessment.
- Results are shown in the app.

#### **Command-Line Arguments**
You can also provide answers directly as arguments (see `--help`):
```sh
python eotss_hosting_recommendation_with_app_age.py --fault_tolerance high --latency low ...
```

---

### 2. Web App (Flask)

The web app is in `app.py` and uses the `templates/` folder for HTML.

#### **Run the Web App**
```sh
python app.py
```
- Open your browser and go to [http://localhost:5000](http://localhost:5000)
- Complete the assessment in your browser
- Features:
  - Progress bar
  - Print-friendly results
  - One-click copy of results
  - Government-style, accessible design

---

## Project Structure
```
EOTSS/
├── app.py                        # Flask web app
├── eotss_hosting_recommendation_with_app_age.py  # CLI/GUI tool
├── requirements.txt              # Python dependencies
├── templates/
│   ├── form.html                 # Web app assessment form
│   └── result.html               # Web app results page
└── README.md                     # Project documentation
```

---

## Customization
- To add or change questions, edit the `QUESTIONS` and `CLOUD_READINESS_QUESTIONS` lists in both `app.py` and `eotss_hosting_recommendation_with_app_age.py`.
- To change scoring logic, update the `score_answers` function in both files.

---

## License
This project is intended for internal use by the Commonwealth of Massachusetts. Contact EOTSS for more information. 