from flask import Flask, request, jsonify
from pymatgen.core.structure import Structure
from chgnet.model.model import CHGNet
import time


app = Flask(__name__)
start_time = time.time()
@app.route("/predict", methods=["POST"])
def predict_energy():
    if "chgnet" not in globals():
        global chgnet
        print("Loading CHGNet model...")
        chgnet = CHGNet.load(use_device = request.json['device'])
        print(f"CHGNet model loaded in {time.time() - start_time:.2f} seconds.")

    try:
        structure = Structure.from_dict(request.json['structure'])
        # 返回预测的能量
        return jsonify({"energy": float(chgnet.predict_structure(structure)['e'])})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded = False)  # 启动 Flask 应用
