from flask import Flask, render_template, request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True) 