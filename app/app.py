from flask import Flask, jsonify, request
import base64
import os
from card_recognition_algorithm import cardRecognitionAlgorithm

app = Flask(__name__)


@app.route('/process', methods=['POST'])
def process():
    user_id = request.form['user_id']
    number_of_photos = int(request.form['number_of_photos'])

    folder_name = 'cards_from_user_' + user_id
    os.makedirs(folder_name, exist_ok=True)

    for i in range(1, number_of_photos + 1):
        image_data = request.form['image_' + str(i)]
        image = base64.b64decode(image_data)
        file_path = folder_name + '/image_' + str(i) + '.jpg'
        with open(file_path, "wb") as f:
            f.write(image)

    response_list = []

    for i in range(1, number_of_photos + 1):
        file_path = folder_name + '/image_' + str(i) + '.jpg'
        card_number, card_name = cardRecognitionAlgorithm(file_path)
        response_list.append({'card_number': card_number, 'card_name': card_name})

    detected_cards_directory = 'detectedCards'
    for file_name in os.listdir(detected_cards_directory):
        file_path = os.path.join(detected_cards_directory, file_name)
        os.remove(file_path)

    return jsonify(response_list)


if __name__ == '__main__':
    app.run()
