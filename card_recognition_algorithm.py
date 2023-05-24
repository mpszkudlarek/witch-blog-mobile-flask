import os
import torch
from torchvision import transforms
from neural_network_model import NeuralNetworkModel
from class_names_reader import classNamesReader
from make_prediction import makePrediction


def cardRecognitionAlgorithm():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_state_dict = classNamesReader("class_names.txt")
    model = NeuralNetworkModel(input_shape=3,
                               hidden_units=10,
                               output_shape=len(model_state_dict)).to(device)

    custom_image_tr = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 348)),
        transforms.ToTensor()
    ])

    for fileName in os.listdir('detectedCards'):
        checkpoint = torch.load("model_trivial_11.pt")
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        makePrediction(device, model, 'detectedCards/' + fileName, model_state_dict, custom_image_tr)
    return
