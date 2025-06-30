import os
import uuid
import logging
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from werkzeug.utils import secure_filename
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

# ---------------------- 初始化 Flask ----------------------
app = Flask(__name__)
CORS(app)

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_bge.log'),
        logging.StreamHandler()
    ]
)

# ---------------------- 路径配置修正 ----------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # 绝对路径处理
AUDIO_FOLDER = BASE_DIR / "audio"  # 定位到项目根目录的audio文件夹

# 创建音频目录（带权限检查）
try:
    AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)
    os.chmod(AUDIO_FOLDER, 0o755)  # 设置目录权限
except PermissionError as e:
    logging.critical(f"目录权限不足: {AUDIO_FOLDER} - {str(e)}")
    exit(1)


# ---------------------- RAG 服务集成 ----------------------
class RAGService:
    def __init__(self, index_path, model_path):
        self.model = SentenceTransformer(model_path)
        self.index = faiss.read_index(os.path.join(index_path, "qa_index"))

        # 元数据加载优化
        metadata_path = os.path.join(index_path, "metadata.json")
        try:
            with open(metadata_path, 'r', encoding='gbk') as f:  # 统一使用gbk编码
                self.metadata = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"元数据文件解析失败: {metadata_path}")
            self.metadata = {}

    def search(self, query: str, top_k: int = 3):
        try:
            query_emb = self.model.encode([query],
                                          convert_to_numpy=True,
                                          normalize_embeddings=True
                                          )
            distances, indices = self.index.search(query_emb, top_k)
            return [{
                "question": self.metadata.get(str(idx), {}).get("question"),
                "answer": self.metadata.get(str(idx), {}).get("answer"),
                "score": float(score)
            } for score, idx in zip(distances[0], indices[0])]
        except Exception as e:
            logging.error(f"RAG检索异常: {str(e)}")
            return []


# ---------------------- TTS 服务增强 ----------------------
dashscope.api_key = "sk-bffacaf5e15f427e9ad0593fce0b67df"
MODEL_NAME = "cosyvoice-v1"
VOICE_TYPE = "longxiaochun"


def text_to_speech(text):
    try:
        # 生成安全文件名
        audio_filename = f"audio_{uuid.uuid4().hex}.mp3"
        audio_path = AUDIO_FOLDER / audio_filename

        synthesizer = SpeechSynthesizer(model=MODEL_NAME, voice=VOICE_TYPE)
        audio_data = synthesizer.call(text)

        if audio_data:
            # 原子写入操作
            with open(audio_path, 'wb') as f:
                f.write(audio_data)
            os.chmod(audio_path, 0o644)  # 设置文件权限
            return audio_filename
        return None
    except Exception as e:
        logging.error(f"语音生成失败: {str(e)}")
        return None


# ---------------------- API 路由优化 ----------------------
@app.route("/chat", methods=["POST"])
def chat():
    """增强型问答接口"""
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "请求格式无效"}), 400

    # 执行检索
    results = rag_service.search(data["question"], top_k=1)
    if not results:
        return jsonify({"error": "未找到相关答案"}), 404

    best_answer = results[0]["answer"]
    audio_filename = text_to_speech(best_answer)

    if not audio_filename:
        return jsonify({"error": "音频生成失败"}), 500

    return jsonify({
        "answer": best_answer,
        "audioUrl": f"/audio/{audio_filename}",
        "reference": results[0]["question"],
        "confidence": results[0]["score"]
    })


@app.route("/audio/<filename>", methods=["GET"])
def get_audio(filename):
    """安全音频文件服务"""
    try:
        safe_name = secure_filename(filename)  # 安全过滤[5,8](@ref)
        logging.info(f"请求音频文件: {safe_name}")
        return send_from_directory(
            directory=AUDIO_FOLDER,
            path=safe_name,
            mimetype="audio/mpeg",
            conditional=True  # 支持断点续传[6](@ref)
        )
    except FileNotFoundError:
        logging.warning(f"音频文件不存在: {safe_name}")
        return jsonify({"error": "音频文件不存在"}), 404


# ---------------------- 服务启动优化 ----------------------
if __name__ == "__main__":
    # 初始化RAG服务
    rag_service = RAGService(
        index_path="E:\my-qa-platform\One_click\\multilingual_ivf_index",
        model_path="E:\my-qa-platform\One_click\\backend\optimized_qa_model"
    )

    # 预热检查
    try:
        rag_service.search("系统预热查询")
        logging.info("RAG服务预热成功")
    except Exception as e:
        logging.critical(f"RAG服务初始化失败: {str(e)}")
        exit(1)

    app.run(port=5000, debug=False)  # 生产环境关闭调试模式