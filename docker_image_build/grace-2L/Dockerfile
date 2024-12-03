FROM python:3.11

# 设置工作目录
WORKDIR /app

# 更新pip并安装必要的依赖
COPY grace-tensorpotential-master /app/grace-tensorpotential-master
RUN pip install /app/grace-tensorpotential-master
RUN pip install pymatgen flask
COPY server.py /server.py
EXPOSE 5000

# 默认运行 bash
CMD ["python", "/server.py"]
