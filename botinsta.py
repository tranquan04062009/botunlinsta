import telebot
import time
import math
import random
from collections import deque, defaultdict
import numpy as np
from datetime import datetime
import logging
import json
import os
import threading
import sys
import signal
import psutil
import gc
from tensorflow import keras
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

logging.basicConfig(
    filename='bot_log_advanced_no_comments.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

TOKEN = "7834807188:AAFtO6u6mJ-1EaDm4W4qA_cb4KgICqSo734"

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "bot_data_advanced_no_comments.json"
CONFIG_FILE = "bot_config_advanced_no_comments.json"

class BotDataAdvanced:
    def __init__(self):
        self.history = deque(maxlen=2000)
        self.prediction_history = deque(maxlen=1000)
        self.pattern_cache = {}
        self.markov_matrix = defaultdict(lambda: defaultdict(float))
        self.weights = [1.0] * 30
        self.fibonacci_cache = {}
        self.last_update = time.time()
        self.accuracy = 0.0
        self.total_predictions = 0
        self.correct_predictions = 0
        self.error_count = 0
        self.model_weights = {"markov": 1.0, "pattern": 1.0, "weighted": 1.0, "nn": 1.0, "fibonacci": 1.0, "gboost": 1.0, "stats": 1.0, "periodicity": 1.0, "flip_trend": 1.0, "self_learn_nn": 1.0} # Added weight for self-learning NN
        self.self_learn_nn_model = self.create_self_learning_nn() # Initialize self-learning NN
        self.nn_history_buffer = deque(maxlen=30) # History for training self-learning NN

    def create_self_learning_nn(self):
        model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=(30,)), # Input is last 30 results
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid') # Output probability for Tai
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']) # Using Adam and binary crossentropy
        return model

    def train_self_learning_nn(self, history_sequence, actual_result):
        if len(history_sequence) < 30: # Ensure enough history for input
            return
        history_input = np.array([history_sequence]) # Reshape for model input [batch_size, input_dim]
        actual_output = np.array([actual_result]) # [batch_size, output_dim]

        self.self_learn_nn_model.train_on_batch(history_input, actual_output) # Online training - single batch


    def save_data(self):
        try:
            data = {
                "history": list(self.history),
                "prediction_history": list(self.prediction_history),
                "pattern_cache": self.pattern_cache,
                "markov_matrix": dict(self.markov_matrix),
                "weights": self.weights,
                "fibonacci_cache": self.fibonacci_cache,
                "accuracy": self.accuracy,
                "total_predictions": self.total_predictions,
                "correct_predictions": self.correct_predictions,
                "error_count": self.error_count,
                "model_weights": self.model_weights
            }
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            logging.info("Dữ liệu đã được lưu (Nâng cao No Comments).")
        except Exception as e:
            logging.error(f"Lỗi khi lưu dữ liệu (Nâng cao No Comments): {str(e)}")
            self.error_count += 1

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.history = deque(data.get("history", []), maxlen=2000)
                    self.prediction_history = deque(data.get("prediction_history", []), maxlen=1000)
                    self.pattern_cache = data.get("pattern_cache", {})
                    self.markov_matrix = defaultdict(lambda: defaultdict(float), data.get("markov_matrix", {}))
                    self.weights = data.get("weights", [1.0] * 30)
                    self.fibonacci_cache = data.get("fibonacci_cache", {})
                    self.accuracy = data.get("accuracy", 0.0)
                    self.total_predictions = data.get("total_predictions", 0)
                    self.correct_predictions = data.get("correct_predictions", 0)
                    self.error_count = data.get("error_count", 0)
                    self.model_weights = data.get("model_weights", {"markov": 1.0, "pattern": 1.0, "weighted": 1.0, "nn": 1.0, "fibonacci": 1.0, "gboost": 1.0, "stats": 1.0, "periodicity": 1.0, "flip_trend": 1.0, "self_learn_nn": 1.0})
                logging.info("Dữ liệu đã được tải (Nâng cao No Comments).")
            except Exception as e:
                logging.error(f"Lỗi khi tải dữ liệu (Nâng cao No Comments): {str(e)}")
                self.error_count += 1
        else:
            logging.info("Không tìm thấy file dữ liệu (Nâng cao No Comments), khởi tạo mới.")

bot_data = BotDataAdvanced()
bot_data.load_data()

class BotConfigAdvanced:
    def __init__(self):
        self.min_history_length = 7
        self.max_confidence = 0.995
        self.pattern_lengths = [3, 5, 7, 9, 12]
        self.markov_order = 4
        self.entropy_threshold = 0.85
        self.weight_adjust_rate = 0.20
        self.fibonacci_threshold = 7
        self.pattern_score_multiplier = 1.1
        self.markov_smoothing = 0.01
        self.nn_bias = 0.15
        self.boost_rate = 0.12
        self.stats_weight = 0.1
        self.periodicity_weight = 0.08
        self.flip_trend_weight = 0.06
        self.confidence_multiplier = 2.8
        self.confidence_base = 0.7
        self.ensemble_method = "weighted_average"
        self.self_learn_nn_weight = 0.15 # Weight for self-learning NN

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.min_history_length = data.get("min_history_length", 7)
                    self.max_confidence = data.get("max_confidence", 0.995)
                    self.pattern_lengths = data.get("pattern_lengths", [3, 5, 7, 9, 12])
                    self.markov_order = data.get("markov_order", 4)
                    self.entropy_threshold = data.get("entropy_threshold", 0.85)
                    self.weight_adjust_rate = data.get("weight_adjust_rate", 0.20)
                    self.fibonacci_threshold = data.get("fibonacci_threshold", 7)
                    self.pattern_score_multiplier = data.get("pattern_score_multiplier", 1.1)
                    self.markov_smoothing = data.get("markov_smoothing", 0.01)
                    self.nn_bias = data.get("nn_bias", 0.15)
                    self.boost_rate = data.get("boost_rate", 0.12)
                    self.stats_weight = data.get("stats_weight", 0.1)
                    self.periodicity_weight = data.get("periodicity_weight", 0.08)
                    self.flip_trend_weight = data.get("flip_trend_weight", 0.06)
                    self.confidence_multiplier = data.get("confidence_multiplier", 2.8)
                    self.confidence_base = data.get("confidence_base", 0.7)
                    self.ensemble_method = data.get("ensemble_method", "weighted_average")
                    self.self_learn_nn_weight = data.get("self_learn_nn_weight", 0.15) # Load weight
                logging.info("Cấu hình đã được tải (Nâng cao No Comments).")
            except Exception as e:
                logging.error(f"Lỗi khi tải cấu hình (Nâng cao No Comments): {str(e)}")
        else:
            self.save_config()
            logging.info("Tạo cấu hình mặc định (Nâng cao No Comments).")

    def save_config(self):
        try:
            data = {
                "min_history_length": self.min_history_length,
                "max_confidence": self.max_confidence,
                "pattern_lengths": self.pattern_lengths,
                "markov_order": self.markov_order,
                "entropy_threshold": self.entropy_threshold,
                "weight_adjust_rate": self.weight_adjust_rate,
                "fibonacci_threshold": self.fibonacci_threshold,
                "pattern_score_multiplier": self.pattern_score_multiplier,
                "markov_smoothing": self.markov_smoothing,
                "nn_bias": self.nn_bias,
                "boost_rate": self.boost_rate,
                "stats_weight": self.stats_weight,
                "periodicity_weight": self.periodicity_weight,
                "flip_trend_weight": self.flip_trend_weight,
                "confidence_multiplier": self.confidence_multiplier,
                "confidence_base": self.confidence_base,
                "ensemble_method": self.ensemble_method,
                "self_learn_nn_weight": self.self_learn_nn_weight # Save weight
            }
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logging.error(f"Lỗi khi lưu cấu hình (Nâng cao No Comments): {str(e)}")

bot_config = BotConfigAdvanced()
bot_config.load_config()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user.first_name
    response = (
        f"Chào {user}!\n"
        "Bot AI Tài/Xỉu 2025 (Advanced No Comments).\n"
        "Dùng lệnh:\n"
        "/add <chuỗi> - Thêm chuỗi (t = Tài, x = Xỉu, ví dụ: /add txtxtttx)\n"
        "/predict - Dự đoán kết quả\n"
        "/history - Xem lịch sử cầu\n"
        "/stats - Xem thống kê hiệu suất\n"
        "/feedback <t/x> - Phản hồi kết quả thực tế\n"
        "/config - Xem cấu hình nâng cao\n"
        "/analyze - Phân tích cầu chi tiết"
    )
    bot.reply_to(message, response)
    logging.info(f"User {user} đã khởi động bot phiên bản nâng cao (No Comments).")

def validate_input(sequence):
    return all(char in "tx" for char in sequence.lower())

def parse_sequence(sequence):
    return [1 if char == "t" else 0 for char in sequence.lower()]

@bot.message_handler(commands=['add'])
def add_result(message):
    try:
        args = message.text.split(maxsplit=1)[1].lower()
        if not validate_input(args):
            bot.reply_to(message, "Chuỗi không hợp lệ! Chỉ dùng 't' (Tài) hoặc 'x' (Xỉu).")
            return

        sequence = parse_sequence(args)
        for result in sequence:
            bot_data.history.append(result)
            bot_data.nn_history_buffer.append(result) # Add to NN history buffer
            update_markov_matrix(result)
            update_fibonacci_cache(result)

        added_str = "".join(["Tài" if x == 1 else "Xỉu" for x in sequence])
        bot.reply_to(message, f"Đã thêm: {added_str} ✅ (Phiên bản Nâng cao No Comments)")
        logging.info(f"Đã thêm chuỗi (Nâng cao No Comments): {added_str}")
        bot_data.save_data()

    except IndexError:
        bot.reply_to(message, "Vui lòng nhập chuỗi sau /add! Ví dụ: /add txtxtttx")
    except Exception as e:
        logging.error(f"Lỗi khi thêm chuỗi (Nâng cao No Comments): {str(e)}")
        bot.reply_to(message, "Đã xảy ra lỗi khi thêm chuỗi! (Phiên bản Nâng cao No Comments)")
        bot_data.error_count += 1

def update_markov_matrix(result):
    try:
        if len(bot_data.history) >= bot_config.markov_order + 1:
            sequence = list(bot_data.history)[-bot_config.markov_order-1:-1]
            key = tuple(sequence)
            bot_data.markov_matrix[key][result] += 1
    except Exception as e:
        logging.error(f"Lỗi khi cập nhật Markov (Nâng cao No Comments): {str(e)}")
        bot_data.error_count += 1

def update_fibonacci_cache(result):
    try:
        last_results = list(bot_data.history)[-bot_config.fibonacci_threshold:]
        if len(last_results) >= bot_config.fibonacci_threshold:
            key = tuple(last_results[:-1])
            bot_data.fibonacci_cache[key] = bot_data.fibonacci_cache.get(key, 0) + (1 if result == 1 else -1)
    except Exception as e:
        logging.error(f"Lỗi khi cập nhật Fibonacci (Nâng cao No Comments): {str(e)}")
        bot_data.error_count += 1

def calculate_entropy(data):
    try:
        if not data:
            return 0
        p_tai = sum(1 for x in data if x == 1) / len(data)
        p_xiu = 1 - p_tai
        if p_tai == 0 or p_xiu == 0:
            return 0
        return - (p_tai * math.log2(p_tai) + p_xiu * math.log2(p_xiu))
    except Exception as e:
        logging.error(f"Lỗi khi tính entropy (Nâng cao No Comments): {str(e)}")
        return 0

def analyze_patterns(history, lengths):
    try:
        pattern_score = 0
        last_results = list(history)

        for length in lengths:
            if len(last_results) >= length:
                last_n = last_results[-length:]
                if all(x == 1 for x in last_n):
                    pattern_score = -0.95 * (length / max(lengths)) * bot_config.pattern_score_multiplier
                    break
                elif all(x == 0 for x in last_n):
                    pattern_score = 0.95 * (length / max(lengths)) * bot_config.pattern_score_multiplier
                    break
                elif length >= 3:
                    if last_n[-3:] in [[1, 0, 1], [0, 1, 0]]:
                        pattern_score = 0.6 * bot_config.pattern_score_multiplier if last_n[-1] == 0 else -0.6 * bot_config.pattern_score_multiplier
                    elif len(set(last_n)) == 1:
                        pattern_score = -0.7 * bot_config.pattern_score_multiplier if last_n[-1] == 1 else 0.7 * bot_config.pattern_score_multiplier
        return pattern_score
    except Exception as e:
        logging.error(f"Lỗi khi phân tích mẫu (Nâng cao No Comments): {str(e)}")
        return 0

def markov_probability(history):
    try:
        if len(history) < bot_config.markov_order + 1:
            return 0.5, 0.5
        last_seq = tuple(list(history)[-bot_config.markov_order:])
        transitions = bot_data.markov_matrix.get(last_seq, {1: bot_config.markov_smoothing, 0: bot_config.markov_smoothing})
        total = transitions.get(1, bot_config.markov_smoothing) + transitions.get(0, bot_config.markov_smoothing)
        return (transitions.get(1, bot_config.markov_smoothing) + bot_config.markov_smoothing) / (total + 2 * bot_config.markov_smoothing), \
               (transitions.get(0, bot_config.markov_smoothing) + bot_config.markov_smoothing) / (total + 2 * bot_config.markov_smoothing)
    except Exception as e:
        logging.error(f"Lỗi khi tính Markov (Nâng cao No Comments): {str(e)}")
        return 0.5, 0.5

def weighted_probability(history, weights):
    try:
        if not history:
            return 0.5, 0.5
        total_weight = 0
        tai_weighted = 0
        xiu_weighted = 0
        for i, result in enumerate(history):
            idx = min(i // (len(history) // len(weights) + 1) if (len(history) // len(weights) + 1) > 0 else 0, len(weights) - 1)
            weight = weights[idx]
            total_weight += weight
            if result == 1:
                tai_weighted += weight
            else:
                xiu_weighted += weight

        if total_weight == 0:
            return 0.5, 0.5

        return tai_weighted / total_weight, xiu_weighted / total_weight
    except Exception as e:
        logging.error(f"Lỗi khi tính trọng số (Nâng cao No Comments): {str(e)}")
        return 0.5, 0.5

def adaptive_neural_network(history):
    try:
        inputs = np.array(list(history)[-15:] + [0] * (15 - min(15, len(history))))
        weights = np.array([0.07 * (i + 1) for i in range(15)])
        bias = bot_config.nn_bias

        output = np.dot(inputs, weights) + bias
        sigmoid_output = 1 / (1 + np.exp(-output))
        return sigmoid_output
    except Exception as e:
        logging.error(f"Lỗi khi chạy NN (Nâng cao No Comments): {str(e)}")
        return 0.5

def fibonacci_predict(history):
    try:
        if len(history) < bot_config.fibonacci_threshold:
            return 0.5
        last_seq = tuple(list(history)[-bot_config.fibonacci_threshold+1:])
        fib_score = bot_data.fibonacci_cache.get(last_seq, 0)
        return 1 / (1 + math.exp(-fib_score * 0.1))
    except Exception as e:
        logging.error(f"Lỗi khi dự đoán Fibonacci (Nâng cao No Comments): {str(e)}")
        return 0.5

def gradient_boost_predict(history):
    try:
        if len(history) < 10:
            return 0.5
        errors = [0.0] * 10
        last_prediction = 0.5
        for i in range(min(10, len(history))):
            actual = history[-i-1]
            error = actual - last_prediction
            errors[i] = error
            last_prediction += error * bot_config.boost_rate
        boosted_prediction = 0.5 + sum(errors) * 0.1
        return max(0, min(1, boosted_prediction))
    except Exception as e:
        logging.error(f"Lỗi khi dự đoán Gradient Boost (Nâng cao No Comments): {str(e)}")
        return 0.5

def self_learning_nn_predict(history):
    try:
        if len(history) < 30: # Minimum history for self-learning NN input
            return 0.5
        inputs = np.array([list(history)[-30:] + [0] * (30 - min(30, len(history)))]) # Pad history
        prediction = bot_data.self_learn_nn_model.predict(inputs, verbose=0)[0][0] # Get single prediction, suppress verbose output
        return prediction # Probability of Tai
    except Exception as e:
        logging.error(f"Lỗi khi dự đoán Self-Learning NN (Nâng cao No Comments): {str(e)}")
        return 0.5


def adjust_weights():
    try:
        if len(bot_data.prediction_history) < 10:
            return
        accuracy = bot_data.accuracy
        for i in range(len(bot_data.weights)):
            bot_data.weights[i] *= (1 + bot_config.weight_adjust_rate * (accuracy - 0.5))
            bot_data.weights[i] = max(0.05, min(15.0, bot_data.weights[i]))
    except Exception as e:
        logging.error(f"Lỗi khi điều chỉnh trọng số (Nâng cao No Comments): {str(e)}")

def analyze_bridge(history):
    try:
        if len(history) < 10:
            return "Chưa đủ dữ liệu để phân tích cầu!"

        tai_ratio = sum(1 for x in history if x == 1) / len(history)
        max_tai_streak = max_xiu_streak = current_streak = 0
        current_value = None
        for result in history:
            if result == current_value:
                current_streak += 1
            else:
                if current_value == 1:
                    max_tai_streak = max(max_tai_streak, current_streak)
                elif current_value == 0:
                    max_xiu_streak = max(max_xiu_streak, current_streak)
                current_streak = 1
                current_value = result

        flips = sum(1 for i in range(len(history) - 1) if history[i] != history[i+1])
        flip_rate = flips / (len(history) - 1) if len(history) > 1 else 0

        return (
            f"Phân tích cầu (Nâng cao No Comments):\n"
            f"- Tỷ lệ Tài: {tai_ratio:.2%}\n"
            f"- Chuỗi Tài dài nhất: {max_tai_streak}\n"
            f"- Chuỗi Xỉu dài nhất: {max_xiu_streak}\n"
            f"- Tỷ lệ đảo cầu: {flip_rate:.2%}"
        )
    except Exception as e:
        logging.error(f"Lỗi khi phân tích cầu (Nâng cao No Comments): {str(e)}")
        return "Lỗi khi phân tích cầu! (Nâng cao No Comments)"

def advanced_statistics(history):
    try:
        if len(history) < 10:
            return {}
        stats = {
            "tai_ratio": sum(1 for x in history if x == 1) / len(history),
            "xiu_ratio": sum(1 for x in history if x == 0) / len(history),
            "longest_tai_streak": 0,
            "longest_xiu_streak": 0,
            "flip_count": 0
        }
        current_streak = 0
        current_value = None
        for i, result in enumerate(history):
            if result == current_value:
                current_streak += 1
            else:
                if current_value == 1:
                    stats["longest_tai_streak"] = max(stats["longest_tai_streak"], current_streak)
                elif current_value == 0:
                    stats["longest_xiu_streak"] = max(stats["longest_xiu_streak"], current_streak)
                current_streak = 1
                current_value = result
            if i > 0 and result != history[i-1]:
                stats["flip_count"] += 1
        return stats
    except Exception as e:
        logging.error(f"Lỗi khi tính thống kê nâng cao (Nâng cao No Comments): {str(e)}")
        return {}

def stats_based_predict(history):
    try:
        stats = advanced_statistics(history)
        if stats.get("longest_tai_streak", 0) >= 7:
            return 0, min(0.92, stats.get("longest_tai_streak", 0) * 0.02 + 0.78)
        elif stats.get("longest_xiu_streak", 0) >= 7:
            return 1, min(0.92, stats.get("longest_xiu_streak", 0) * 0.02 + 0.78)
        return None, 0
    except Exception as e:
        logging.error(f"Lỗi khi dự đoán dựa trên thống kê (Nâng cao No Comments): {str(e)}")
        return None, 0

def detect_periodicity(history):
    try:
        if len(history) < 20:
            return 0
        fft = np.fft.fft(list(history))
        freq = np.fft.fftfreq(len(history))
        power = np.abs(fft) ** 2
        dominant_freq = freq[np.argmax(power[1:]) + 1]
        return abs(1 / dominant_freq) if dominant_freq != 0 else 0
    except Exception as e:
        logging.error(f"Lỗi khi phát hiện tuần hoàn (Nâng cao No Comments): {str(e)}")
        return 0

def periodicity_predict(history):
    try:
        period = detect_periodicity(history)
        if period > 0 and len(history) >= period * 1.5:
            last_cycle = list(history)[-int(round(period)):]
            predicted_result = last_cycle[0]
            confidence = min(0.88, (1/period) * 0.3 + 0.55)
            return predicted_result, confidence
        return None, 0
    except Exception as e:
        logging.error(f"Lỗi khi dự đoán tuần hoàn (Nâng cao No Comments): {str(e)}")
        return None, 0

def flip_trend_analysis(history):
    try:
        if len(history) < 15:
            return 0
        flips = [1 if history[i] != history[i+1] else 0 for i in range(len(history)-1)]
        recent_flips = sum(flips[-15:]) / 15 if len(flips) >= 15 else sum(flips) / len(flips)
        return (recent_flips - 0.5) * 2.0
    except Exception as e:
        logging.error(f"Lỗi khi phân tích xu hướng đảo (Nâng cao No Comments): {str(e)}")
        return 0

def ultimate_predict(history):
    try:
        model_predictions = {}

        markov_tai, markov_xiu = markov_probability(history)
        model_predictions["markov"] = markov_tai
        pattern_score = analyze_patterns(history, bot_config.pattern_lengths)
        model_predictions["pattern"] = 0.5 - pattern_score

        tai_prob_weighted, xiu_prob_weighted = weighted_probability(history, bot_data.weights)
        model_predictions["weighted"] = tai_prob_weighted

        nn_prob = adaptive_neural_network(history)
        model_predictions["nn"] = nn_prob

        fib_prob = fibonacci_predict(history)
        model_predictions["fibonacci"] = fib_prob

        boost_prob = gradient_boost_predict(history)
        model_predictions["gboost"] = boost_prob

        stats_pred, stats_conf = stats_based_predict(history)
        if stats_pred is not None:
            model_predictions["stats"] = stats_pred if stats_pred == 1 else (1-stats_pred)
            model_predictions["stats_conf"] = stats_conf
        else:
            model_predictions["stats"] = 0.5
            model_predictions["stats_conf"] = 0

        period_pred, period_conf = periodicity_predict(history)
        if period_pred is not None:
            model_predictions["periodicity"] = period_pred if period_pred == 1 else (1-period_pred)
            model_predictions["periodicity_conf"] = period_conf
        else:
            model_predictions["periodicity"] = 0.5
            model_predictions["periodicity_conf"] = 0

        flip_trend_score = flip_trend_analysis(history)
        model_predictions["flip_trend"] = 0.5 - flip_trend_score

        self_learn_nn_prob = self_learning_nn_predict(history) # Get prediction from self-learning NN
        model_predictions["self_learn_nn"] = self_learn_nn_prob


        if bot_config.ensemble_method == "weighted_average":
            final_score = 0
            total_weight = 0
            for model_name, weight in bot_data.model_weights.items():
                if model_name in model_predictions:
                    prediction_value = model_predictions[model_name]
                    final_score += prediction_value * weight
                    total_weight += weight

            if total_weight > 0:
                final_score /= total_weight
            else:
                final_score = 0.5

        elif bot_config.ensemble_method == "stacking":

            features = [v for k, v in model_predictions.items() if k not in ["stats_conf", "periodicity_conf"]]

            stacking_weights = {
                "markov": 0.15, "pattern": 0.1, "weighted": 0.2, "nn": 0.3, "fibonacci": 0.05, "gboost": 0.1, "stats": 0.05, "periodicity": 0.03, "flip_trend": 0.02, "self_learn_nn": 0.1 # Added weight for self-learning NN
            }
            final_score_stacked = 0
            for model_name, weight in stacking_weights.items():
                if model_name in model_predictions:
                    final_score_stacked += model_predictions[model_name] * weight
            final_score = final_score_stacked

        else:
            final_score = model_predictions.get("nn", 0.5)


        prediction = 1 if final_score > 0.5 else 0
        entropy = calculate_entropy(list(bot_data.history)[-30:])
        confidence_adjust = max(bot_config.confidence_base, 1 - (entropy / bot_config.entropy_threshold))
        confidence = min(bot_config.max_confidence, abs(final_score - 0.5) * bot_config.confidence_multiplier * confidence_adjust)

        return prediction, confidence, model_predictions

    except Exception as e:
        logging.error(f"Lỗi khi tích hợp dự đoán cuối cùng (Nâng cao No Comments): {str(e)}")
        return 0, 0.5, {}

@bot.message_handler(commands=['predict'])
def predict(message):
    try:
        if len(bot_data.history) < bot_config.min_history_length:
            bot.reply_to(message, f"Vui lòng thêm ít nhất {bot_config.min_history_length} kết quả để dự đoán! (Phiên bản Nâng cao No Comments)")
            return

        adjust_weights()
        prediction, confidence, model_predictions = ultimate_predict(bot_data.history)

        pred_str = "Tài" if prediction == 1 else "Xỉu"

        response_parts = [
            f"**Dự đoán (Nâng cao No Comments): {pred_str}**\n",
            f"**Độ tin cậy: {confidence:.2%}**\n",
            "(Chi tiết mô hình):",
            f"- Weighted Avg: {model_predictions.get('weighted', 0.5):.2%}",
            f"- Markov: {model_predictions.get('markov', 0.5):.2%}",
            f"- NN: {model_predictions.get('nn', 0.5):.2%}",
            f"- Fibonacci: {model_predictions.get('fibonacci', 0.5):.2%}",
            f"- GBoost: {model_predictions.get('gboost', 0.5):.2%}",
            f"- Pattern: {model_predictions.get('pattern', 0.5):.2%}",
            f"- Stats: {model_predictions.get('stats', 0.5):.2%}",
            f"- Periodicity: {model_predictions.get('periodicity', 0.5):.2%}",
            f"- Flip Trend: {model_predictions.get('flip_trend', 0.5):.2%}",
            f"- Self-Learn NN: {model_predictions.get('self_learn_nn', 0.5):.2%}", # Include self-learn NN in output
            f"Ensemble Method: {bot_config.ensemble_method}"
        ]
        response = "\n".join(response_parts)
        bot.reply_to(message, response, parse_mode="Markdown")
        logging.info(f"Dự đoán (Nâng cao No Comments): {pred_str}, Độ tin cậy: {confidence:.2%}, Mô hình chi tiết: {model_predictions}")

        bot_data.total_predictions += 1
        bot_data.prediction_history.append((prediction, None))
    except Exception as e:
        logging.error(f"Lỗi khi dự đoán (Nâng cao No Comments): {str(e)}")
        bot.reply_to(message, "Đã xảy ra lỗi khi dự đoán! (Phiên bản Nâng cao No Comments)")
        bot_data.error_count += 1

@bot.message_handler(commands=['feedback'])
def handle_feedback(message):
    try:
        args = message.text.split(maxsplit=1)[1].lower()
        if args not in ["t", "x"]:
            bot.reply_to(message, "Phản hồi không hợp lệ! Dùng 't' (Tài) hoặc 'x' (Xỉu).")
            return

        actual = 1 if args == "t" else 0
        if bot_data.prediction_history:
            last_pred, _ = bot_data.prediction_history.pop()
            bot_data.prediction_history.append((last_pred, actual))

            history_seq_for_nn = list(bot_data.nn_history_buffer) # Current NN buffer content for training
            bot_data.train_self_learning_nn(history_seq_for_nn, actual) # Train self-learning NN after feedback


            if last_pred == actual:
                bot_data.correct_predictions += 1
            bot_data.accuracy = bot_data.correct_predictions / bot_data.total_predictions if bot_data.total_predictions > 0 else 0.0
            bot_data.save_data()
            bot.reply_to(message, f"Đã ghi nhận phản hồi: {'Tài' if actual == 1 else 'Xỉu'} (Phiên bản Nâng cao No Comments)")
            logging.info(f"Phản hồi (Nâng cao No Comments): {'Tài' if actual == 1 else 'Xỉu'}, Độ chính xác: {bot_data.accuracy:.2%}")
    except IndexError:
        bot.reply_to(message, "Vui lòng cung cấp phản hồi! Ví dụ: /feedback t")
    except Exception as e:
        logging.error(f"Lỗi khi xử lý phản hồi (Nâng cao No Comments): {str(e)}")
        bot.reply_to(message, "Lỗi khi ghi nhận phản hồi! (Phiên bản Nâng cao No Comments)")
        bot_data.error_count += 1

@bot.message_handler(commands=['history'])
def show_history(message):
    try:
        if not bot_data.history:
            bot.reply_to(message, "Chưa có lịch sử cầu! (Phiên bản Nâng cao No Comments)")
            return
        history_str = "".join(["T" if x == 1 else "X" for x in bot_data.history])
        bot.reply_to(message, f"Lịch sử cầu (Nâng cao No Comments) (Last 200 chars):\n{history_str[-200:]}")
    except Exception as e:
        logging.error(f"Lỗi khi xem lịch sử (Nâng cao No Comments): {str(e)}")
        bot.reply_to(message, "Lỗi khi hiển thị lịch sử! (Phiên bản Nâng cao No Comments)")

@bot.message_handler(commands=['stats'])
def show_stats(message):
    try:
        if not bot_data.prediction_history:
            bot.reply_to(message, "Chưa có dữ liệu dự đoán! (Phiên bản Nâng cao No Comments)")
            return
        response = (
            f"**Thống kê hiệu suất (Nâng cao No Comments):**\n"
            f"- Độ chính xác: {bot_data.accuracy:.2%}\n"
            f"- Tổng dự đoán: {bot_data.total_predictions}\n"
            f"- Dự đoán đúng: {bot_data.correct_predictions}\n"
            f"- Số lỗi hệ thống: {bot_data.error_count}"
        )
        bot.reply_to(message, response, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Lỗi khi xem thống kê (Nâng cao No Comments): {str(e)}")
        bot.reply_to(message, "Lỗi khi hiển thị thống kê! (Phiên bản Nâng cao No Comments)")

@bot.message_handler(commands=['config'])
def show_config(message):
    try:
        config_str_parts = [
            "**Cấu hình hiện tại (Nâng cao No Comments):**\n",
            f"- Độ dài tối thiểu: {bot_config.min_history_length}",
            f"- Độ tin cậy tối đa: {bot_config.max_confidence:.2%}",
            f"- Độ dài mẫu: {bot_config.pattern_lengths}",
            f"- Bậc Markov: {bot_config.markov_order}",
            f"- Ngưỡng Entropy: {bot_config.entropy_threshold}",
            f"- Ngưỡng Fibonacci: {bot_config.fibonacci_threshold}",
            f"- Multiplier mẫu: {bot_config.pattern_score_multiplier}",
            f"- Smoothing Markov: {bot_config.markov_smoothing}",
            f"- Bias NN: {bot_config.nn_bias}",
            f"- Rate GBoost: {bot_config.boost_rate}",
            f"- Trọng số Stats: {bot_config.stats_weight}",
            f"- Trọng số Periodicity: {bot_config.periodicity_weight}",
            f"- Trọng số Flip Trend: {bot_config.flip_trend_weight}",
            f"- Confidence Multiplier: {bot_config.confidence_multiplier}",
            f"- Confidence Base: {bot_config.confidence_base}",
            f"- Ensemble Method: {bot_config.ensemble_method}",
            f"- Self-Learn NN Weight: {bot_config.self_learn_nn_weight}", # Show self-learn NN weight
            "\n**Trọng số mô hình:**",
            f"- Markov: {bot_data.model_weights.get('markov', 1.0)}",
            f"- Pattern: {bot_data.model_weights.get('pattern', 1.0)}",
            f"- Weighted: {bot_data.model_weights.get('weighted', 1.0)}",
            f"- NN: {bot_data.model_weights.get('nn', 1.0)}",
            f"- Fibonacci: {bot_data.model_weights.get('fibonacci', 1.0)}",
            f"- GBoost: {bot_data.model_weights.get('gboost', 1.0)}",
            f"- Stats: {bot_data.model_weights.get('stats', 1.0)}",
            f"- Periodicity: {bot_data.model_weights.get('periodicity', 1.0)}",
            f"- Flip Trend: {bot_data.model_weights.get('flip_trend', 1.0)}",
            f"- Self-Learn NN: {bot_data.model_weights.get('self_learn_nn', 1.0)}" # Show self-learn NN weight
        ]
        response = "\n".join(config_str_parts)
        bot.reply_to(message, response, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Lỗi khi xem cấu hình (Nâng cao No Comments): {str(e)}")
        bot.reply_to(message, "Lỗi khi hiển thị cấu hình! (Phiên bản Nâng cao No Comments)")

@bot.message_handler(commands=['analyze'])
def analyze_bridge_handler(message):
    try:
        analysis = analyze_bridge(bot_data.history)
        bot.reply_to(message, analysis)
    except Exception as e:
        logging.error(f"Lỗi khi phân tích cầu (Nâng cao No Comments): {str(e)}")
        bot.reply_to(message, "Lỗi khi phân tích cầu! (Nâng cao No Comments)")

@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.reply_to(message, "Lệnh không hợp lệ! Dùng /start để xem hướng dẫn (Phiên bản Nâng cao No Comments).")
    logging.warning(f"Tin nhắn không hợp lệ từ {message.from_user.id}: {message.text} (Phiên bản Nâng cao No Comments)")

def memory_optimization():
    try:
        gc.collect()
        if len(bot_data.history) > 1500:
            bot_data.history = deque(list(bot_data.history)[-1000:], maxlen=2000)
        logging.info("Đã tối ưu hóa bộ nhớ. (Phiên bản Nâng cao No Comments)")
    except Exception as e:
        logging.error(f"Lỗi khi tối ưu hóa bộ nhớ (Nâng cao No Comments): {str(e)}")

def check_cpu_usage():
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as e:
        logging.error(f"Lỗi khi kiểm tra CPU (Nâng cao No Comments): {str(e)}")
        return 0

def background_task():
    while True:
        try:
            time.sleep(240)
            bot_data.save_data()
            memory_optimization()
            cpu_usage = check_cpu_usage()
            if cpu_usage > 95:
                logging.warning(f"CPU usage cao: {cpu_usage}% (Phiên bản Nâng cao No Comments)")
        except Exception as e:
            logging.error(f"Lỗi trong luồng nền (Nâng cao No Comments): {str(e)}")
            bot_data.error_count += 1

def handle_shutdown(signal, frame):
    bot_data.save_data()
    logging.info("Bot đã dừng và lưu dữ liệu. (Phiên bản Nâng cao No Comments)")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_shutdown)

def check_data_integrity():
    try:
        if any(x not in [0, 1] for x in bot_data.history):
            bot_data.history = deque([x for x in bot_data.history if x in [0, 1]], maxlen=2000)
            logging.warning("Đã sửa lỗi dữ liệu lịch sử. (Phiên bản Nâng cao No Comments)")
        if any(not isinstance(p, tuple) or len(p) != 2 for p in bot_data.prediction_history):
            bot_data.prediction_history = deque([p for p in bot_data.prediction_history if isinstance(p, tuple) and len(p) == 2], maxlen=1000)
            logging.warning("Đã sửa lỗi dữ liệu dự đoán. (Phiên bản Nâng cao No Comments)")
    except Exception as e:
        logging.error(f"Lỗi khi kiểm tra dữ liệu (Nâng cao No Comments): {str(e)}")

check_data_integrity()

if __name__ == "__main__":
    print("Bot nâng cao (no comments) đang chạy...")
    logging.info("Bot phiên bản nâng cao (no comments) đã khởi động.")

    bg_thread = threading.Thread(target=background_task, daemon=True)
    bg_thread.start()

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Lỗi khi chạy bot phiên bản nâng cao (no comments): {str(e)}")
        bot_data.error_count += 1
        sys.exit(1)

logging.info("Bot nâng cao (no comments) đã được cập nhật và sẵn sàng với kỹ thuật 2025+!")
print("Bot nâng cao (no comments) đã sẵn sàng với kỹ thuật tối đa 2025+!")