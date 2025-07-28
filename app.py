from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key'  # Change this in production

# Email configuration for demo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jimixoso@gmail.com'  # Replace with your email, should be something like no-reply@mass.gov
app.config['MAIL_PASSWORD'] = 'xqga lnyf kjav qtsq'     # Replace with your app password, should be server app password for the EOTSS server.
app.config['MAIL_DEFAULT_SENDER'] = 'jimixoso@gmail.com' # Should be same as MAIL_USERNAME

mail = Mail(app)

# QUESTIONS: Main assessment questions for application requirements.
# Each question is a dict with a key, prompt, valid options, and a help string for user guidance.
QUESTIONS = [
    {"key": "fault_tolerance", "prompt": "Fault Tolerance (Low/Moderate/High):", "options": ["low", "moderate", "high"], "help": "High = must always be available (e.g., 24/7 critical), Moderate = some downtime acceptable, Low = downtime is fine"},
    {"key": "latency", "prompt": "Latency Sensitivity (Low/Moderate/High):", "options": ["low", "moderate", "high"], "help": "High = needs instant response (e.g., real-time), Moderate = some delay is ok, Low = delay is fine"},
    {"key": "data_volume", "prompt": "Data Volume (Low/Moderate/High):", "options": ["low", "moderate", "high"], "help": "High = large datasets (TBs+), Moderate = moderate data, Low = small data"},
    {"key": "security", "prompt": "Security Needs (Low/Moderate/High):", "options": ["low", "moderate", "high"], "help": "High = sensitive data (e.g., PII, HIPAA), Moderate = some sensitive data, Low = public or non-sensitive"},
    {"key": "migration", "prompt": "Migration Complexity (Low/Moderate/High):", "options": ["low", "moderate", "high"], "help": "High = hard to move, many dependencies; Low = easy to move"},
    {"key": "ops_expertise", "prompt": "Operational Expertise (aws/vmware/minimal):", "options": ["aws", "vmware", "minimal"], "help": "AWS = team knows AWS, VMware = team knows on-prem/cloud, Minimal = little expertise"},
    {"key": "budget", "prompt": "Budget Sensitivity (Low/Moderate/High):", "options": ["low", "moderate", "high"], "help": "Low = cost is a concern, High = cost is not a concern"},
    {"key": "compliance", "prompt": "Does your application have specific compliance requirements (yes/no)?", "options": ["yes", "no"], "help": "Yes = must meet regulations (e.g., HIPAA, CJIS)"},
    {"key": "scalability", "prompt": "Do you expect rapid growth or fluctuating workloads (yes/no)?", "options": ["yes", "no"], "help": "Yes = user base or data may grow quickly or unpredictably"},
]

# CLOUD_READINESS_QUESTIONS: Questions to assess the application's cloud readiness.
# Used to determine if the app is 'modern' or 'legacy' for scoring purposes.
CLOUD_READINESS_QUESTIONS = [
    {"key": "containerized", "prompt": "Is the app containerized or able to be containerized (e.g., Docker)?", "options": ["yes", "no"], "help": "Yes = can run in Docker or similar, No = needs special hardware or OS"},
    {"key": "compatible_runtime", "prompt": "Does the app run on a cloud-supported OS/runtime (e.g., modern Linux, Windows Server 2016+)?", "options": ["yes", "no"], "help": "Yes = runs on modern Linux/Windows, No = needs legacy OS"},
    {"key": "no_hardware_deps", "prompt": "Does the app avoid relying on physical hardware or specialized networking?", "options": ["yes", "no"], "help": "Yes = no special cards/devices, No = needs hardware access"},
]

def score_answers(answers):
    """
    Calculate the hosting recommendation based on user answers.
    Args:
        answers (dict): Dictionary of answers to all questions.
    Returns:
        tuple: (recommendation (str), scores (dict), explanations (list of str))
    """
    cloud_ready_score = sum(1 for q in CLOUD_READINESS_QUESTIONS if answers.get(q["key"]) == "yes")
    app_age = "modern" if cloud_ready_score >= 2 else "legacy"
    answers["app_age"] = app_age
    scores = {"aws": 0, "on_prem_cloud": 0, "physical": 0}
    if answers["fault_tolerance"] == "high": scores["aws"] += 2
    elif answers["fault_tolerance"] == "moderate": scores["on_prem_cloud"] += 1
    if answers["latency"] == "high": scores["physical"] += 2
    elif answers["latency"] == "moderate": scores["on_prem_cloud"] += 1
    if answers["data_volume"] == "high": scores["on_prem_cloud"] += 2
    elif answers["data_volume"] == "moderate": scores["aws"] += 1
    else: scores["aws"] += 2
    if answers["security"] == "high": scores["physical"] += 2
    elif answers["security"] == "moderate": scores["on_prem_cloud"] += 2
    else: scores["aws"] += 1
    if answers["app_age"] == "modern": scores["aws"] += 2
    else: scores["physical"] += 2
    if answers["migration"] == "low": scores["aws"] += 2
    elif answers["migration"] == "moderate": scores["on_prem_cloud"] += 1
    else: scores["physical"] += 2
    if answers["ops_expertise"] == "aws": scores["aws"] += 2
    elif answers["ops_expertise"] == "vmware": scores["on_prem_cloud"] += 2
    else: scores["physical"] += 1
    if answers["budget"] == "low": scores["aws"] += 2
    elif answers["budget"] == "moderate": scores["on_prem_cloud"] += 1
    if answers["compliance"] == "yes": scores["on_prem_cloud"] += 2; scores["aws"] += 1
    else: scores["aws"] += 1
    if answers["scalability"] == "yes": scores["aws"] += 2; scores["on_prem_cloud"] += 1
    else: scores["physical"] += 1
    recommendation = max(scores, key=scores.get)
    explanations = []
    if recommendation == "aws":
        if answers["fault_tolerance"] == "high": explanations.append("High fault tolerance needs are best met by AWS.")
        if answers["budget"] == "low": explanations.append("Low budget sensitivity favors AWS's cost efficiency.")
        if answers["app_age"] == "modern": explanations.append("Modern, cloud-ready applications are ideal for AWS.")
        if answers["migration"] == "low": explanations.append("Low migration complexity makes AWS adoption easier.")
        if answers["ops_expertise"] == "aws": explanations.append("Your team has AWS expertise.")
        if answers["scalability"] == "yes": explanations.append("AWS is well-suited for scalable workloads.")
        if answers["compliance"] == "no": explanations.append("No strict compliance requirements allow for public cloud hosting.")
    elif recommendation == "on_prem_cloud":
        if answers["fault_tolerance"] == "moderate": explanations.append("Moderate fault tolerance can be handled by on-prem cloud.")
        if answers["latency"] == "moderate": explanations.append("Moderate latency sensitivity is suitable for on-prem cloud.")
        if answers["data_volume"] == "high": explanations.append("High data volume is often better managed on-premises.")
        if answers["security"] == "moderate": explanations.append("Moderate security needs are met by on-prem cloud.")
        if answers["migration"] == "moderate": explanations.append("Moderate migration complexity fits on-prem cloud.")
        if answers["ops_expertise"] == "vmware": explanations.append("Your team has VMware/on-prem expertise.")
        if answers["compliance"] == "yes": explanations.append("Compliance requirements are often easier to meet on-premises.")
        if answers["scalability"] == "yes": explanations.append("On-prem cloud can support some scalability needs.")
    elif recommendation == "physical":
        if answers["latency"] == "high": explanations.append("High latency sensitivity is best served by physical infrastructure.")
        if answers["security"] == "high": explanations.append("High security needs are best met by physical hosting.")
        if answers["app_age"] == "legacy": explanations.append("Legacy applications are often better suited to physical servers.")
        if answers["migration"] == "high": explanations.append("High migration complexity favors staying on physical infrastructure.")
        if answers["ops_expertise"] == "minimal": explanations.append("Minimal cloud/on-prem expertise may require physical hosting.")
        if answers["scalability"] == "no": explanations.append("Physical infrastructure is suitable for stable, non-scaling workloads.")
    return recommendation, scores, explanations

def send_eotss_notification(agency_info, results_data):
    """
    Send notification email to EOTSS with assessment results.
    """
    try:
        msg = Message(
            subject=f"EOTSS Hosting Assessment - {agency_info['agency_name']} - {results_data['date']}",
            recipients=['jimixoso@mit.edu'],
            body=f"""
Dear EOTSS Team,

A hosting assessment has been completed for {agency_info['agency_name']}.

ASSESSMENT RESULTS:
- Recommended Platform: {results_data['recommendation']}
- Agency Contact: {agency_info['contact_name']} ({agency_info['contact_email']})
- Department: {agency_info['department']}
- Assessment Date: {results_data['date']}

ASSESSMENT SCORES:
{results_data['scores_text']}

ANALYSIS SUMMARY:
{results_data['explanations_text']}

ASSESSMENT RESPONSES:
{results_data['answers_text']}

Please review and follow up with the agency as needed.

Best regards,
EOTSS Hosting Recommendation System
            """,
            html=f"""
<html>
<body>
<h2>EOTSS Hosting Assessment Notification</h2>
<p><strong>Agency:</strong> {agency_info['agency_name']}</p>
<p><strong>Contact:</strong> {agency_info['contact_name']} ({agency_info['contact_email']})</p>
<p><strong>Department:</strong> {agency_info['department']}</p>
<p><strong>Assessment Date:</strong> {results_data['date']}</p>

<h3>Recommendation: {results_data['recommendation']}</h3>

<h3>Assessment Scores:</h3>
{results_data['scores_html']}

<h3>Analysis Summary:</h3>
{results_data['explanations_html']}

<h3>Assessment Responses:</h3>
{results_data['answers_html']}

<p><em>Please review and follow up with the agency as needed.</em></p>
</body>
</html>
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_agency_confirmation(agency_email, results_data):
    """
    Send confirmation email to the agency.
    """
    try:
        msg = Message(
            subject=f"EOTSS Hosting Assessment Confirmation - {results_data['date']}",
            recipients=[agency_email],
            body=f"""
Dear {results_data['contact_name']},

Thank you for completing the EOTSS Hosting Assessment. Your results have been submitted to EOTSS for review.

ASSESSMENT RESULTS:
- Recommended Platform: {results_data['recommendation']}
- Assessment Date: {results_data['date']}

EOTSS will review your assessment and contact you within 2-3 business days with next steps.

If you have any questions, please contact EOTSS directly.

Best regards,
EOTSS Hosting Recommendation System
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending confirmation email: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route for the web app. Handles both GET (show form) and POST (process form) requests.
    Returns:
        str: Rendered HTML for the form or results page.
    """
    if request.method == 'POST':
        answers = {q['key']: request.form.get(q['key'], '') for q in QUESTIONS + CLOUD_READINESS_QUESTIONS}
        # Validate all fields
        missing = [q['prompt'] for q in QUESTIONS + CLOUD_READINESS_QUESTIONS if not answers[q['key']]]
        if missing:
            return render_template('form.html', questions=QUESTIONS, cloud_questions=CLOUD_READINESS_QUESTIONS, error=f"Please answer: {', '.join(missing)}", answers=answers)
        recommendation, scores, explanations = score_answers(answers)
        return render_template('result.html', recommendation=recommendation, scores=scores, explanations=explanations, answers=answers, questions=QUESTIONS, cloud_questions=CLOUD_READINESS_QUESTIONS)
    return render_template('form.html', questions=QUESTIONS, cloud_questions=CLOUD_READINESS_QUESTIONS, error=None, answers={})

@app.route('/submit_to_eotss', methods=['POST'])
def submit_to_eotss():
    """
    Handle email submission to EOTSS.
    """
    # Get form data
    agency_info = {
        'agency_name': request.form.get('agency_name', ''),
        'contact_name': request.form.get('contact_name', ''),
        'contact_email': request.form.get('contact_email', ''),
        'department': request.form.get('department', '')
    }
    
    # Get the assessment results from the form
    recommendation = request.form.get('recommendation', '')
    scores = request.form.get('scores', '')
    explanations = request.form.get('explanations', '')
    answers = request.form.get('answers', '')
    
    # Validate required fields
    if not all([agency_info['agency_name'], agency_info['contact_name'], agency_info['contact_email'], agency_info['department']]):
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('index'))
    
    # Prepare results data
    from datetime import datetime
    results_data = {
        'recommendation': recommendation,
        'scores_text': scores,
        'explanations_text': explanations,
        'answers_text': answers,
        'scores_html': scores.replace('\n', '<br>'),
        'explanations_html': explanations.replace('\n', '<br>'),
        'answers_html': answers.replace('\n', '<br>'),
        'date': datetime.now().strftime('%B %d, %Y'),
        'contact_name': agency_info['contact_name']
    }
    
    # Send emails
    eotss_sent = send_eotss_notification(agency_info, results_data)
    confirmation_sent = send_agency_confirmation(agency_info['contact_email'], results_data)
    
    if eotss_sent and confirmation_sent:
        flash('Assessment submitted successfully! EOTSS has been notified and you will receive a confirmation email shortly.', 'success')
    elif eotss_sent:
        flash('Assessment submitted to EOTSS, but there was an issue sending your confirmation email. Please contact EOTSS directly.', 'warning')
    else:
        flash('There was an issue submitting your assessment. Please try again or contact EOTSS directly.', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 