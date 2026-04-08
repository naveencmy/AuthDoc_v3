from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="fr")


def run_ocr(image_path):
    result = ocr.ocr(image_path, cls=True)

    blocks = []

    for line in result:
        for word in line:
            box, (text, conf) = word

            x = int(box[0][0])
            y = int(box[0][1])
            w = int(box[2][0] - box[0][0])
            h = int(box[2][1] - box[0][1])

            blocks.append({
                "text": text.lower(),
                "confidence": conf,
                "x": x,
                "y": y,
                "width": w,
                "height": h
            })

    print("RAW BLOCKS:", blocks)
    return blocks