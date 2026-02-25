from flask import Flask, render_template, jsonify, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, 
            template_folder='.', 
            static_folder='.',
            static_url_path='')

# Configuration for Video Uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- 1. Routing ---

@app.route('/')
def index():
    """메인 프론트엔드 페이지를 서빙합니다."""
    return render_template('frontend_vedioAI.html')

@app.route('/api/analytics')
def get_analytics():
    """실시간 분석 데이터를 반환합니다."""
    return jsonify({
        "views": 125840,
        "engagement": 89,
        "seo_score": 92,
        "emotion_peak": "00:43"
    })

# Mock AI Engine for Phase 2
def mock_ai_generate_seo(title, country, tone):
    """Simulates LLM-based SEO keyword generation"""
    base_keywords = {
        'United States': ['AI Marketing Automation', 'Next Gen AI Trends', 'Real-Time Video Analytics', 'Global SaaS Marketing', 'AI for Business Growth'],
        'Korea': ['AI 마케팅 자동화', '차세대 AI 트렌드', '실시간 비디오 분석', '글로벌 SaaS 마케팅', '비즈니스 성장을 위한 AI'],
        'Japan': ['AIマーケティング自動化', '次世代AIトレンド', 'リアルタイムビデオ分析', 'グローバルSaaSマーケティング', 'ビジネス成長のためのAI'],
        'Germany': ['AI-Marketing-Automatisierung', 'KI-Trends der nächsten Generation', 'Echtzeit-Videoanalyse', 'Globales SaaS-Marketing', 'KI für Geschäftswachstum']
    }
    
    import random
    keywords = base_keywords.get(country, base_keywords['United States'])
    return [
        {"text": kw, "val": random.randint(70, 99), "confidence": "high" if i < 3 else "mid"}
        for i, kw in enumerate(keywords)
    ]

@app.route('/api/ai/generate-seo', methods=['POST'])
def ai_generate_seo():
    data = request.json
    title = data.get('title', '')
    country = data.get('country', 'United States')
    tone = data.get('tone', 'Viral')
    
    new_keywords = mock_ai_generate_seo(title, country, tone)
    return jsonify({
        "status": "success",
        "keywords": new_keywords,
        "analytics": {
            "views": "135,210",
            "engagement": 92,
            "seoScore": 95,
            "emotionPeak": "00:52"
        }
    })

@app.route('/api/ai/analyze-video', methods=['POST'])
def ai_analyze_video():
    return jsonify({
        "status": "analyzing",
        "progress": 100,
        "result": "Analysis Complete"
    })

@app.route('/api/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Ensure directory exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({
            "status": "success",
            "message": f"File {filename} uploaded successfully",
            "filename": filename
        })
    
    return jsonify({"status": "error", "message": "Invalid file type"}), 400

@app.route('/api/keywords')
def get_keywords():
    country = request.args.get('country', 'United States')
    keywords = mock_ai_generate_seo("Initial Scan", country, "Professional")
    return jsonify({"keywords": keywords})

if __name__ == '__main__':
    print("--- [vedioAI] AI Video SEO Agent Backend Starting ---")
    print("URL: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
