import pytest
import os
import sys
import torch
from ultralytics import YOLO
import numpy as np
import shutil

@pytest.fixture(scope="session")
def model_path():
    """Fixture para la ruta del modelo"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yolov8s.pt')

@pytest.fixture(scope="session")
def model(model_path):
    """Fixture para cargar el modelo"""
    if not os.path.exists(model_path):
        download_path = 'yolov8s.pt'
        model = YOLO('yolov8s')
        if os.path.exists(download_path):
            shutil.move(download_path, model_path)
    return YOLO(model_path)

@pytest.fixture(scope="session")
def device():
    """Fixture para determinar el dispositivo de ejecución"""
    return 'cuda' if torch.cuda.is_available() else 'cpu'

@pytest.fixture(scope="session")
def test_image():
    """Fixture para crear una imagen de prueba"""
    return np.zeros((640, 640, 3), dtype=np.uint8)

def pytest_configure(config):
    """Setup inicial para las pruebas"""
    print("\nIniciando configuración de pruebas...")
    print(f"Dispositivo de ejecución: {'cuda' if torch.cuda.is_available() else 'cpu'}")