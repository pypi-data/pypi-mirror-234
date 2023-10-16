import cv2
import sys
import numpy as np
from pathlib import Path
from omegaconf import DictConfig, OmegaConf
import rich
from typing import Union, List, Dict, Optional
import faiss
import weakref

# ------------------------------------------
from usls.src.utils import (
	TIMER, CONSOLE, IMG_FORMAT, 
	# decode_device, DeviceKind,
	download_from_url, FEAT_WEIGHTS_URL
)

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  



class FeatureExtractor:

	def __init__(self, use_gpu=False):

		# build model
		self.weights = download_from_url(
			FEAT_WEIGHTS_URL, 
			saveout=str(ROOT / ('usls/src/.qwasdhjkaskduwbbashgd.onnx')),
			prefix='downloading nn model'
		)
		self.model = cv2.dnn.readNetFromONNX(self.weights) # build model
		# self.device = decode_device(device)
		# if self.device.type is DeviceKind.GPU:
		if use_gpu:
			# TODO:  bug may has
			self.model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
			self.model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
		# elif self.device.type is DeviceKind.CPU:
		else:
			self.model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV);
			self.model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU);
		# TODO: set model device

		self.index = faiss.IndexFlatIP(512)  # build feats lib


	def register(self, xs):
		feats = self.model(xs) 	# (n, dim)   
		self.index.add(feats)    # update index 




	@property
	def num_feats(self):
		"""number of feats"""
		return self.index.ntotal



	def __call__(self, x):
		if isinstance(x, str):
			x = cv2.imread(x)
		assert isinstance(x, np.ndarray), f"x should be np.ndarray"

		print(x.shape)

		blob = cv2.dnn.blobFromImage(x, scalefactor=1 / 255, size=(224, 224), swapRB=True)
		self.model.setInput(blob)
		y = self.model.forward()
		return y

	# def index_device_synchronized(self, *, device: Device):
	# 	'''set index to gpu devices, when do query'''
	# 	if device.type is DeviceKind.GPU:
	# 		res = faiss.StandardGpuResources()  # single GPU
	# 		self.index = faiss.index_cpu_to_gpu(res, device.id, self.index)
	# 	print(f"> Index synchronized: {device}")




# ----------------------------------------------------------------------------------------------------
def main():
	model = FeatureExtractor()


if __name__ == "__main__":
	main()


