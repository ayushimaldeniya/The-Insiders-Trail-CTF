from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Expected Evidence Tokens from Stages 1-5
CORRECT_EVIDENCE = {
    "clue1": "NIGHTHAWK",
    "clue2": "ghostwire_lk",
    "clue3": "N1GHT_DR1V3_2026",
    "clue4": "exfil.nexora-logistics.lk:8443",
    "clue5": "RevokeAccess2026"
}

CAPSTONE_FLAG = "CTF{1nc1d3nt_c0rr3l4t10n_m4st3r_2026}"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/correlate', methods=['POST'])
def correlate():
    data = request.json or request.form
    for key, expected in CORRECT_EVIDENCE.items():
        if data.get(key, '').strip() != expected:
            return jsonify({"status": "error", "message": f"Validation failed for {key}."}), 400
            
    return jsonify({"status": "success", "flag": CAPSTONE_FLAG})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)