# SkillMapper

A tool to analyze the alignment of your resume skills with job description requirements.

## Overview

SkillMapper is a web application that helps job seekers quickly assess how well their skills, extracted from their uploaded resume, match the requirements outlined in a job description. By providing both a job description and your resume (in PDF or TXT format), the tool identifies matching keywords and provides an alignment score, along with suggestions for key skills to highlight.

## Features

* **Job Description Input:** Allows users to paste the text of a job description.
* **Resume Upload:** Supports uploading resumes in PDF (.pdf) and plain text (.txt) formats.
* **Manual Skill Input (Fallback):** Provides an option to manually enter skills if resume parsing is problematic.
* **Skill Analysis:** Extracts keywords from both the job description and the resume.
* **Skill Alignment Score:** Calculates and displays a percentage indicating the overlap in skills.
* **Matched Skills:** Lists the specific skills found in both the job description and the resume.
* **Top Keyword Suggestions:** Identifies and suggests key skills from the job description that might be important to emphasize.
* **Clear Explanation:** Includes a "How This Tool Works" section to guide users.
* **Single-Page Application:** Offers a smooth and iterative user experience.
* **Coming Soon:** [Mention any planned future features, e.g., Visualization of skill overlap (word cloud, Venn diagram)].

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/aarif22827/SkillMapper.git](https://github.com/aarif22827/SkillMapper.git)
    cd SkillMapper
    ```

2.  **Set up a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate   # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Note: You'll need to populate `requirements.txt` with `Flask` and `PyPDF2`)

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```

5.  **Open in your browser:** Navigate to `http://127.0.0.1:5000` in your web browser.

## How to Use

1.  Paste the job description into the provided text area.
2.  Upload your resume using the file input (PDF or TXT).
3.  Alternatively, check the box to manually enter your skills.
4.  Click the "Analyze" button.
5.  View the skill alignment score, matched skills, and top keyword suggestions in the results section.
6.  Use the "Restart Analysis" or "Analyze with Different Data" buttons to try again with different inputs.
7.  Click "How This Tool Works" for a detailed explanation of the application.

## License

This project is licensed under the [MIT License](LICENSE) - see the `LICENSE` file for details.

## Contributing

[Optional: If you plan to accept contributions, add guidelines here.]

## Author

Asad Arif - [https://github.com/aarif22827](https://github.com/aarif22827)

## Acknowledgements

[Optional: If you used any external resources or libraries you want to acknowledge, add them here.]
