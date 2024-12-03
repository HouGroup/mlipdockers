from flask import Flask, request, jsonify
from pymatgen.core.structure import Structure
from chgnet.model.model import CHGNet

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict_energy():
    try:
        chgnet = CHGNet.load(use_device = request.json['device'])
        structure = Structure.from_dict(request.json['structure'])
        # 返回预测的能量
        return jsonify({"energy": float(chgnet.predict_structure(structure)['e'])})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # 启动 Flask 应用
