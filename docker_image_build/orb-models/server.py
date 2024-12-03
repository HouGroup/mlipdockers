import json
from flask import Flask, request, jsonify
from pymatgen.core.structure import Structure
import ase
from ase.build import bulk
from orb_models.forcefield import pretrained
from orb_models.forcefield.calculator import ORBCalculator
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict_energy():
    try:
        atoms = Structure.from_dict(request.json['structure']).to_ase_atoms()
        calc = ORBCalculator(pretrained.orb_v2(device = request.json['device']), device=request.json['device'])
        atoms.set_calculator(calc)
        # 返回预测的能量
        return jsonify({"energy": atoms.get_potential_energy()})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # 启动 Flask 应用
