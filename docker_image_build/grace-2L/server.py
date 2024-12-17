import json
from flask import Flask, request, jsonify
from pymatgen.core.structure import Structure
from tensorpotential.calculator import grace_fm
import time

app = Flask(__name__)
start_time = time.time()
@app.route("/predict", methods=["POST"])
def predict_energy():
    if "calc" not in globals():
        global calc
        print("Loading grace-2l model...")
        calc = grace_fm('MP_GRACE_2L_r6_11Nov2024')
        print(f"grace-2l model loaded in {time.time() - start_time:.2f} seconds.")
    try:
        atoms = Structure.from_dict(request.json['structure']).to_ase_atoms()
        atoms.calc = calc
        # 返回预测的能量
        return jsonify({"energy": atoms.get_potential_energy()})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=False)  # 启动 Flask 应用
