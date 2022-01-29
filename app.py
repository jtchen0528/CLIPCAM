import clip_modified
import torch
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import patches as mtp_ptch
from torchvision import transforms
from tqdm.notebook import tqdm
import argparse
import cv2
import pandas as pd
import json
import sys

from utils.model import getCLIP, getCAM
from utils.preprocess import getImageTranform
from utils.dataset import DirDataset
from utils.imagenet_utils import *
from utils.evaluation_tools import *
from utils.preprocess import getAttacker
from utils.grid_utils import *

parser = argparse.ArgumentParser()
parser.add_argument("--clip_model_name", type=str,
                    default='ViT-B/16', help="Model name of CLIP")
parser.add_argument("--cam_model_name", type=str,
                    default='GradCAM', help="Model name of GradCAM")
parser.add_argument("--attack", type=str, default=None,
                    help="attack type: \"snow\", \"fog\"")
args = parser.parse_args()

GPU_ID = 'cpu'
CLIP_MODEL_NAME = args.clip_model_name
CAM_MODEL_NAME = args.cam_model_name
RESIZE = 1
ATTACK = args.attack
DISTILL_NUM = 0


ImageTransform = getImageTranform(resize=RESIZE)
originalTransform = getImageTranform(resize=RESIZE, normalized=False)

def api(CLIP_MODEL_NAME, CAM_MODEL_NAME, image_path, sentence):
    model, target_layer, reshape_transform = getCLIP(
        model_name=CLIP_MODEL_NAME, gpu_id=GPU_ID)

    cam = getCAM(model_name=CAM_MODEL_NAME, model=model, target_layer=target_layer,
                gpu_id=GPU_ID, reshape_transform=reshape_transform)

    MASK_THRESHOLD = get_mask_threshold(CLIP_MODEL_NAME)

    if len(image_path) == 4:
        final_img = get_clipcam_grid(cam, model, MASK_THRESHOLD, image_path, sentence)
    elif len(image_path) == 1:
        final_img = get_clipcam_single(cam, model, MASK_THRESHOLD, image_path[0], sentence)
    
    final_img.save('img.png')

    del model
    del cam

def get_mask_threshold(CLIP_MODEL_NAME):
    if CLIP_MODEL_NAME == 'RN50':
        MASK_THRESHOLD = 0.2
    if CLIP_MODEL_NAME == 'RN101':
        MASK_THRESHOLD = 0.2
    if CLIP_MODEL_NAME == 'ViT-B/16':
        MASK_THRESHOLD = 0.3
    if CLIP_MODEL_NAME == 'ViT-B/32':
        MASK_THRESHOLD = 0.3
    return MASK_THRESHOLD

def get_clipcam_single(clipcam, model, MASK_THRESHOLD, image_path, sentence = None, DISTILL_NUM = 0, ATTACK = None):
    image = Image.open(image_path)
    orig_image = image
    if ATTACK is not None:
        image = image.resize((224, 224))
        image = getAttacker(image, type=ATTACK, gpu_id=GPU_ID)
    image = ImageTransform(image)
    orig_image = originalTransform(orig_image)
    image = image.unsqueeze(0)
    image = image.to(GPU_ID)
    orig_image = orig_image.to(GPU_ID)
    
    if sentence == None:
        sentence = input(f"Please enter the query sentence: ")

    text  = clip_modified.tokenize(sentence)
    text = text.to(GPU_ID)
    text_features = model.encode_text(text)
    grayscale_cam = clipcam(input_tensor=image, text_tensor=text_features)[0, :]
    grayscale_cam_total = grayscale_cam[np.newaxis, :]
    if DISTILL_NUM > 0:
        for distill in range(DISTILL_NUM):
            distill_mask = np.where(grayscale_cam > 0.5, 0, 1)
            distill_mask = torch.tensor(distill_mask).unsqueeze(0)
            distill_mask = torch.cat((distill_mask,distill_mask,distill_mask)).unsqueeze(0)
            distill_mask = distill_mask.to(GPU_ID)
            image = image * distill_mask
            grayscale_cam = clipcam(input_tensor=image, text_tensor=text_features)[0, :]
            grayscale_cam_total += grayscale_cam
        grayscale_cam = (grayscale_cam_total / np.max(grayscale_cam_total))[0, :]
    grayscale_cam_mask = np.where(grayscale_cam_total < MASK_THRESHOLD, 0, 1)
    pred_bbox, pred_mask = MaskToBBox(grayscale_cam_mask, 1)
    final_img = getHeatMapOneBBox(grayscale_cam, orig_image.permute(1, 2, 0).cpu().numpy(), pred_bbox, sentence)
    return final_img

def get_clipcam_grid(clipcam, model, MASK_THRESHOLD, image_paths, sentence = None, DISTILL_NUM = 0, ATTACK = None):
    grid = []
    for i in range(4):
        image = Image.open(image_paths[i])
        image = image.resize((224, 224))
        grid.append(image)
        
    img_grid = get_concat(grid[0], grid[1], grid[2], grid[3])
    image = img_grid.resize((224, 224))

    orig_image = image
    if ATTACK is not None:
        image = image.resize((224, 224))
        image = getAttacker(image, type=ATTACK, gpu_id=GPU_ID)

    image = ImageTransform(image)
    orig_image = originalTransform(orig_image)
    image = image.unsqueeze(0)
    image = image.to(GPU_ID)
    orig_image = orig_image.to(GPU_ID)
    
    if sentence == None:
        sentence = input(f"Please enter the query sentence: ")

    text  = clip_modified.tokenize(sentence)
    text = text.to(GPU_ID)
    text_features = model.encode_text(text)
    grayscale_cam = clipcam(input_tensor=image, text_tensor=text_features)[0, :]
    grayscale_cam_total = grayscale_cam[np.newaxis, :]
    if DISTILL_NUM > 0:
        for distill in range(DISTILL_NUM):
            distill_mask = np.where(grayscale_cam > 0.5, 0, 1)
            distill_mask = torch.tensor(distill_mask).unsqueeze(0)
            distill_mask = torch.cat((distill_mask,distill_mask,distill_mask)).unsqueeze(0)
            distill_mask = distill_mask.to(GPU_ID)
            image = image * distill_mask
            grayscale_cam = clipcam(input_tensor=image, text_tensor=text_features)[0, :]
            grayscale_cam_total += grayscale_cam
        grayscale_cam = (grayscale_cam_total / np.max(grayscale_cam_total))[0, :]
    grayscale_cam = grayscale_cam_total[0, :]
    grayscale_cam_mask = np.where(grayscale_cam < MASK_THRESHOLD, 0, 1)
    circular_mask = create_circular_mask(h=224, w=224, radius=30)
    grayscale_cam_mask = np.where(circular_mask > 0, 0, grayscale_cam_mask)
    grayscale_cam_img = Image.fromarray(
        (grayscale_cam_mask * 255).astype(np.uint8)).convert('L')

    grayscale_cam_img = grayscale_cam_img.resize((448, 448))
    # grayscale_cam_img.save(os.path.join(SAVE_DIR, str(total_count) + '_graycam.png'))
    grayscale_cam_np = (np.array(grayscale_cam_img) / 255).astype(np.uint8)
    total_pred_mask, total_bboxes = get_4_bbox(grayscale_cam_np)

    final_img = getHeatMapOneBBox(grayscale_cam, orig_image.permute(1, 2, 0).cpu().numpy(), total_bboxes, sentence, size=448)
    return final_img

api('ViT-B/16', 'GradCAM', ['test_img.jpg', 'test_img.jpg', 'test_img.jpg', 'test_img.jpg'], 'white trunks')
api('ViT-B/32', 'GradCAM', ['test_img.jpg'], 'white trunks')