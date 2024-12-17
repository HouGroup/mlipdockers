import json
from flask import Flask, request, jsonify
from pymatgen.core.structure import Structure
from sevenn.sevennet_calculator import SevenNetCalculator

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict_energy():
    if "calc" not in globals():
        global calc
        calc = SevenNetCalculator(request.json['version'], device=request.json['device'])
    try:
        atoms = Structure.from_dict(request.json['structure']).to_ase_atoms()
        atoms.set_calculator(calc)
        # 返回预测的能量
        return jsonify({"energy": atoms.get_potential_energy()})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded = False)  # 启动 Flask 应用
