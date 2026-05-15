
"""
Smart News Summarizer Agent - Flask REST API
REST API interface for the news summarizer agent
"""

from flask import Flask, request, jsonify, render_template_string
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

run_news_summarizer_agent = None
generate_html_report = None

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>Smart News Summarizer Agent</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            background: linear-gradient(135deg, #f3e5f5 0%, #ede7f6 50%, #e1bee7 100%); 
            min-height: 100vh; 
            padding: 20px; 
        }
        .container { max-width: 1300px; margin: 0 auto; }
        header { 
            background: rgba(255,255,255,0.98); 
            backdrop-filter: blur(10px); 
            border-radius: 16px; 
            padding: 40px; 
            margin-bottom: 30px; 
            box-shadow: 0 4px 15px rgba(156, 39, 176, 0.08); 
        }
        h1 { 
            font-size: 2.5rem; 
            color: #7b1fa2; 
            margin-bottom: 8px; 
            background: linear-gradient(135deg, #ba68c8 0%, #7b1fa2 100%); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
        }
        .subtitle { color: #888; font-size: 1.1rem; }
        .main-card { 
            background: white; 
            border-radius: 16px; 
            padding: 30px; 
            box-shadow: 0 4px 12px rgba(156, 39, 176, 0.1); 
            margin-bottom: 24px; 
        }
        .controls { 
            display: grid; 
            grid-template-columns: 1fr 200px auto; 
            gap: 16px; 
            align-items: flex-end; 
        }
        label { 
            display: block; 
            font-weight: 600; 
            color: #333; 
            margin-bottom: 8px; 
            font-size: 0.95rem; 
        }
        input, select { 
            width: 100%; 
            padding: 12px 16px; 
            border: 2px solid #e0e0e0; 
            border-radius: 8px; 
            font-size: 1rem; 
            transition: all 0.3s; 
            font-family: inherit; 
        }
        input:focus, select:focus { 
            outline: none; 
            border-color: #ba68c8; 
            box-shadow: 0 0 0 3px rgba(186, 104, 200, 0.1); 
        }
        .actions { display: flex; gap: 12px; align-items: center; }
        .btn { 
            padding: 12px 24px; 
            border: none; 
            border-radius: 8px; 
            font-weight: 600; 
            cursor: pointer; 
            font-size: 0.95rem; 
            transition: all 0.3s; 
        }
        .btn-primary { 
            background: linear-gradient(135deg, #ba68c8 0%, #7b1fa2 100%); 
            color: white; 
            box-shadow: 0 4px 15px rgba(156, 39, 176, 0.3); 
        }
        .btn-primary:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(156, 39, 176, 0.4); }
        .btn-secondary { 
            background: #f5f5f5; 
            color: #333; 
            border: 2px solid #e0e0e0; 
        }
        .btn-secondary:hover:not(:disabled) { background: #eeeeee; }
        .btn-success { background: linear-gradient(135deg, #81c784 0%, #4caf50 100%); color: white; }
        .btn-success:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(76, 175, 80, 0.3); }
        .btn-info { background: linear-gradient(135deg, #64b5f6 0%, #2196f3 100%); color: white; }
        .btn-info:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(33, 150, 243, 0.3); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .report-panel { 
            background: white; 
            border-radius: 16px; 
            padding: 24px; 
            box-shadow: 0 4px 16px rgba(0,0,0,0.08); 
            min-height: 400px; 
            max-height: 600px; 
            overflow-y: auto; 
            margin-bottom: 30px;
        }
        .bottom-buttons {
            display: flex;
            gap: 12px;
            justify-content: center;
            padding: 20px 0;
        }
        .bottom-buttons .btn {
            width: 200px;
        }
        .status-msg { 
            padding: 16px; 
            border-radius: 8px; 
            margin-bottom: 16px; 
            display: flex; 
            align-items: center; 
            gap: 12px; 
        }
        .status-msg.success { background: #c8e6c9; color: #1b5e20; border-left: 4px solid #4caf50; }
        .status-msg.error { background: #ffccbc; color: #bf360c; border-left: 4px solid #ff6e40; }
        .spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid currentColor; border-top-color: transparent; border-radius: 50%; animation: spin 0.6s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .report-content p { margin-bottom: 12px; line-height: 1.6; color: #2d3748; }
        @media (max-width: 1024px) { .controls { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Smart News Summarizer Agent</h1>
            <p class="subtitle">Automatically find recent news and create professional summaries</p>
        </header>
        
        <div class="main-card">
            <div class="controls">
                <div style="flex-grow: 1;">
                    <label for="topic">Search Topic</label>
                    <input id="topic" type="text" placeholder="e.g., Climate change, AI development, Tech news...">
                </div>
                <div class="actions" style="margin-top: 24px;">
                    <button class="btn btn-primary" id="searchBtn" onclick="window.doSearch()">Search & Summarize</button>
                    <button class="btn btn-secondary" id="clearBtn" onclick="window.doClear()">Clear</button>
                </div>
            </div>
        </div>

        <div class="report-panel">
            <div id="statusArea"></div>
            <div id="errorArea"></div>
            <div id="reportDisplay">
                <p style="color:#a0aec0; text-align:center; padding:40px 20px;">Enter a topic and click "Search & Summarize" to get started</p>
            </div>
        </div>

        <div class="bottom-buttons">
            <button class="btn btn-success" id="exportBtn" onclick="window.doExport()">Download as HTML</button>
            <button class="btn btn-info" id="printBtn" onclick="window.doPrint()">Print Report</button>
        </div>
    </div>

    <script>
        let currentReport = '';
        let currentStats = {};

        window.doSearch = async function() {
            const topic = document.getElementById('topic').value.trim();
            if(!topic) {
                window.showStatus('Please enter a topic', true);
                return;
            }
            
            window.showStatus('Searching for news...');
            document.getElementById('searchBtn').disabled = true;
            document.getElementById('clearBtn').disabled = true;
            document.getElementById('exportBtn').disabled = true;
            document.getElementById('printBtn').disabled = true;
            
            try {
                const response = await fetch('/api/summarize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic: topic, style: 'corporate' })
                });
                
                if(!response.ok) throw new Error('API error: ' + response.status);
                
                const data = await response.json();
                if(data.success) {
                    currentReport = data.report || '';
                    currentStats = data.stats || {};
                    
                    const html = data.report_html || ('<div class="report-content">' + 
                        (data.report || '').split('\\n').map(l => '<p>' + (l || '').replace(/</g, '&lt;') + '</p>').join('') + 
                        '</div>');
                    
                    document.getElementById('reportDisplay').innerHTML = html;
                    window.showStatus('Report generated successfully!');
                    
                    document.getElementById('exportBtn').disabled = false;
                    document.getElementById('printBtn').disabled = false;
                } else {
                    window.showStatus(data.error || 'Error generating report', true);
                }
            } catch(e) {
                window.showStatus('Error: ' + e.message, true);
            } finally {
                document.getElementById('searchBtn').disabled = false;
                document.getElementById('clearBtn').disabled = false;
            }
        };

        window.doClear = function() {
            document.getElementById('topic').value = '';
            document.getElementById('reportDisplay').innerHTML = '<p style="color:#a0aec0; text-align:center; padding:40px 20px;">Enter a topic and click "Search & Summarize" to get started</p>';
            document.getElementById('statusArea').innerHTML = '';
            document.getElementById('errorArea').innerHTML = '';
            document.getElementById('exportBtn').disabled = true;
            document.getElementById('printBtn').disabled = true;
            currentReport = '';
            currentStats = {};
        };

        window.doExport = function() {
            if(!currentReport) {
                alert('No report to export');
                return;
            }
            const html = '<html><head><meta charset="utf-8"><title>News Report</title><style>body{font-family:system-ui,sans-serif;padding:20px;line-height:1.6;}</style></head><body>' + currentReport + '</body></html>';
            const blob = new Blob([html], {type: 'text/html'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'news_report_' + new Date().getTime() + '.html';
            a.click();
            URL.revokeObjectURL(url);
        };

        window.doPrint = function() {
            if(!currentReport) {
                alert('No report to print');
                return;
            }
            const w = window.open();
            w.document.write('<html><head><meta charset="utf-8"><style>body{font-family:system-ui,sans-serif;padding:20px;line-height:1.6;}</style></head><body>' + currentReport + '</body></html>');
            w.document.close();
            setTimeout(() => w.print(), 500);
        };

        window.showStatus = function(msg, isError) {
            const html = '<div class="status-msg ' + (isError ? 'error' : 'success') + '">' + msg + '</div>';
            document.getElementById('statusArea').innerHTML = html;
        };
    </script>
</body>
</html>"""


@app.route('/', methods=['GET'])
def index():
    """Render the web UI"""
    response = app.make_response(render_template_string(HTML_TEMPLATE))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/api/summarize', methods=['POST'])
def summarize():
    """API endpoint to summarize news"""
    try:
        data = request.get_json() or {}
        topic = (data.get('topic') or '').strip()
        style = data.get('style', 'corporate')

        if not topic:
            return jsonify({'success': False, 'error': 'Topic is required'}), 400

        global run_news_summarizer_agent, generate_html_report
        if run_news_summarizer_agent is None:
            try:
                from app.app import run_news_summarizer_agent as _r
                run_news_summarizer_agent = _r
            except Exception:
                pass

        if generate_html_report is None:
            try:
                from modules.report_generator import generate_html_report as _g
                generate_html_report = _g
            except Exception:
                pass

        if run_news_summarizer_agent is None:
            report = (
                f"Demo Report for: {topic}\n\n"
                "Total Articles Found: 3\n"
                "Successfully Processed: 3\n"
                "Failed to Process: 0\n"
                "Success Rate: 100.0\n\n"
                "Article 1: Example News One - Brief summary of the article.\n"
                "Article 2: Example News Two - Brief summary of the article.\n"
                "Article 3: Example News Three - Brief summary of the article.\n"
            )
        else:
            report = run_news_summarizer_agent(topic, save_to_file=True)

        report_html = None
        if generate_html_report is not None:
            try:
                report_html = generate_html_report(report, style=style)
            except Exception:
                pass

        lines = report.split('\n') if isinstance(report, str) else []
        stats = {'total': 0, 'processed': 0, 'failed': 0, 'success_rate': 0}

        for line in lines:
            try:
                if 'Total Articles Found:' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        num_str = ''.join(c for c in parts[1] if c.isdigit())
                        if num_str:
                            stats['total'] = int(num_str)
                elif 'Successfully Processed:' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        num_str = ''.join(c for c in parts[1] if c.isdigit())
                        if num_str:
                            stats['processed'] = int(num_str)
                elif 'Failed to Process:' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        num_str = ''.join(c for c in parts[1] if c.isdigit())
                        if num_str:
                            stats['failed'] = int(num_str)
                elif 'Success Rate:' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        num_str = ''.join(c for c in parts[1] if c.isdigit() or c == '.')
                        if num_str:
                            stats['success_rate'] = float(num_str)
            except (ValueError, IndexError):
                continue

        resp = {'success': True, 'report': report, 'stats': stats}
        if report_html:
            resp['report_html'] = report_html

        return jsonify(resp), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat(), 'version': '1.0'}), 200


@app.route('/api/info', methods=['GET'])
def info():
    """API information endpoint"""
    return jsonify({
        'name': 'Smart News Summarizer Agent',
        'version': '1.0',
        'description': 'Automatically find recent news and create brief summaries',
        'endpoints': {
            'GET /': 'Web UI',
            'POST /api/summarize': 'Summarize news',
            'GET /api/health': 'Health check',
            'GET /api/info': 'API information'
        }
    }), 200


if __name__ == '__main__':
    print("\n" + "="*80)
    print("[STARTING] Flask API Server")
    print("="*80)
    print("[API] Server: http://localhost:5000")
    print("[WEB] UI: http://localhost:5000")
    print("[DOCS] API Documentation: http://localhost:5000/api/info")
    print("="*80 + "\n")
    app.run(debug=False, host='0.0.0.0', port=5000)
