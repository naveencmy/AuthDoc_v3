import cv2
import numpy as np
import re
from paddleocr import PaddleOCR
from sklearn.cluster import KMeans
from layout_analyzer import analyze_layout

ocr = PaddleOCR(
    use_angle_cls=True,
    lang="fr",
    det_db_thresh=0.1,
    det_db_box_thresh=0.2,
    det_db_unclip_ratio=2.5,
    det_limit_side_len=4000,
    use_gpu=False
)

def preprocess(path):
    img = cv2.imread(path)
    img = cv2.resize(
        img,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(
        clipLimit=3.0,
        tileGridSize=(8,8)
    )
    gray = clahe.apply(gray)
    return gray

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zàâéèêëîïôûùç]", "", text)
    return text

def is_valid_text(text, confidence):
    if confidence < 0.6:
        return False
    if len(text) < 3:
        return False
    letters = sum(c.isalpha() for c in text)
    return letters > len(text) * 0.4

def segment_columns(blocks):
    if len(blocks) == 0:
        return {"columns": []}
    xs = np.array([[b["x"]] for b in blocks])
    kmeans = KMeans(n_clusters=2, random_state=0).fit(xs)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    left_cluster = np.argmin(centers)
    right_cluster = np.argmax(centers)
    left = []
    right = []
    for i, b in enumerate(blocks):
        if labels[i] == left_cluster:
            left.append(b)
        else:
            right.append(b)
    left = sorted(left, key=lambda b: (b["y"], b["x"]))
    right = sorted(right, key=lambda b: (b["y"], b["x"]))
    return {
        "columns": [
            {"name": "left", "blocks": left},
            {"name": "main", "blocks": right}
        ]
    }

def reconstruct_reading_order(columns):
    ordered_blocks = []
    for column in columns:
        blocks = column["blocks"]
        blocks = sorted(
            blocks,
            key=lambda b: b["y"]
        )
        ordered_blocks.extend(blocks)
    return ordered_blocks

def group_vertical(blocks):
    if not blocks:
        return []
    groups = []
    current = [blocks[0]]
    for b in blocks[1:]:
        prev = current[-1]
        if abs(b["y"] - prev["y"]) < prev["height"] * 1.8:
            current.append(b)
        else:
            groups.append(current)
            current = [b]
    groups.append(current)
    return groups

def build_document_graph(blocks):
    if len(blocks) == 0:
        return {"nodes": [], "edges": []}
    edges = []
    avg_height = np.mean([b["height"] for b in blocks])
    vertical_threshold = avg_height * 2
    horizontal_threshold = avg_height * 4
    for i, a in enumerate(blocks):
        for j, b in enumerate(blocks):
            if i == j:
                continue
            dy = b["y"] - a["y"]
            dx = b["x"] - a["x"]
            if abs(dx) < avg_height and 0 < dy < vertical_threshold:
                edges.append({
                    "from": i,
                    "to": j,
                    "type": "vertical"
                })
            if abs(dy) < avg_height and 0 < dx < horizontal_threshold:
                edges.append({
                    "from": i,
                    "to": j,
                    "type": "horizontal"
                })
    return {
        "nodes": blocks,
        "edges": edges
    }

def run_ocr(path: str):
    img = preprocess(path)
    result = ocr.ocr(img)
    text_blocks = []
    if not result or not result[0]:
        return {
            "text_blocks": [],
            "columns": [],
            "layout": {},
            "graph": {},
            "groups": []
        }
    for line in result[0]:
        bbox = line[0]
        raw_text = line[1][0]
        confidence = float(line[1][1])
        text = normalize_text(raw_text)
        if not is_valid_text(text, confidence):
            continue
        x_coords = [p[0] for p in bbox]
        y_coords = [p[1] for p in bbox]
        block = {
            "text": text,
            "raw_text": raw_text,
            "confidence": confidence,
            "bbox": bbox,
            "x": min(x_coords),
            "y": min(y_coords),
            "width": max(x_coords) - min(x_coords),
            "height": max(y_coords) - min(y_coords)
        }
        text_blocks.append(block)
    text_blocks = sorted(
        text_blocks,
        key=lambda b: (b["y"], b["x"])
    )
    columns = segment_columns(text_blocks)["columns"]
    text_blocks = reconstruct_reading_order(columns)
    groups = group_vertical(text_blocks)
    layout = analyze_layout(text_blocks)
    graph = build_document_graph(text_blocks)
    print("\n colums:  \n",columns,"\n graph :  \n",graph,"\n layout :    \n",layout,"\ngroups:\n  ",groups)
    return {
        "text_blocks": text_blocks,
        "columns": columns,
        "groups": groups,
        "layout": layout,
        "graph": graph
    }