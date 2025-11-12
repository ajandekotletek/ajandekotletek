from flask import Flask, render_template_string, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'valami_osszefoglalo_secret')

PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', '')

CREDIT_PACKAGES = {
    '1': {'credits': 1, 'price': 500},
    '10': {'credits': 10, 'price': 4000},
    '20': {'credits': 20, 'price': 7500},
}

def init_user():
    if 'credits' not in session:
        session['credits'] = 2

@app.route('/')
def index():
    init_user()
    return render_template_string("""
<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<title>Ajándékötletek</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
<script src="https://www.paypal.com/sdk/js?client-id={{ paypal_client_id }}&currency=HUF"></script>
<style>
    body {
        font-family: 'Poppins', sans-serif;
        background: #fff5f0;
        color: #333;
        text-align: center;
        padding: 30px;
    }
    h2 { color: #d6336c; }
    .credits { font-size: 1.2em; margin-bottom: 20px; font-weight: 600; }
    .paypal-card {
        display: inline-block;
        background: #fff;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        width: 220px;
    }
    .paypal-card h3 { margin-bottom: 10px; color: #555; }
</style>
</head>
<body>
<h2>Ajándékötletek</h2>
<p class="credits">Jelenlegi kreditek: {{credits}}</p>

<div class="paypal-card">
    <h3>1 Kredit — 500 Ft</h3>
    <div id="paypal-buttons-1"></div>
</div>
<div class="paypal-card">
    <h3>10 Kredit — 4000 Ft</h3>
    <div id="paypal-buttons-10"></div>
</div>
<div class="paypal-card">
    <h3>20 Kredit — 7500 Ft</h3>
    <div id="paypal-buttons-20"></div>
</div>

<script>
const packages = {'1':500, '10':4000, '20':7500};

for (const pack_id in packages){
  paypal.Buttons({
    createOrder: function(data, actions){
      return actions.order.create({
        purchase_units:[{amount:{value: packages[pack_id]}}]
      });
    },
    onApprove: function(data, actions){
      return actions.order.capture().then(function(details){
        fetch('/add_credits', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({pack_id: pack_id})
        }).then(res=>res.json()).then(resp=>{
          alert('Sikeres fizetés! Új kredit egyenleg: ' + resp.credits);
          location.reload();
        });
      });
    }
  }).render('#paypal-buttons-' + pack_id);
}
</script>
</body>
</html>
""", credits=session.get('credits', 0), paypal_client_id=PAYPAL_CLIENT_ID)

@app.route('/add_credits', methods=['POST'])
def add_credits():
    data = request.get_json() or {}
    pack_id = data.get('pack_id')
    if pack_id not in CREDIT_PACKAGES:
        return jsonify({'error':'Érvénytelen csomag'}), 400
    credits_to_add = CREDIT_PACKAGES[pack_id]['credits']
    session['credits'] = session.get('credits', 0) + credits_to_add
    return jsonify({'credits': session['credits']})

# Render-en production-ready indítás
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
