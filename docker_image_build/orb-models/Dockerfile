FROM python:3.12

# 设置工作目录
WORKDIR /app

# 更新pip并安装必要的依赖
RUN pip install pymatgen orb-models flask gunicorn
RUN pip install "pynanoflann@git+https://github.com/dwastberg/pynanoflann#egg=af434039ae14bedcbb838a7808924d6689274168"
COPY server.py /app/server.py
EXPOSE 5000

# 默认运行 bash
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "--chdir", "/app", "--worker-class", "sync", "--timeout", "300", "--preload", "--log-level", "debug", "server:app"]

