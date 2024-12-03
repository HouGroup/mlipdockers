import json
from flask import Flask, request, jsonify
from pymatgen.core.structure import Structure
from mace.calculators import mace_mp

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict_energy():
    try:
        atoms = Structure.from_dict(request.json['structure']).to_ase_atoms()
        calc = mace_mp(model=request.json['model'], dispersion=bool(request.json['dispersion']), default_dtype="float64", device=request.json['device'])
        atoms.calc = calc
        # 返回预测的能量
        return jsonify({"energy": atoms.get_potential_energy()})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # 启动 Flask 应用
