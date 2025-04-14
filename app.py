from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader
import re
from collections import Counter


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'job-description' not in request.form:
        return jsonify({'error': 'Missing job description'}), 400

    job_description_text = request.form['job-description']
    resume_file = request.files.get('resume-upload')
    manual_skills_text = request.form.get('manual-skills')

    resume_text = None
    if resume_file and resume_file.filename != '':
        resume_text = extract_text_from_resume(resume_file)
        if not resume_text:
            return jsonify({
                'error': 'Could not extract text from the uploaded resume'
            }), 500
    elif manual_skills_text:
        resume_text = manual_skills_text
    else:
        return jsonify({
            'error': 'No resume file uploaded and no manual skills entered'
        }), 400

    job_keywords, job_keyword_counts = extract_keywords(job_description_text)
    resume_keywords, _ = extract_keywords(resume_text)

    matched_skills = set(job_keywords) & set(resume_keywords)
    alignment_score = (
        (
            (len(matched_skills) / len(set(job_keywords)) * 100)
            if job_keywords
            else 0
        )
    )

    top_job_keywords = [item[0] for item in job_keyword_counts.most_common(5)]

    return jsonify({
        'matched_skills': list(matched_skills),
        'alignment_score': f"{alignment_score:.2f}%",
        'job_keywords': list(set(job_keywords)),
        'resume_keywords': list(set(resume_keywords)),
        'top_job_keywords': top_job_keywords
    })


def extract_text_from_resume(resume_file):
    file_extension = resume_file.filename.rsplit('.', 1)[1].lower()
    text = ""
    try:
        if file_extension == 'pdf':
            pdf_reader = PdfReader(resume_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif file_extension == 'txt':
            text = resume_file.stream.read().decode('utf-8')
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
    return text


def extract_keywords(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()

    # Common English stop words
    stop_words = {
        'the', 'a', 'is', 'are', 'in', 'on', 'at', 'for', 'to', 'of', 'and',
        'with', 'as', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my',
        'your', 'his', 'her', 'its', 'our', 'their', 'me', 'him', 'her', 'us',
        'them', 'this', 'that', 'these', 'those', 'am', 'was', 'were', 'being',
        'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'should', 'can', 'could', 'may', 'might', 'must', 'be', 'by', 'from',
        'up', 'down', 'out', 'into', 'through', 'over', 'under', 'again',
        'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
        'any', 'both', 'each', 'few', 'many', 'some', 'most', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
        've', 'd', 'll', 'm', 're', 'y', 'if', 'or', 'because', 'until',
        'while', 'about', 'against', 'between', 'during', 'before', 'after',
        'above', 'below', 'further', 'more', 'other', 'such', 'just', 'don',
        'now', 'theirs', 'ours', 'yours', 'hers', 'his', 'itself', 'ourselves',
        'yourselves', 'themselves', 'what', 'which', 'who', 'whom', 'having',
        'an', 'but', 'off', 'able', 'across', 'afterwards', 'almost', 'alone',
        'along', 'already', 'also', 'although', 'always', 'among', 'amongst',
        'another', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere',
        'around', 'became', 'become', 'becomes', 'becoming', 'behind',
        'beside', 'besides', 'beyond', 'brief', 'cant', 'certain', 'certainly',
        'dare', 'dared', 'daringly', 'directly', 'done', 'downwards',
        'eagerly', 'early', 'either', 'else', 'elsewhere', 'enough',
        'entirely', 'especially', 'even', 'ever', 'every', 'everybody',
        'everyone', 'everything', 'everywhere', 'exactly', 'example', 'except',
        'fairly', 'far', 'farther', 'finally', 'first', 'followed',
        'following', 'follows', 'forth', 'forward', 'furthermore', 'generally',
        'getting', 'given', 'gladly', 'going', 'gone', 'got', 'gotten',
        'greatly', 'hardly', 'hence', 'here', 'hereafter', 'hereby', 'herein',
        'hereupon', 'hitherto', 'however', 'hundred', 'ie', 'inasmuch',
        'indeed', 'inside', 'instead', 'inward', 'keenly', 'kept', 'kindly',
        'know', 'known', 'largely', 'last', 'lately', 'later', 'least', 'less',
        'lest', 'likely', 'little', 'livelong', 'look', 'looking', 'looks',
        'loudly', 'made', 'mainly', 'make', 'making', 'man', 'maybe',
        'meanwhile', 'merely', 'moreover', 'mostly', 'much', 'myself',
        'nearly', 'need', 'needed', 'needing', 'needs', 'neither', 'never',
        'nevertheless', 'new', 'next', 'nicely', 'nobody', 'none', 'noone',
        'normally', 'nothing', 'nowhere', 'obviously', 'often', 'oh', 'one',
        'ones', 'onto', 'openly', 'opposite', 'otherwise', 'ought', 'outward',
        'overall', 'particularly', 'partly', 'perhaps', 'placed', 'plainly',
        'please', 'possibly', 'presumably', 'presently', 'previously',
        'primarily', 'promptly', 'proudly', 'provided', 'publicly', 'quickly',
        'quietly', 'quite', 'rather', 'readily', 'really', 'recently', 'red',
        'related', 'relatively', 'respectively', 'rightly', 'round', 'said',
        'saw', 'say', 'saying', 'says', 'secondly', 'see', 'seeing', 'seem',
        'seemed', 'seeming', 'seems', 'seen', 'seldom', 'seldomly', 'self',
        'selves', 'sensibly', 'sent', 'seriously', 'several', 'severely',
        'shall', 'shortly', 'show', 'showed', 'shown', 'shows', 'namely',
        'significantly', 'simply', 'since', 'sincerely', 'slightly', 'slowly',
        'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes',
        'somewhat', 'somewhere', 'soon', 'specially', 'still', 'strongly',
        'subtly', 'sure', 'surely', 'taken', 'taking', 'talk', 'talking',
        'talks', 'tell', 'telling', 'tells', 'thank', 'thanking', 'thanks',
        'thence', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon',
        'thickly', 'thinly', 'thirdly', 'thorough', 'thoroughly', 'though',
        'thought', 'thoughtfully', 'thoughts', 'throughout', 'thus', 'tidily',
        'till', 'timely', 'together', 'tonight', 'toward', 'towards', 'truly',
        'try', 'trying', 'tries', 'twice', 'two', 'typically', 'usually',
        'underneath', 'undoing', 'unfortunately', 'unless', 'unlikely', 'unto',
        'upward', 'use', 'used', 'using', 'various', 'via', 'viciously',
        'visibly', 'viz', 'voluntarily', 'want', 'wanted', 'wanting', 'wants',
        'way', 'ways', 'well', 'went', 'whatever', 'whence', 'whenever',
        'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever',
        'whether', 'while', 'whither', 'whoever', 'whole', 'whomever', 'whose',
        'widely', 'willingly', 'wish', 'within', 'without', 'wonderfully',
        'wont', 'words', 'work', 'worked', 'working', 'works', 'world',
        'would', 'wrongly', 'wrote', 'written', 'wrong', 'ye', 'yes', 'yet',
        'yourself', 'yourselves', 'zillion', 'one', 'two', 'three', 'four',
        'five', 'six', 'seven', 'eight', 'nine', 'ten'
    }

    # Extract keywords (words not in stop_words and longer than 2 characters)
    keywords = [
        word for word in words
        if word not in stop_words and len(word) > 2
    ]

    keyword_counts = Counter(keywords)
    return keywords, keyword_counts


if __name__ == '__main__':
    app.run(debug=True)
