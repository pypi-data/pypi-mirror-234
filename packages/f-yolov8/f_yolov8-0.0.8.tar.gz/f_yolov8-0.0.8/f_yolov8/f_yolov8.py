from ultralytics.utils.plotting import Annotator, colors
from ultralytics.data.augment import LetterBox
import copy
import cv2
from PIL import Image, ImageDraw
import numpy as np
import torch

from PIL import ImageFont


def pascal2yolo(Img, Txt):
    
    # pascal2yolo는 yolov8의 탐지 결과 중 result 클래스에서 추출한 detection 결과(pascal)를 yolo format으로 변환하는 코드
    # detection 결과(pascal) format: (x1, y1, x2, y2, confidence, class)
    # yolo format : (class, confidence, x, y, w, h)
    
    _Txt = copy.deepcopy(Txt)
    m, n, k = Img.shape
    Det = np.zeros([_Txt.shape[0], _Txt.shape[1]])
    
    yolo_x, yolo_y = ((_Txt[:,2] + _Txt[:,0]) / 2 - 1) / n, ((_Txt[:,3] + _Txt[:,1]) / 2 - 1) / m
    yolo_w, yolo_h = (_Txt[:,2] - _Txt[:,0] - 2) / n, (_Txt[:,3] - _Txt[:,1] - 2) / m
    
    Det[:,0], Det[:,1] = _Txt[:,5], _Txt[:,4]
    Det[:,2], Det[:,3], Det[:,4], Det[:,5] = yolo_x, yolo_y, yolo_w, yolo_h
    
    return Det

def yolo2pascal(Img, Txt, mode='gt'):
    
    # pascal format : (class, confidence, x1, y1, x2, y2)
    # yolo format : (class, confidence, x, y, w, h)
    
    _Txt = copy.deepcopy(Txt)
    m, n, k = Img.shape
    
    if len(_Txt) > 0:
        if mode == 'gt':
            pascal_x, pascal_y = (_Txt[:,1] - _Txt[:,3]/2) * n + 1, (_Txt[:,2] - _Txt[:,4]/2) * m + 1
            pascal_w, pascal_h = (_Txt[:,1] + _Txt[:,3]/2) * n + 1, (_Txt[:,2] + _Txt[:,4]/2) * m + 1
               
            _Txt[:,1], _Txt[:,2], _Txt[:,3], _Txt[:,4] = pascal_x, pascal_y, pascal_w, pascal_h
            _Txt = _Txt.astype(int)
            
        elif mode == 'det':
            pascal_x, pascal_y = (_Txt[:,2] - _Txt[:,4]/2) * n + 1, (_Txt[:,3] - _Txt[:,5]/2) * m + 1
            pascal_w, pascal_h = (_Txt[:,2] + _Txt[:,4]/2) * n + 1, (_Txt[:,3] + _Txt[:,5]/2) * m + 1
            
            _Txt[:,2], _Txt[:,3], _Txt[:,4], _Txt[:,5] = pascal_x, pascal_y, pascal_w, pascal_h
    return _Txt

def yolodraw(Img, Result, Classes, labels=True, mode='single'):
    
    rec_th = 2
    font_th = 1
    
    if max(Img.shape[0:2]) > 1500:
        font_size = 0.6
        pol_th = 2
    elif max(Img.shape[0:2]) > 1000 and max(Img.shape[0:2]) < 1500:
        font_size = 0.4
        pol_th = 2
    elif  max(Img.shape[0:2]) < 1000:
        font_size = 0.2
        pol_th = 1
    
    _Img = copy.deepcopy(Img)
    d_img = copy.deepcopy(_Img)
    
    if mode == 'single':
        if Result['pol'] == None:
            for i in range(len(Result['class'])):
                color = colors(int(Result['class'][i]))
                cv2.rectangle(_Img, (int(Result['bbox_pascal'][i][0]), int(Result['bbox_pascal'][i][1])), (int(Result['bbox_pascal'][i][2]), int(Result['bbox_pascal'][i][3])), color, -1)
                cv2.addWeighted(_Img, 0.12, d_img, 1 - 0.12, 0, d_img)
                d_img = cv2.rectangle(d_img, (int(Result['bbox_pascal'][i][0]), int(Result['bbox_pascal'][i][1])), (int(Result['bbox_pascal'][i][2]), int(Result['bbox_pascal'][i][3])), color, rec_th)
                
            if labels == True:
                for i in range(len(Result['class'])):
                    color = colors(int(Result['class'][i]))
                    lab = Result['names'][Result['class'][i]] + '(%d):'%(int(Result['class'][i])) + '{:.2f}'.format(Result['bbox_pascal'][i][4])
                    size, baseline = cv2.getTextSize(lab, cv2.FONT_HERSHEY_SIMPLEX, font_size, 1)
                    cv2.rectangle(d_img, (int(Result['bbox_pascal'][i][0]), int(Result['bbox_pascal'][i][1])), (int(Result['bbox_pascal'][i][0]+size[0]), int(Result['bbox_pascal'][i][1]-size[1])), color, -1)
                    cv2.putText(d_img, lab, (int(Result['bbox_pascal'][i][0]), int(Result['bbox_pascal'][i][1])), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255,255,255), font_th, cv2.LINE_AA)
                    
        elif Result['pol'] != None:
            for i in range(len(Result['class'])):
                color = colors(int(Result['class'][i]))
                p = np.array(Result['pol'][i], dtype=int)
                d_img = cv2.polylines(d_img, [p], True, color, pol_th)
                
                if labels == True:
                    lab = Result['names'][Result['class'][i]] + '(%d)'%(int(Result['class'][i]))
                    size, baseline = cv2.getTextSize(lab, cv2.FONT_HERSHEY_SIMPLEX, font_size, 1)
                    cv2.rectangle(d_img, (int(Result['bbox_pascal'][i][0]), int(Result['bbox_pascal'][i][1])), (int(Result['bbox_pascal'][i][0]+size[0]), int(Result['bbox_pascal'][i][1]-size[1])), color, -1)
                    cv2.putText(d_img, lab, (int(Result['bbox_pascal'][i][0]), int(Result['bbox_pascal'][i][1])), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255,255,255), font_th, cv2.LINE_AA)

                
    elif mode == 'double':
        for i in range(len(Result['class'])):
            color = colors(int(Result['class'][i]))
            p = np.array(Result['pol'][i], dtype=int)
            cv2.fillPoly(_Img, [p], color, cv2.LINE_AA)
            cv2.addWeighted(_Img, 0.15, d_img, 1 - 0.15, 0, d_img)
            d_img = cv2.polylines(d_img, [p], True, color, pol_th)
        for i in range(len(Result['class'])):
            color = colors(int(Result['class'][i]))
            cv2.rectangle(d_img, (int(Result['bbox_pascal'][i][0]), int(Result['bbox_pascal'][i][1])), (int(Result['bbox_pascal'][i][2]), int(Result['bbox_pascal'][i][3])), color, rec_th)
            
            if labels == True:
                lab = Result['names'][Result['class'][i]] + '(%d):'%(int(Result['class'][i])) + '{:.2f}'.format(Result['bbox_pascal'][i][4])
                size, baseline = cv2.getTextSize(lab, cv2.FONT_HERSHEY_SIMPLEX, font_size, 1)
                cv2.rectangle(d_img, (int(Result['bbox_pascal'][i][0]), int(Result['bbox_pascal'][i][1])), (int(Result['bbox_pascal'][i][0]+size[0]), int(Result['bbox_pascal'][i][1]-size[1])), color, -1)
                cv2.putText(d_img, lab, (int(Result['bbox_pascal'][i][0]), int(Result['bbox_pascal'][i][1])), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255,255,255), font_th, cv2.LINE_AA)
            
    return d_img





def inference(Result):
    
    o_img = copy.deepcopy(Result.orig_img)
    conf, labels = True, True
    annotator = Annotator(copy.deepcopy(o_img))
    
    pred_boxes = Result.boxes
    names = Result.names
    Detections, Segmentations = {}, {}
    
    if Result.masks == None:
        
        
        for d in reversed(pred_boxes):
            c, conf, id = int(d.cls), float(d.conf) if conf else None, None if d.id is None else int(d.id.item())
            name = ('' if id is None else f'id:{id} ') + names[c]
            label = (f'{name} {conf:.2f}' if conf else name) if labels else None
            annotator.box_label(d.xyxy.squeeze(), label, color=colors(c, True))
        
        txt = Result.boxes.data
        txt = txt.to(torch.device('cpu')).numpy()
        
        Detections['bbox_pascal'] = txt
        Detections['names'] = names
        Detections['class'] = pred_boxes.cls.to(torch.device('cpu')).numpy()
        Detections['pol'] = None
        
        Detections['bbox_yolo'] = pascal2yolo(o_img, txt)
        
        d_img = annotator.result()
        
        return d_img, Detections
        
    elif Result.masks != None:
        pred_masks = Result.masks
        # if 'cuda' in Result.boxes.xywh.device.type:
        img = LetterBox(pred_masks.shape[1:])(image=annotator.result())
        img_gpu = torch.as_tensor(img, dtype=torch.float16, device=pred_masks.data.device).permute(
            2, 0, 1).flip(0).contiguous() / 255
        annotator.masks(pred_masks.data, colors=[colors(x, True) for x in pred_boxes.cls], im_gpu=img_gpu)
        
        txt = Result.masks.xy
        
        Segmentations['pol'] = txt
        Segmentations['names'] = names
        Segmentations['class'] = pred_boxes.cls.to(torch.device('cpu')).numpy()
        Segmentations['conf'] = pred_boxes.conf.to(torch.device('cpu')).numpy()
        Segmentations['bbox_pascal'] = Result.boxes.data.to(torch.device('cpu')).numpy()
        
        txt_yolo = pascal2yolo(o_img, Result.boxes.data.to(torch.device('cpu')).numpy())
        Segmentations['bbox_yolo'] = txt_yolo
    
        d_img = annotator.result()
    
        return d_img, Segmentations