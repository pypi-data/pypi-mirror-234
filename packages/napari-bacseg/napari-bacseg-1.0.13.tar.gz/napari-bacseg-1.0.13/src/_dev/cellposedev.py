# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 17:22:35 2022

@author: turnerp
"""




from cellpose import models, dynamics
import torch

model = None
gpu = False

if torch.cuda.is_available():
    gpu = True


if __name__=='__main__':

    model = models.CellposeModel(diam_mean=15,
                                 model_type="Cyto",
                                 gpu=gpu,
                                 net_avg=False)