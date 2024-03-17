# -*- coding: utf-8 -*-
"""long/short_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GUVGM61TllTg8Y_Jhh1s_sX-uGxtJE5n
"""

from PIL import Image
import torchvision.transforms as transforms
import torch
import torchvision.models as models
import torch.nn as nn

def predict_class(image_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    image = Image.open(image_path)

    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    # 저장한 모델 불러오기
    loaded_model = models.resnet18(pretrained=False)
    loaded_model.fc = nn.Linear(loaded_model.fc.in_features, 6)
    loaded_model = loaded_model.to(device)

    loaded_model.load_state_dict(torch.load('C:/Users/kate2/PycharmProjects/DressMeUp-CV/flask/long_short_classification.pth', map_location=device))
    loaded_model.eval()

    input_batch = input_batch.to(device)

    with torch.no_grad():
        output = loaded_model(input_batch)

    _, predicted_class = torch.max(output, 1)
    predicted_class_index = predicted_class.item()
    return predicted_class_index