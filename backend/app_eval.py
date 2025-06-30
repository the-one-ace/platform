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
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# ---------------------- 路径配置修正 (建议将此类配置放在文件顶部，靠近导入) ----------------------
BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_FOLDER = BASE_DIR / "audio"

# 创建音频目录（带权限检查）
try:
    AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)
    os.chmod(AUDIO_FOLDER, 0o755)
except PermissionError as e:
    logging.critical(f"目录权限不足: {AUDIO_FOLDER} - {str(e)}")
    exit(1)


# ---------------------- RAG 服务集成 (完整的 RAGService 类定义) ----------------------
class RAGService:
    def __init__(self, index_path, model_path):
        logging.info(f"尝试加载 SentenceTransformer 模型从: {model_path}")
        self.model = SentenceTransformer(str(model_path)) # 转换为字符串路径
        logging.info(f"成功加载 SentenceTransformer 模型: {model_path}")

        index_file_path = index_path / "qa.index" # 假设索引文件名为 qa.index
        try:
            self.index = faiss.read_index(str(index_file_path))
            logging.info(f"成功加载FAISS索引: {index_file_path}")
        except Exception as e:
            logging.critical(f"FAISS索引加载失败: {index_file_path} - {str(e)}")
            exit(1)

        metadata_path = index_path / "metadata.json"
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            logging.info(f"成功加载元数据: {metadata_path}")
        except FileNotFoundError:
            logging.error(f"元数据文件未找到: {metadata_path}")
            self.metadata = {}
        except json.JSONDecodeError as e:
            logging.error(f"元数据文件解析失败: {metadata_path} - {str(e)}")
            self.metadata = {}
        except Exception as e:
            logging.error(f"加载元数据时发生未知错误: {str(e)}")
            self.metadata = {}

    # 这个 search 方法是您之前提供的完整定义的一部分
    def search(self, query: str, top_k: int = 3):
        try:
            query_emb = self.model.encode([query],
                                          convert_to_numpy=True,
                                          normalize_embeddings=True
                                          )
            distances, indices = self.index.search(query_emb, top_k)
            results = []
            for score, idx in zip(distances[0], indices[0]):
                meta_item = self.metadata.get(str(idx))
                if meta_item:
                    results.append({
                        "question": meta_item.get("question"),
                        "answer": meta_item.get("answer"),
                        "score": float(score)
                    })
                else:
                    logging.warning(f"在元数据中未找到索引为 {idx} 的条目。")
            return results
        except Exception as e:
            logging.error(f"RAG检索异常: {str(e)}")
            return []


# ---------------------- TTS 服务增强 ----------------------
dashscope.api_key = "sk-bffacaf5e15f427e9ad0593fce0b67df"
MODEL_NAME = "cosyvoice-v1"
VOICE_TYPE = "longxiaochun"

def text_to_speech(text):
    try:
        audio_filename = f"audio_{uuid.uuid4().hex}.mp3"
        audio_path = AUDIO_FOLDER / audio_filename

        synthesizer = SpeechSynthesizer(model=MODEL_NAME, voice=VOICE_TYPE)
        audio_data = synthesizer.call(text)

        if audio_data:
            with open(audio_path, 'wb') as f:
                f.write(audio_data)
            os.chmod(audio_path, 0o644)
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
    # rag_service 必须在 app.run 之前被初始化
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
        safe_name = secure_filename(filename)
        logging.info(f"请求音频文件: {safe_name}")
        return send_from_directory(
            directory=AUDIO_FOLDER,
            path=safe_name,
            mimetype="audio/mpeg",
            conditional=True
        )
    except FileNotFoundError:
        logging.warning(f"音频文件不存在: {safe_name}")
        return jsonify({"error": "音频文件不存在"}), 404


# ---------------------- 服务启动优化 ----------------------
if __name__ == "__main__":
    # 配置日志系统，在生产测试时可以调高日志级别以减少开销
    logging.basicConfig(
        level=logging.INFO, # 或 logging.WARNING, logging.ERROR
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

    # 假设 backend 文件夹位于 BASE_DIR 下
    backend_folder = BASE_DIR / "backend"

    # 构建索引和模型的绝对路径
    # 根据您当前成功的加载日志，索引路径是 'index_ivf'
    index_base_path = backend_folder / "multilingual_ivf_index"
    # 模型路径是 'plus_bge_zh_model'
    model_base_path = backend_folder / "optimized_qa_model"

    # 初始化 RAG 服务
    rag_service = RAGService(
        index_path=index_base_path,
        model_path=model_base_path
    )

    # 预热检查
    try:
        rag_service.search("系统预热查询")
        logging.info("RAG服务预热成功")
    except Exception as e:
        logging.critical(f"RAG服务初始化失败: {str(e)}")
        exit(1)

    app.run(port=5000, debug=False)