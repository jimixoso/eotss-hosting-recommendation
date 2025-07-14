import sys
import argparse
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# QUESTIONS: Main assessment questions for application requirements.
# Each question is a dict with a key, prompt, valid options, and a help string for user guidance.
QUESTIONS = [
    {"key": "fault_tolerance", "prompt": "Fault Tolerance (Low/Moderate/High): ", "options": ["low", "moderate", "high"], "help": "High = must always be available (e.g., 24/7 critical), Moderate = some downtime acceptable, Low = downtime is fine"},
    {"key": "latency", "prompt": "Latency Sensitivity (Low/Moderate/High): ", "options": ["low", "moderate", "high"], "help": "High = needs instant response (e.g., real-time), Moderate = some delay is ok, Low = delay is fine"},
    {"key": "data_volume", "prompt": "Data Volume (Low/Moderate/High): ", "options": ["low", "moderate", "high"], "help": "High = large datasets (TBs+), Moderate = moderate data, Low = small data"},
    {"key": "security", "prompt": "Security Needs (Low/Moderate/High): ", "options": ["low", "moderate", "high"], "help": "High = sensitive data (e.g., PII, HIPAA), Moderate = some sensitive data, Low = public or non-sensitive"},
    {"key": "migration", "prompt": "Migration Complexity (Low/Moderate/High): ", "options": ["low", "moderate", "high"], "help": "High = hard to move, many dependencies; Low = easy to move"},
    {"key": "ops_expertise", "prompt": "Operational Expertise (aws/vmware/minimal): ", "options": ["aws", "vmware", "minimal"], "help": "AWS = team knows AWS, VMware = team knows on-prem/cloud, Minimal = little expertise"},
    {"key": "budget", "prompt": "Budget Sensitivity (Low/Moderate/High): ", "options": ["low", "moderate", "high"], "help": "Low = cost is a concern, High = cost is not a concern"},
    {"key": "compliance", "prompt": "Does your application have specific compliance requirements (yes/no)? ", "options": ["yes", "no"], "help": "Yes = must meet regulations (e.g., HIPAA, CJIS)"},
    {"key": "scalability", "prompt": "Do you expect rapid growth or fluctuating workloads (yes/no)? ", "options": ["yes", "no"], "help": "Yes = user base or data may grow quickly or unpredictably"},
]

# CLOUD_READINESS_QUESTIONS: Questions to assess the application's cloud readiness.
# Used to determine if the app is 'modern' or 'legacy' for scoring purposes.
CLOUD_READINESS_QUESTIONS = [
    {"key": "containerized", "prompt": "Is the app containerized or able to be containerized (e.g., Docker)? ", "options": ["yes", "no"], "help": "Yes = can run in Docker or similar, No = needs special hardware or OS"},
    {"key": "compatible_runtime", "prompt": "Does the app run on a cloud-supported OS/runtime (e.g., modern Linux, Windows Server 2016+)? ", "options": ["yes", "no"], "help": "Yes = runs on modern Linux/Windows, No = needs legacy OS"},
    {"key": "no_hardware_deps", "prompt": "Does the app avoid relying on physical hardware or specialized networking? ", "options": ["yes", "no"], "help": "Yes = no special cards/devices, No = needs hardware access"},
]

def get_migration_complexity(answers):
    """
    Determine migration complexity based on sub-question answers.
    Returns: 'low', 'moderate', or 'high'.
    """
    score = 0
    if answers.get("custom_hardware") == "yes":
        score += 2
    if answers.get("legacy_software") == "yes":
        score += 2
    if answers.get("large_data") == "yes":
        score += 1
    if answers.get("many_integrations") == "yes":
        score += 1
    if answers.get("documentation") == "not documented":
        score += 2
    elif answers.get("documentation") == "somewhat":
        score += 1
    # Scoring: 0-1 = low, 2-3 = moderate, 4+ = high
    if score >= 4:
        return "high"
    elif score >= 2:
        return "moderate"
    else:
        return "low"


def get_valid_input(prompt, valid_options):
    """
    Prompt the user for input until a valid option is entered.
    Args:
        prompt (str): The prompt to display to the user.
        valid_options (list): List of valid string options (lowercase).
    Returns:
        str: The valid input entered by the user (lowercase).
    """
    while True:
        value = input(prompt).strip().lower()
        if value in valid_options:
            return value
        print(f"Invalid input. Please enter one of: {', '.join(valid_options)}")


def parse_args():
    """
    Parse command-line arguments for the hosting recommendation tool.
    Returns:
        argparse.Namespace: Parsed arguments object.
    """
    parser = argparse.ArgumentParser(description="EOTSS Hosting Recommendation System")
    for q in QUESTIONS:
        parser.add_argument(f'--{q["key"]}', type=str, choices=q["options"], help=q["help"])
    for q in CLOUD_READINESS_QUESTIONS:
        parser.add_argument(f'--{q["key"]}', type=str, choices=q["options"], help=q["help"])
    parser.add_argument('--gui', action='store_true', help='Launch the GUI version')
    return parser.parse_args()


def recommend_hosting():
    """
    Run the CLI version of the EOTSS Hosting Recommendation System.
    Prompts the user for answers, processes them, and displays the recommendation.
    """
    print("=== EOTSS Hosting Recommendation System ===")

    # Parse command-line arguments
    args = parse_args()
    arg_dict = vars(args)

    # Collect answers (use CLI args if provided, else prompt)
    answers = {}
    for q in QUESTIONS:
        arg_val = arg_dict.get(q["key"])
        if arg_val:
            answers[q["key"]] = arg_val
        else:
            if "help" in q:
                print(f"  (Hint: {q['help']})")
            answers[q["key"]] = get_valid_input(q["prompt"], q["options"])

    # Application Age Determination Logic
    print("\n--- Application Cloud Readiness Check ---")
    print("Answer 'yes' or 'no' to the following questions:")
    cloud_ready_score = 0
    for q in CLOUD_READINESS_QUESTIONS:
        arg_val = arg_dict.get(q["key"])
        if arg_val:
            ans = arg_val
        else:
            if "help" in q:
                print(f"  (Hint: {q['help']})")
            ans = get_valid_input(q["prompt"], q["options"])
        answers[q["key"]] = ans
        if ans == "yes":
            cloud_ready_score += 1
    app_age = "modern" if cloud_ready_score >= 2 else "legacy"
    answers["app_age"] = app_age

    # Review and edit answers before processing (only if running interactively)
    if not any(arg_dict.values()):
        while True:
            print("\nSummary of your answers:")
            for idx, q in enumerate(QUESTIONS):
                print(f"{idx+1}. {q['prompt']} {answers[q['key']]}")
            edit = get_valid_input("Would you like to change any answer? (yes/no): ", ["yes", "no"])
            if edit == "no":
                break
            qnum = int(get_valid_input("Enter the number of the question to change: ", [str(i+1) for i in range(len(QUESTIONS))]))
            q = QUESTIONS[qnum-1]
            if "help" in q:
                print(f"  (Hint: {q['help']})")
            answers[q["key"]] = get_valid_input(q["prompt"], q["options"])

    # Scoring logic
    scores = {"aws": 0, "on_prem_cloud": 0, "physical": 0}

    # Fault Tolerance
    if answers["fault_tolerance"] == "high":
        scores["aws"] += 2
    elif answers["fault_tolerance"] == "moderate":
        scores["on_prem_cloud"] += 1

    # Latency Sensitivity
    if answers["latency"] == "high":
        scores["physical"] += 2
    elif answers["latency"] == "moderate":
        scores["on_prem_cloud"] += 1

    # Data Volume
    if answers["data_volume"] == "high":
        scores["on_prem_cloud"] += 2
    elif answers["data_volume"] == "moderate":
        scores["aws"] += 1
    else:
        scores["aws"] += 2

    # Security Needs
    if answers["security"] == "high":
        scores["physical"] += 2
    elif answers["security"] == "moderate":
        scores["on_prem_cloud"] += 2
    else:
        scores["aws"] += 1

    # Application Age (using logic above)
    if answers["app_age"] == "modern":
        scores["aws"] += 2
    else:
        scores["physical"] += 2

    # Migration Complexity
    migration_complexity = get_migration_complexity(answers)
    if migration_complexity == "low":
        scores["aws"] += 2
    elif migration_complexity == "moderate":
        scores["on_prem_cloud"] += 1
    else: # high
        scores["physical"] += 2

    # Operational Expertise
    if answers["ops_expertise"] == "aws":
        scores["aws"] += 2
    elif answers["ops_expertise"] == "vmware":
        scores["on_prem_cloud"] += 2
    else:
        scores["physical"] += 1

    # Budget Sensitivity
    if answers["budget"] == "low":
        scores["aws"] += 2
    elif answers["budget"] == "moderate":
        scores["on_prem_cloud"] += 1

    # Compliance Requirements
    if answers["compliance"] == "yes":
        scores["on_prem_cloud"] += 2
        scores["aws"] += 1  # Some compliance can be met in AWS, but on-prem is often preferred
    else:
        scores["aws"] += 1

    # Scalability Needs
    if answers["scalability"] == "yes":
        scores["aws"] += 2
        scores["on_prem_cloud"] += 1
    else:
        scores["physical"] += 1

    # Final recommendation
    recommendation = max(scores, key=scores.get)

    # Explanation logic: collect top contributing factors
    explanations = []
    if recommendation == "aws":
        if answers["fault_tolerance"] == "high":
            explanations.append("High fault tolerance needs are best met by AWS.")
        if answers["budget"] == "low":
            explanations.append("Low budget sensitivity favors AWS's cost efficiency.")
        if answers["app_age"] == "modern":
            explanations.append("Modern, cloud-ready applications are ideal for AWS.")
        if migration_complexity == "low":
            explanations.append("Low migration complexity makes AWS adoption easier.")
        if answers["ops_expertise"] == "aws":
            explanations.append("Your team has AWS expertise.")
        if answers["scalability"] == "yes":
            explanations.append("AWS is well-suited for scalable workloads.")
        if answers["compliance"] == "no":
            explanations.append("No strict compliance requirements allow for public cloud hosting.")
    elif recommendation == "on_prem_cloud":
        if answers["fault_tolerance"] == "moderate":
            explanations.append("Moderate fault tolerance can be handled by on-prem cloud.")
        if answers["latency"] == "moderate":
            explanations.append("Moderate latency sensitivity is suitable for on-prem cloud.")
        if answers["data_volume"] == "high":
            explanations.append("High data volume is often better managed on-premises.")
        if answers["security"] == "moderate":
            explanations.append("Moderate security needs are met by on-prem cloud.")
        if migration_complexity == "moderate":
            explanations.append("Moderate migration complexity fits on-prem cloud.")
        if answers["ops_expertise"] == "vmware":
            explanations.append("Your team has VMware/on-prem expertise.")
        if answers["compliance"] == "yes":
            explanations.append("Compliance requirements are often easier to meet on-premises.")
        if answers["scalability"] == "yes":
            explanations.append("On-prem cloud can support some scalability needs.")
    elif recommendation == "physical":
        if answers["latency"] == "high":
            explanations.append("High latency sensitivity is best served by physical infrastructure.")
        if answers["security"] == "high":
            explanations.append("High security needs are best met by physical hosting.")
        if answers["app_age"] == "legacy":
            explanations.append("Legacy applications are often better suited to physical servers.")
        if migration_complexity == "high":
            explanations.append("High migration complexity favors staying on physical infrastructure.")
        if answers["ops_expertise"] == "minimal":
            explanations.append("Minimal cloud/on-prem expertise may require physical hosting.")
        if answers["scalability"] == "no":
            explanations.append("Physical infrastructure is suitable for stable, non-scaling workloads.")
    print("\nSystem Recommendation:", recommendation.upper())
    print("Scores:", scores)
    if explanations:
        print("\nReasoning for recommendation:")
        for reason in explanations:
            print("-", reason)

    # Personal discretion override
    override = get_valid_input("\nWould you like to override the recommendation? (yes/no): ", ["yes", "no"])
    if override == "yes":
        custom_choice = get_valid_input("Enter your preferred hosting platform (aws/on_prem_cloud/physical): ", ["aws", "on_prem_cloud", "physical"])
        final_recommendation = f"Final Recommendation Overridden to: {custom_choice.upper()} (by personal discretion)"
        print(f"\n{final_recommendation}")
    else:
        final_recommendation = f"Final Recommendation: {recommendation.upper()}"
        print(f"\n{final_recommendation}")

    # Offer to export/save results
    save = get_valid_input("\nWould you like to save your answers and the recommendation to a file? (yes/no): ", ["yes", "no"])
    if save == "yes":
        filename = input("Enter filename to save to (e.g., result.txt): ").strip()
        with open(filename, "w") as f:
            f.write("EOTSS Hosting Recommendation System\n\n")
            f.write("Summary of your answers:\n")
            for q in QUESTIONS:
                f.write(f"- {q['prompt']} {answers[q['key']]}\n")
            f.write("\nCloud Readiness Questions:\n")
            for q in CLOUD_READINESS_QUESTIONS:
                f.write(f"- {q['prompt']} {answers[q['key']]}\n")
            f.write(f"\nScores: {scores}\n")
            f.write(f"\nSystem Recommendation: {recommendation.upper()}\n")
            if explanations:
                f.write("\nReasoning for recommendation:\n")
                for reason in explanations:
                    f.write(f"- {reason}\n")
            f.write(f"\n{final_recommendation}\n")
        print(f"Results saved to {filename}")

def run_gui():
    """
    Launch the Tkinter GUI version of the EOTSS Hosting Recommendation System.
    Presents the questions in a graphical form and displays the recommendation.
    """
    root = tk.Tk()
    root.title("EOTSS Hosting Recommendation System")
    root.minsize(600, 600)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Create a canvas and a vertical scrollbar for the main frame
    canvas = tk.Canvas(root, borderwidth=0)
    vscroll = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vscroll.set)
    vscroll.grid(row=0, column=1, sticky="ns")
    canvas.grid(row=0, column=0, sticky="nsew")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Frame inside the canvas
    main_frame = ttk.Frame(canvas, padding=20)
    main_frame_id = canvas.create_window((0, 0), window=main_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    main_frame.bind("<Configure>", on_frame_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    # Group: Main Questions
    questions_labelframe = ttk.LabelFrame(main_frame, text="Main Application Questions", padding=15)
    questions_labelframe.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    questions_labelframe.columnconfigure(1, weight=1)

    entries = {}
    row = 0
    for q in QUESTIONS:
        ttk.Label(questions_labelframe, text=q["prompt"], font=("Segoe UI", 10)).grid(row=row, column=0, sticky="w", pady=2, padx=(0, 10))
        var = tk.StringVar()
        entries[q["key"]] = var
        combo = ttk.Combobox(questions_labelframe, textvariable=var, values=q["options"], state="readonly", font=("Segoe UI", 10))
        combo.grid(row=row, column=1, sticky="ew", pady=2)
        if "help" in q:
            ttk.Label(questions_labelframe, text=f"Hint: {q['help']}", foreground="gray", font=("Segoe UI", 9, "italic")).grid(row=row+1, column=0, columnspan=2, sticky="w", pady=(0, 6))
            row += 1
        row += 1

    # Group: Cloud Readiness
    cloud_labelframe = ttk.LabelFrame(main_frame, text="Cloud Readiness Questions", padding=15)
    cloud_labelframe.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    cloud_labelframe.columnconfigure(1, weight=1)
    row = 0
    for q in CLOUD_READINESS_QUESTIONS:
        ttk.Label(cloud_labelframe, text=q["prompt"], font=("Segoe UI", 10)).grid(row=row, column=0, sticky="w", pady=2, padx=(0, 10))
        var = tk.StringVar()
        entries[q["key"]] = var
        combo = ttk.Combobox(cloud_labelframe, textvariable=var, values=q["options"], state="readonly", font=("Segoe UI", 10))
        combo.grid(row=row, column=1, sticky="ew", pady=2)
        if "help" in q:
            ttk.Label(cloud_labelframe, text=f"Hint: {q['help']}", foreground="gray", font=("Segoe UI", 9, "italic")).grid(row=row+1, column=0, columnspan=2, sticky="w", pady=(0, 6))
            row += 1
        row += 1

    # Results area
    results_frame = ttk.LabelFrame(main_frame, text="Recommendation Results", padding=15)
    results_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
    results_frame.columnconfigure(0, weight=1)
    results_frame.rowconfigure(0, weight=1)
    result_box = scrolledtext.ScrolledText(results_frame, width=60, height=15, state='disabled', font=("Consolas", 10))
    result_box.grid(row=0, column=0, sticky="nsew")

    # Submit button
    submit_btn = ttk.Button(main_frame, text="Submit", command=lambda: on_submit(entries, result_box))
    submit_btn.grid(row=3, column=0, columnspan=2, pady=(10, 0))

    def on_submit(entries, result_box):
        """
        Handle the form submission in the GUI, validate input, compute the recommendation, and display results.
        Args:
            entries (dict): Mapping of question keys to Tkinter StringVar objects.
            result_box (tkinter widget): The text box to display results.
        """
        answers = {k: v.get() for k, v in entries.items()}
        # Validate all fields
        for q in QUESTIONS + CLOUD_READINESS_QUESTIONS:
            if not answers[q["key"]]:
                messagebox.showerror("Missing Input", f"Please answer: {q['prompt']}")
                return
        # Compute cloud readiness
        cloud_ready_score = sum(1 for q in CLOUD_READINESS_QUESTIONS if answers[q["key"]] == "yes")
        app_age = "modern" if cloud_ready_score >= 2 else "legacy"
        answers["app_age"] = app_age
        # Scoring logic (same as CLI)
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
        migration_complexity = get_migration_complexity(answers)
        if migration_complexity == "low":
            scores["aws"] += 2
        elif migration_complexity == "moderate": scores["on_prem_cloud"] += 1
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
            if migration_complexity == "low": explanations.append("Low migration complexity makes AWS adoption easier.")
            if answers["ops_expertise"] == "aws": explanations.append("Your team has AWS expertise.")
            if answers["scalability"] == "yes": explanations.append("AWS is well-suited for scalable workloads.")
            if answers["compliance"] == "no": explanations.append("No strict compliance requirements allow for public cloud hosting.")
        elif recommendation == "on_prem_cloud":
            if answers["fault_tolerance"] == "moderate": explanations.append("Moderate fault tolerance can be handled by on-prem cloud.")
            if answers["latency"] == "moderate": explanations.append("Moderate latency sensitivity is suitable for on-prem cloud.")
            if answers["data_volume"] == "high": explanations.append("High data volume is often better managed on-premises.")
            if answers["security"] == "moderate": explanations.append("Moderate security needs are met by on-prem cloud.")
            if migration_complexity == "moderate": explanations.append("Moderate migration complexity fits on-prem cloud.")
            if answers["ops_expertise"] == "vmware": explanations.append("Your team has VMware/on-prem expertise.")
            if answers["compliance"] == "yes": explanations.append("Compliance requirements are often easier to meet on-premises.")
            if answers["scalability"] == "yes": explanations.append("On-prem cloud can support some scalability needs.")
        elif recommendation == "physical":
            if answers["latency"] == "high": explanations.append("High latency sensitivity is best served by physical infrastructure.")
            if answers["security"] == "high": explanations.append("High security needs are best met by physical hosting.")
            if answers["app_age"] == "legacy": explanations.append("Legacy applications are often better suited to physical servers.")
            if migration_complexity == "high": explanations.append("High migration complexity favors staying on physical infrastructure.")
            if answers["ops_expertise"] == "minimal": explanations.append("Minimal cloud/on-prem expertise may require physical hosting.")
            if answers["scalability"] == "no": explanations.append("Physical infrastructure is suitable for stable, non-scaling workloads.")
        # Show results
        result_box.config(state='normal')
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, "System Recommendation: " + recommendation.upper() + "\n")
        result_box.insert(tk.END, f"Scores: {scores}\n\n")
        if explanations:
            result_box.insert(tk.END, "Reasoning for recommendation:\n")
            for reason in explanations:
                result_box.insert(tk.END, f"- {reason}\n")
        result_box.config(state='disabled')

    root.mainloop()

if __name__ == "__main__":
    args = parse_args()
    if hasattr(args, 'gui') and args.gui:
        run_gui()
    else:
        recommend_hosting()
