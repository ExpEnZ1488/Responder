from flask import Flask, request, Response, send_from_directory
import urllib.request
import urllib.error
import os

API_KEY = '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'

app = Flask(__name__)

def cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

@app.route('/', methods=['GET'])
@app.route('/RESPONDER.html', methods=['GET'])
def index():
    return send_from_directory('.', 'RESPONDER.html')

@app.route('/test', methods=['GET'])
def test():
    return 'Flask works!'

@app.route('/api', methods=['GET', 'POST', 'OPTIONS'])
def api():
    print(f'API called: {request.method}')
    if request.method in ['GET', 'OPTIONS']:
        r = Response('OK')
        return cors(r)
    
    body = request.get_data()
    print(f'Body size: {len(body)} bytes')
    
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': API_KEY,
            'anthropic-version': '2023-06-01'
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as r:
            result = r.read()
        print('API success!')
        return cors(Response(result, content_type='application/json'))
    except urllib.error.HTTPError as e:
        body = e.read()
        print(f'API error: {e.code} {body}')
        return cors(Response(body, status=e.code, content_type='application/json'))
    except Exception as e:
        print(f'Exception: {e}')
        return cors(Response(f'{{"error":"{e}"}}', status=500, content_type='application/json'))

port = int(os.environ.get('PORT', 8000))
print(f'Server: http://0.0.0.0:{port}')
print(f'Test: http://0.0.0.0:{port}/test')
print(f'App: http://0.0.0.0:{port}/RESPONDER.html')
app.run(host='0.0.0.0', port=port, debug=False)
