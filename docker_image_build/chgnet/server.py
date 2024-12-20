from flask import Flask, request, jsonify
from pymatgen.core.structure import Structure
from chgnet.model.model import CHGNet
from chgnet.model import StructOptimizer
from ase.filters import FrechetCellFilter
from ase.constraints import FixAtoms

app = Flask(__name__)
@app.route("/predict", methods=["POST"])
def mlip_calculate():
    try:
        if "chgnet" not in globals():
            global chgnet
            chgnet = CHGNet.load(use_device = request.json['device'])
        
        if request.json['job'] == 'predict_energy':
            structure = Structure.from_dict(request.json['structure'])
            # 返回预测的能量
            return jsonify({"energy": float(chgnet.predict_structure(structure)['e'])})
        
        elif request.json['job'] == 'optimize':
            atoms = Structure.from_dict(request.json['structure']).to_ase_atoms()
            ft = FrechetCellFilter(atoms, request.json['opt_info']['fix_cell_booleans'])
            relaxer = StructOptimizer()
            result = relaxer.relax(atoms = atoms,
                                   fmax = request.json['opt_info']['fmax'],
                                   steps = request.json['opt_info']['steps'],
                                   relax_cell = True,
                                   ase_filter = ft,
                                   )["final_structure"]
            return jsonify({"structure":result.to_json(), "energy":float(chgnet.predict_structure(result)['e'])})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded = False)  # 启动 Flask 应用
