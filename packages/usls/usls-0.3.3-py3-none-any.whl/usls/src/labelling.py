import argparse
import os
import re
import cv2
import numpy as np
from tqdm import tqdm
from pathlib import Path
import sys
import shutil
import random
import time
import rich
from omegaconf import OmegaConf, DictConfig
from typing import List, Union, Dict, Optional
from enum import Enum, auto
from dataclasses import dataclass, field

from usls.src.utils import (
    Palette, IMG_FORMAT, CONSOLE, natural_sort,
    smart_path, BBox, Point, ClassesManager, ImageManager,
)


# help message
USAGE = """
    shift + 1   -> Doing detection mark task 
    shift + 2   -> Doing keypoint mark task 
    shift + 3   -> Doing segmentation mark task 
    R           -> Switch between Read mode and Mark mode

    A/D         -> Switch between images 
    W/S         -> Switch between classes
    C           -> Delete all bound bboxes & circles in current image (label file will be deleted)
    L           -> Random change class colors
    N           -> Hiding class label
    B           -> Blinking labels and bboxes
    T           -> Switch between line-width-max and line-width=1
    +           -> Increase the line width
    -           -> Decrease the line width
    I           -> Info of this image (for the purpose of no-qt)
    H           -> Help message

    (Keys're case-insensetive)

"""




class MarkerTask(Enum):
    mark_dets = 0   
    mark_kpts = auto() 
    # mark_segs = auto()
    # doodle = auto() 



class MarkerMode(Enum):
    read = 0
    mark = auto()   



@dataclass
class FeaturesMisc:
    # features misc

    # cursor
    cursor: Point = field(default_factory=Point)
    
    # det rect bbox
    rect_det: BBox = field(default_factory=BBox)

    # kpt point 
    pt_kpt: Point = field(default_factory=Point)


    # colors palette
    color_palette: Palette = field(default=Palette(shuffle=False))    

    # features
    HIDE_BBOX_LABEL: bool = False  # hide label flag
    SINGLE_CLS_INDEX: Union[int, bool, None] = None   # only show one specific class

    # bboxes blink
    DO_BLINKING: bool = False
    BLINK_OR_NOT_SWITCHER: bool = False

    # line thickness  &  line thickes adjust
    MIN_LINE_WIDTH: bool = False  # min line width
    LINE_THICKNESS: Union[bool, None, int] = 1            
    LINE_THICKNESS_ADJUST: bool = False   # line thickness adjust flag

    # show current info 
    SHOW_INFO: bool = False

    
    # previous left-button double click
    l_double_clicked_previous: bool = False   



    def auto_set_line_width(self, img_shape):
        # auto calculate line-thickness
        if self.MIN_LINE_WIDTH:
            self.LINE_THICKNESS = 1
        else:
            if not self.LINE_THICKNESS_ADJUST: 
                self.LINE_THICKNESS = max(round(sum(img_shape) / 2 * 0.003), 1)  
            else: 
                self.LINE_THICKNESS      # line width


    def line_width_recommended(self, img_shape):
        return max(round(sum(img_shape) / 2 * 0.003), 2)




class MarkerApp:
    def __init__(
        self, 
        input_,
        classes,
        kpts_classes=None,
    ):

        # mode & task
        self.mode = MarkerMode.read 
        self.task = MarkerTask.mark_dets


        # image manager
        self.dir_img = input_
        self.m_image = ImageManager()
        self.m_image.load(self.dir_img)
        self.m_image.idx = 0   # initialize the img index=0 
        print(f"> Input directory: {Path(self.dir_img).resolve()}")
        
        # class manager 
        self.m_cls = ClassesManager()
        self.m_cls.parse([self.dir_img] if classes is None else classes)
        self.m_cls.parse_kpts(kpts_classes)

        # misc manager: blink, hide label, line-thickness
        self.m_misc = FeaturesMisc()
        self.window_init()  # create window 

        # mouse listen callback
        cv2.setMouseCallback(self.window_name, self.mouse_listener)

        # mode trackbar
        self.mode_list = list(MarkerMode.__members__.keys())
        # self.trackbar_mode_name = f'Mode: {self.mode_list}'
        self.trackbar_mode_name = f'#[Read | mark]'
        cv2.createTrackbar(self.trackbar_mode_name, self.window_name, 0, len(self.mode_list) - 1, lambda _x: _x)
        
        # task trackbar
        self.task_list = list(MarkerTask.__members__.keys())
        # self.trackbar_task_name = f'Task: {self.task_list}'
        self.trackbar_task_name = f'#[Detection | Keypoint]'
        cv2.createTrackbar(self.trackbar_task_name, self.window_name, 0, len(self.task_list) - 1, lambda _x: _x)
        

        # images trackbar
        self.trackbar_image_name = '#IMAGE'
        if self.m_image.count - 1 != 0:
            cv2.createTrackbar(self.trackbar_image_name, self.window_name, 0, self.m_image.count - 1, lambda x: self.m_image.set_idx(x))   

        # class trackbar
        self.trackbar_class_name = f'#CLS: {self.m_cls.names}'
        if self.m_cls.count - 1 != 0:
            cv2.createTrackbar(self.trackbar_class_name, self.window_name, 0, self.m_cls.count - 1, lambda _x: _x)
        
        # kpts class trackbar
        self.trackbar_kpt_class_name = f'#CLS-KPT: ' 
        if kpts_classes is not None:
            self.trackbar_kpt_class_name += f'{self.m_cls.names_kpts}' 
            if self.m_cls.count_kpts - 1 != 0:
                cv2.createTrackbar(self.trackbar_kpt_class_name, self.window_name, 0, self.m_cls.count_kpts - 1, lambda _x: _x)





    def bboxes_blinking(self, img):
        # Blink bboxes
        if self.m_misc.DO_BLINKING:
            if self.m_misc.BLINK_OR_NOT_SWITCHER == False:
                img = self.draw_bboxes_from_file(
                    img=img, 
                    line_thickness=0,  # line_thickness = 0 
                )
                self.m_misc.BLINK_OR_NOT_SWITCHER = True 
            else:
                img = self.draw_bboxes_from_file(
                    img=img, 
                    line_thickness=self.m_misc.LINE_THICKNESS,  # line_thickness
                )
                self.m_misc.BLINK_OR_NOT_SWITCHER = False
        else:
            img = self.draw_bboxes_from_file(
                img=img, 
                line_thickness=self.m_misc.LINE_THICKNESS,  # line_thickness
            )
        return img



    def highlight_selected_bbox(self, img):
        # hight-light seletec bbox
        if self.m_image.has_bbox_selected:
            _bbox = self.m_image.bboxes[self.m_image.id_selected_bbox]  # selected bbox
            mask_highlight = np.zeros((img.shape), dtype=np.uint8)
            _lw = self.m_misc.LINE_THICKNESS // 2   # border
            cv2.rectangle(
                mask_highlight, 
                (_bbox.tl.x - _lw, _bbox.tl.y - _lw),
                (_bbox.br.x + _lw, _bbox.br.y + _lw), 
                (255, 255, 255, 0), 
                -1, 
                cv2.LINE_AA
            )
            img = cv2.addWeighted(img, 1, mask_highlight, 0.5, 0)
        return img



    def save_label_det(self, line):
        with open(self.m_image.path_label, 'a') as f:
            if os.path.getsize(self.m_image.path_label) == 0:
                f.write(line)
            else:
                f_r = open(self.m_image.path_label, "r").read()   # read a
                if f_r[-1] == '\n':
                    msg = line
                else:
                    msg = '\n' + line
                f.write(msg)


    def show_info_no_qt(self, img):
        # show info when has no qt supported
        if self.m_misc.SHOW_INFO:
            # msg = f'{self.m_image.idx}/{self.m_image.count - 1} | {self.m_image.path} | {self.task}'
            msg = f'{self.m_image.path}'

            # get text width, height
            text_w, text_h = cv2.getTextSize(
                msg, 0,
                fontScale=self.m_misc.LINE_THICKNESS / 4, 
                thickness=max(self.m_misc.LINE_THICKNESS - 1, 1)
            )[0]

            text_x, text_y = self.m_image.image.shape[1] // 20, self.m_image.image.shape[0] // 10
            _dealt = 10
            cv2.rectangle(
                img, 
                (max(0, text_x - _dealt), max(0, text_y - text_h - _dealt)),
                (min(text_x + text_w + _dealt, img.shape[1]), min(text_y + _dealt, img.shape[0])), 
                (0, 0, 0), 
                -1, 
                cv2.LINE_AA
            )
            cv2.putText(
                img, 
                msg, 
                (text_x, text_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                self.m_misc.LINE_THICKNESS / 4, 
                (255, 255, 255), 
                thickness=int(self.m_misc.LINE_THICKNESS * 0.7), 
                lineType=cv2.LINE_AA
            )
        return img



    def mainloop(self):
        while True:
            color = self.m_misc.color_palette(int(self.m_cls.idx), bgr=False)  # color for every class
            img_c = self.m_image.image.copy()    # current image  

            # statusbar info
            if self.with_qt:
                status_msg = (
                    f"Mode: {'Reading' if self.mode is MarkerMode.read else 'Marking'}" + "\t" * 8 + 
                    f"Task: {self.task}" + "\t" * 8 + 
                    f"Cursor: ({self.m_misc.cursor})" + "\t" * 8 + 
                    f"Num_BBoxes: {str(len(self.m_image.bboxes))}" + "\t" * 8 +
                    f"Image Resolution: ({self.m_image.height}, {self.m_image.width})" + "\t" * 5 +
                    f"Image Path: {self.m_image.path}"
                )
                cv2.displayStatusBar(self.window_name, status_msg)


            # calculate line-thickness
            self.m_misc.auto_set_line_width(img_c.shape)

            # do blinking
            if self.task is MarkerTask.mark_dets or self.task is MarkerTask.mark_kpts:
                img_c = self.bboxes_blinking(img_c)
            else:
                pass


            # doing labelling
            if self.mode is MarkerMode.mark:
                if self.task is MarkerTask.mark_dets or self.task is MarkerTask.mark_kpts:   # detection marking

                    if self.task is MarkerTask.mark_dets:
                        # show cursor line for drawing
                        cv2.line(
                            img_c, 
                            (self.m_misc.cursor.x, 0),
                            (self.m_misc.cursor.x, self.m_image.height), 
                            color, self.m_misc.LINE_THICKNESS
                        )
                        cv2.line(
                            img_c, 
                            (0, self.m_misc.cursor.y), 
                            (self.m_image.width, self.m_misc.cursor.y), 
                            color, 
                            self.m_misc.LINE_THICKNESS
                        )
                    elif self.task is MarkerTask.mark_kpts:
                        cv2.circle(
                            img_c,
                            (self.m_misc.cursor.x, self.m_misc.cursor.y),
                            int(self.m_misc.LINE_THICKNESS * 2),  # radius
                            color,
                            -1,     # filled
                        )

                    # show label or not when drawing
                    if not self.m_misc.HIDE_BBOX_LABEL:
                        self.show_objects_labels(
                            img=img_c,
                            label=self.m_cls.names[self.m_cls.idx] if self.task is MarkerTask.mark_dets else self.m_cls.names_kpts[self.m_cls.idxk],
                            line_thickness=self.m_misc.LINE_THICKNESS,
                            x=self.m_misc.cursor.x,
                            y=self.m_misc.cursor.y,                       
                            color=color,
                        )

                    # hightlight selected bbox
                    img_c = self.highlight_selected_bbox(img_c)

                    # draw and save det
                    if self.task is MarkerTask.mark_dets:
                        if self.m_misc.rect_det.tl.x != -1:   # 1st point
                            cv2.rectangle(
                                img_c, 
                                (self.m_misc.rect_det.tl.x, self.m_misc.rect_det.tl.y),
                                (self.m_misc.cursor.x, self.m_misc.cursor.y), 
                                color, 
                                self.m_misc.LINE_THICKNESS
                            )  # draw partial bbox 

                            # 2nd point checking
                            if self.m_misc.rect_det.br.x != -1:
                                
                                # save label
                                line = f'{self.m_cls.idx} ' + self.m_misc.rect_det.str_cxcywh_n(self.m_image.width, self.m_image.height)

                                self.save_label_det(line)
                                # reset
                                self.m_misc.rect_det = BBox()
                        
                # # TODO: seg task
                # elif self.task is MarkerTask.mark_segs:
                #     cv2.circle(
                #         img_c,
                #         (self.m_misc.cursor.x, self.m_misc.cursor.y),
                #         int(self.m_misc.LINE_THICKNESS * 2),  # radius
                #         color,
                #         -1,     # filled
                #     )

            
            imgc = self.show_info_no_qt(img_c)   # show info when has no QT
            cv2.imshow(self.window_name, img_c)    # current show
            self.keys_listener()   # key listening

            # if window gets closed then quit
            if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                break

        cv2.destroyAllWindows()


        # deal with wrong img: can not be opened by opencv
        if len(self.m_image.deprecated_img_set) > 0:
            print(f"> Warning: {len(self.m_image.deprecated_img_set)} images can not be decode.")
            
            # create dir
            self.dir_deprecated = "images-deprecated"
            self.dir_deprecated = smart_path(Path(self.dir_deprecated), exist_ok=False, sep='-')  # increment run
            self.dir_deprecated.mkdir(parents=True, exist_ok=True)  # make dir for every page

            # move
            for img in self.m_image.deprecated_img_set:
                shutil.move(img, str(self.dir_deprecated))
            print(f'> Deprecated images saved at: {self.dir_deprecated}')



    def show_objects_labels(
            self,
            *,
            img,
            label,
            line_thickness,
            x,
            y,
            color,
            font=cv2.FONT_HERSHEY_SIMPLEX,
            lineType=cv2.LINE_AA
        ):
        # TODO: font and text style
        # show objects labels when loaded from files and cursor line

        text_w, text_h = cv2.getTextSize(
            label,   # label
            0,
            fontScale=line_thickness / 3, 
            thickness=max(line_thickness - 1, 1)
        )[0]  # get text width, height

        # check if label is outside of image
        outside = y - text_h - 3 >= 0  
        cv2.putText(
            img, 
            label, 
            (x, y - 2 if outside else y + text_h + 5), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            line_thickness / 3, 
            color, 
            thickness=int(line_thickness * 0.7), 
            lineType=cv2.LINE_AA
        )
        return img



    def draw_bboxes_from_file(
            self, 
            *,
            img, 
            line_thickness,  # line_thickness
        ):
        # draw bboxes from label.txt
        
        height, width = img.shape[:2]   # h, w
        self.m_image.bboxes.clear()

        # Drawing bounding boxes from the files
        if Path(self.m_image.path_label).exists():
            with open(self.m_image.path_label, 'r') as f:   # read label file
                for idx, line in enumerate(f):
                    cls_id, cx, cy, box_w, box_h, *kpts_list = line.split()
                    box_w, box_h, cx, cy = map(float, (box_w, box_h, cx, cy))  # to float
                    cls_id = int(cls_id)   # to int
                    cls_name = self.m_cls.names[cls_id]  # class name

                    # coords
                    w = width * box_w
                    h = height * box_h
                    xmin = int(width * cx - w / 2.0)
                    xmax = int(width * cx + w / 2.0)   
                    ymin = int(height * cy - h / 2.0)
                    ymax = int(height * cy + h / 2.0)

                    # show single class
                    if self.m_misc.SINGLE_CLS_INDEX is not None:   
                        if cls_id != self.m_misc.SINGLE_CLS_INDEX:
                            continue    

                    color = self.m_misc.color_palette(cls_id, bgr=False)   # color palette

                    # kpts
                    kpts_ = [Point] * self.m_cls.count_kpts
                    if len(kpts_list) > 0:
                        # print(f'kpts_list: {kpts_list}')
                        step = len(kpts_list) // self.m_cls.count_kpts
                        # print(f'step: {step}')
                        assert step == 3, f'keypoint format must be like: x, y, visible(0|1)'
                        for id_, i in enumerate(range(0, len(kpts_list), step)):
                            x_, y_ = kpts_list[i], kpts_list[i+1]

                            # continue when has no kpt
                            if x_ == '-1' and y_ == '-1':
                                continue

                            x_, y_, visiable = float(x_), float(y_), float(kpts_list[i+2])
                            x_ *= width
                            y_ *= height

                            # save 
                            kpts_[id_] = Point(
                                x=x_,
                                y=y_,
                                id_=id_,
                                conf=visiable,
                            )

                            # draw
                            cv2.circle(
                                img,
                                (int(x_), int(y_)),
                                line_thickness * 2,  # radius
                                color,
                                -1,     # filled
                            )
                        
                            # Display Label if has label txt
                            if not self.m_misc.HIDE_BBOX_LABEL:
                                self.show_objects_labels(
                                    img=img,
                                    label=self.m_cls.names_kpts[id_],
                                    line_thickness=line_thickness,
                                    x=int(x_),
                                    y=int(y_),
                                    color=color,
                                )


                    # save to memory
                    self.m_image.bboxes.append(
                        BBox(
                            tl = Point(xmin, ymin),
                            br = Point(xmax, ymax),
                            id_ = cls_id,
                            kpts = kpts_ if len(kpts_) > 0 else None
                        )
                    )

                    # draw bbox
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, line_thickness, cv2.LINE_AA)  

                    # Display Label if has label txt
                    if not self.m_misc.HIDE_BBOX_LABEL:
                        self.show_objects_labels(
                            img=img,
                            label=cls_name,
                            line_thickness=line_thickness,
                            x=xmin,
                            y=ymin,
                            color=color,
                        )


        return img


    def bind_point_to_bbox(self):
        smallest_area = -1
        for idx, bbox in enumerate(self.m_image.bboxes):
            # check if cursor is in bbox
            if bbox.tl.x <= self.m_misc.cursor.x <= bbox.br.x and bbox.tl.y <= self.m_misc.cursor.y <= bbox.br.y:   
                # find smaller bbox
                if bbox.area < smallest_area or smallest_area == -1:
                    smallest_area = bbox.area
                    self.m_image.id_selected_bbox_by_pt = idx
                    self.m_image.has_bbox_bind_to_point = True



    def find_and_delete_point(self):
        # find out the point which cursor on and delete it

        # find from bbox , then its kpts
        idx_ = -1   # the bbox cursor in 
        smallest_area = -1
        for idx, bbox in enumerate(self.m_image.bboxes):
            # check if cursor is in bbox
            if bbox.tl.x <= self.m_misc.cursor.x <= bbox.br.x and bbox.tl.y <= self.m_misc.cursor.y <= bbox.br.y:   
                # find smaller bbox
                if bbox.area < smallest_area or smallest_area == -1:
                    smallest_area = bbox.area
                    idx_ = idx


        for i, kpt in enumerate(self.m_image.bboxes[idx_].kpts):
            if kpt == Point():
                continue

            _delta = 10
            if kpt.x - _delta <= self.m_misc.cursor.x <= kpt.x + _delta and kpt.y - _delta <= self.m_misc.cursor.y <= kpt.y + _delta:
                # find the kpt
                self.m_image.bboxes[idx_].kpts[i] = Point()  # delete from mem
                kpts_ = self.m_image.bboxes[self.m_image.id_selected_bbox_by_pt].kpts
                s_ = []
                for kpt in kpts_:
                    if kpt.x == -1:
                        s_.extend([-1, -1, 0])
                    else:
                        s_.extend([kpt.x / self.m_image.width, kpt.y / self.m_image.height, kpt.conf])
                line_kpt = ' '.join(map(str, s_))

                # load original label file
                with open(self.m_image.path_label, 'r') as f_original:
                    lines_original = f_original.readlines()

                # # re-write label file
                with open(self.m_image.path_label, 'w') as f:
                    for idx, line in enumerate(lines_original):
                        if idx != idx_:   # nothing changed
                            f.write(line)
                        else:
                            line_new = ' '.join(line.strip().split(' ')[:5]) + ' ' + line_kpt + '\n'
                            f.write(line_new) 


    def set_selected_bbox(self, set_cls_trackbar=True):
        # left double click in bbox => select the smallest bbox, and set that bbox

        smallest_area = -1
        for idx, bbox in enumerate(self.m_image.bboxes):
            # check if cursor is in bbox
            if bbox.tl.x <= self.m_misc.cursor.x <= bbox.br.x and bbox.tl.y <= self.m_misc.cursor.y <= bbox.br.y:   
                self.m_image.has_bbox_selected = True   # set bbox selected
                # find smaller bbox
                if bbox.area < smallest_area or smallest_area == -1:
                    smallest_area = bbox.area
                    self.m_image.id_selected_bbox = idx   # set selected bbox index
                    self.m_cls.idx = bbox.id_   # track current bbox id

                    # set class trackbar position
                    if set_cls_trackbar: 
                        cv2.setTrackbarPos(self.trackbar_class_name, self.window_name, bbox.id_)    
            


    def actions_to_selected_bbox(self, *, delete=False, change_id=False):
        # load original label file
        with open(self.m_image.path_label, 'r') as f_original:
            lines_original = f_original.readlines()

        # re-write label file
        with open(self.m_image.path_label, 'w') as f:
            for idx, line in enumerate(lines_original):
                if idx != self.m_image.id_selected_bbox:   # nothing changed
                    f.write(line)
                elif change_id is True:    # re-write line
                    line_new = str(self.m_cls.idx) + line[1:]
                    f.write(line_new)
                elif delete is True:   # skip this line
                    continue
                else:
                    pass



    def mouse_listener(self, event, x, y, flags, param):
        # mouse callbacks
        if self.mode is MarkerMode.mark:

            # mark det mode
            if self.task == MarkerTask.mark_dets:
                if event == cv2.EVENT_MOUSEMOVE:
                    self.m_misc.cursor.x = x
                    self.m_misc.cursor.y = y


                # left button double click -> select object
                elif event == cv2.EVENT_LBUTTONDBLCLK:
                    self.m_misc.l_double_clicked_previous = True    
                    self.m_misc.rect_det.tl = Point(-1, -1)   # reset top_left point

                    # if clicked inside a bounding box we set that bbox
                    self.set_selected_bbox(set_cls_trackbar=True)


                # right button pressed down
                elif event == cv2.EVENT_RBUTTONDOWN:  
                    self.set_selected_bbox(set_cls_trackbar=False)   # cancel set class
                    if self.m_image.has_bbox_selected:   # delete box when box is selected
                        self.actions_to_selected_bbox(delete=True)
                        self.m_image.has_bbox_selected = False    # mark false when box after deleted
                        

                # left button pressed down
                elif event == cv2.EVENT_LBUTTONDOWN:
                    if self.m_misc.l_double_clicked_previous:  # cancel last double click
                        self.m_misc.l_double_clicked_previous = False
                    else:  # Normal left click
                        if self.m_misc.rect_det.tl.x == -1:  # in bbox ---> set select
                            if self.m_image.has_bbox_selected:  # selected  -> de-selected
                                self.m_image.has_bbox_selected = False
                            else:  # first click
                                self.m_misc.rect_det.tl = Point(x, y)  # top-left point
                        else:  # second click
                            _threshold = 5  # minimal size for bounding box to avoid errors
                            if abs(x - self.m_misc.rect_det.tl.x) > _threshold or abs(y - self.m_misc.rect_det.tl.y) > _threshold:
                                self.m_misc.rect_det.br = Point(x, y)    # bottom-right point
            



            # TODO: mark kpt mode
            elif self.task is MarkerTask.mark_kpts:
                if event == cv2.EVENT_MOUSEMOVE:
                    self.m_misc.cursor.x = x
                    self.m_misc.cursor.y = y

                    # reset 
                    self.m_image.id_selected_bbox_by_pt = -1
                    self.m_image.has_bbox_bind_to_point = False
                    self.bind_point_to_bbox()  # bind pt to bbox


                # right button pressed down
                elif event == cv2.EVENT_RBUTTONDOWN:  
                    self.find_and_delete_point()


                # left button pressed down
                elif event == cv2.EVENT_LBUTTONDOWN:
                    if self.m_misc.l_double_clicked_previous:  # cancel last double click
                        self.m_misc.l_double_clicked_previous = False
                    else:  # Normal left click
                        self.m_misc.pt_kpt = Point(
                            x=x,
                            y=y,
                            conf=1.0,
                            id_=self.m_cls._idxk
                        )
                        if self.m_image.has_bbox_bind_to_point == True:
                            if self.m_image.bboxes[self.m_image.id_selected_bbox_by_pt].tl.x <= self.m_misc.cursor.x <= self.m_image.bboxes[self.m_image.id_selected_bbox_by_pt].br.x and \
                                self.m_image.bboxes[self.m_image.id_selected_bbox_by_pt].tl.y <= self.m_misc.cursor.y <= self.m_image.bboxes[self.m_image.id_selected_bbox_by_pt].br.y:

                                # init when not exists
                                if self.m_image.bboxes[self.m_image.id_selected_bbox_by_pt].kpts == None:
                                    self.m_image.bboxes[self.m_image.id_selected_bbox_by_pt].kpts = [Point] * self.m_cls.count_kpts

                                # put current kpt into bbox binged
                                self.m_image.bboxes[self.m_image.id_selected_bbox_by_pt].kpts[self.m_cls._idxk] = self.m_misc.pt_kpt

                                # kpts in bbox
                                kpts_ = self.m_image.bboxes[self.m_image.id_selected_bbox_by_pt].kpts
                                s_ = []
                                for kpt in kpts_:
                                    if kpt.x == -1:
                                        s_.extend([-1, -1, 0])
                                    else:
                                        s_.extend([kpt.x / self.m_image.width, kpt.y / self.m_image.height, kpt.conf])
                                line_kpt = ' '.join(map(str, s_))

                                # find the label of bbox line need to modify 
                                # load original label file
                                with open(self.m_image.path_label, 'r') as f_original:
                                    lines_original = f_original.readlines()

                                # # re-write label file
                                with open(self.m_image.path_label, 'w') as f:
                                    for idx, line in enumerate(lines_original):
                                        if idx != self.m_image.id_selected_bbox_by_pt:   # nothing changed
                                            f.write(line)
                                        else:
                                            # id, x, y, w, h, 
                                            line_new = ' '.join(line.strip().split(' ')[:5]) + ' ' + line_kpt + '\n'
                                            f.write(line_new) 

                                # reset
                                self.m_image.has_bbox_bind_to_point == False


            # # TODO: mark seg mode
            # elif self.task is MarkerTask.mark_segs:
            #     if event == cv2.EVENT_MOUSEMOVE:
            #         self.m_misc.cursor.x = x
            #         self.m_misc.cursor.y = y


        else:
            pass


    def keys_listener(self, delay=1):
        # ---------------- Key Listeners ------------------------
        pressed_key = cv2.waitKey(delay)

        # h/H -> help 
        if pressed_key in (ord('h'), ord('H')):
            print(f'\nUSAGE:\n{USAGE}\n')


        # tasks
        elif pressed_key == 33:  # !, shift + 1
            self.task = MarkerTask.mark_dets
            cv2.setTrackbarPos(self.trackbar_task_name, self.window_name, self.task.value)  # update  trackbar 

        elif pressed_key == 64:   # @, shift + 2
            if self.m_cls.count_kpts <= 0:
                self.task = MarkerTask.mark_dets
                print(f'Warning: No `-kc` named, can not switch to `MarkerTask.mark_kpts`')
            else:
                self.task = MarkerTask.mark_kpts
                cv2.setTrackbarPos(self.trackbar_task_name, self.window_name, self.task.value)  # update  trackbar 


        # elif pressed_key == 35:
        #     # mark seg  => #
        #     self.task = MarkerTask.mark_segs
        #     cv2.setTrackbarPos(self.trackbar_task_name, self.window_name, self.task.value)  # update  trackbar 
            # print(f'> Task: {self.task}')


        # -----------------------------------------------------
        # r/R  =>  switch between mark and read mode
        # -----------------------------------------------------
        elif pressed_key in (ord('r'), ord('R')):
            if self.with_qt:
                cv2.displayOverlay(self.window_name, f"Switch between READ and MARK", 800)

            if self.mode is MarkerMode.read:
                self.mode = MarkerMode.mark
            elif self.mode is MarkerMode.mark:
                self.mode = MarkerMode.read
            
            cv2.setTrackbarPos(self.trackbar_mode_name, self.window_name, self.mode.value)  # update  trackbar 


        # ---------------------------------------
        # a,d -> images [previous, next]
        # ---------------------------------------
        elif pressed_key in (ord('a'), ord('A'), ord('d'), ord('D')):
            if not self.m_image.has_bbox_selected:
                if pressed_key in (ord('a'), ord('A')):     
                    self.m_image.to_next()

                elif pressed_key in (ord('d'), ord('D')):
                    self.m_image.to_last()

                # if self.with_qt:
                cv2.setTrackbarPos(self.trackbar_image_name, self.window_name, self.m_image.idx)  # update img trackbar 
                
                # set the adjust flag False
                self.m_misc.LINE_THICKNESS_ADJUST = False    

        

        # ---------------------------------------
        # w,s -> class  [previous, next]
        # ---------------------------------------
        elif pressed_key in (ord('s'), ord('S'), ord('w'), ord('W')):

            if pressed_key in (ord('s'), ord('S')):
                if self.task is MarkerTask.mark_dets:
                    self.m_cls.to_next()
                elif self.task is MarkerTask.mark_kpts:
                    self.m_cls.to_next_kpt()

            elif pressed_key in (ord('w'), ord('W')):
                if self.task is MarkerTask.mark_dets:
                    self.m_cls.to_last()
                elif self.task is MarkerTask.mark_kpts:
                    self.m_cls.to_last_kpt()


            # update class trackbar                
            # if self.with_qt:
            if self.task is MarkerTask.mark_dets:
                cv2.setTrackbarPos(self.trackbar_class_name, self.window_name, self.m_cls.idx)
            elif self.task is MarkerTask.mark_kpts:
                cv2.setTrackbarPos(self.trackbar_kpt_class_name, self.window_name, self.m_cls.idxk)


            # TODO: kpt select
            # when select, use W/S to change bbox's class
            if self.m_image.has_bbox_selected:
                self.actions_to_selected_bbox(change_id=True)


        # ---------------------------------------
        # n/N => hide label
        # ---------------------------------------
        elif pressed_key in (ord('n'), ord('N')):
            self.m_misc.HIDE_BBOX_LABEL = not self.m_misc.HIDE_BBOX_LABEL

            if self.with_qt:
                cv2.displayOverlay(self.window_name, 'Press N to hide or show class.', 800)

        # ---------------------------------------
        # '+-' => adjust line thickness
        # ---------------------------------------
        elif pressed_key in (ord('='), ord('+')):
            self.m_misc.LINE_THICKNESS_ADJUST = True   # set the adjust flag TRUE
            
            # increate the line width
            if self.m_misc.LINE_THICKNESS <= self.m_misc.line_width_recommended(self.m_image.image.shape) + 10:   # MAX LINE WIDTH
                self.m_misc.LINE_THICKNESS += 1
                if self.with_qt:
                    cv2.displayOverlay(self.window_name, f'Line Thickness +1, now = {self.m_misc.LINE_THICKNESS}', 800)
            else:
                if self.with_qt:
                    cv2.displayOverlay(self.window_name, 'Line Thickness has reach the max value!', 800)

        elif pressed_key in (ord('-'), ord('_')):
            self.m_misc.LINE_THICKNESS_ADJUST = True
            min_t = 1
            if self.m_misc.LINE_THICKNESS > min_t:
                self.m_misc.LINE_THICKNESS -= 1
                if self.with_qt:
                    cv2.displayOverlay(self.window_name, f'Line Thickness -1, now = {self.m_misc.LINE_THICKNESS}', 800)
            else: 
                if self.with_qt:
                    cv2.displayOverlay(self.window_name, 'Line Thickness has reach the min value!', 800)


        # ---------------------------------------
        # i/I => display the info in this img(size, path, num_bboxes)
        # ---------------------------------------
        elif pressed_key in (ord('i'), ord('I')):
            self.m_misc.SHOW_INFO = not self.m_misc.SHOW_INFO


        # ---------------------------------------
        # b/b => blink bboxes in current img
        # ---------------------------------------
        elif pressed_key in (ord('b'), ord('B')):
            self.m_misc.DO_BLINKING = not self.m_misc.DO_BLINKING


        # ---------------------------------------
        # c/C  =>  Remove all bboxes in this img, 
        # specifically, delete the annotation file(.txt)
        # ---------------------------------------
        elif pressed_key in (ord('c'), ord('C')):
            if not self.m_image.has_bbox_selected:
                if self.with_qt:
                    cv2.displayOverlay(self.window_name, f"{len(self.m_image.bboxes)} bboxes deleted, unrecoverable!", 800)
                
                if Path(self.m_image.path_label).exists():
                    Path(self.m_image.path_label).unlink()
                else:
                    if self.with_qt:
                        cv2.displayOverlay(self.window_name, f"No bboxes found in this img!", 800)



        # ---------------------------------------
        # l/L  =>  shuffle bbox color
        # ---------------------------------------
        elif pressed_key in (ord('l'), ord('L')):
            self.m_misc.color_palette = Palette(shuffle=True)

            if self.with_qt:
                cv2.displayOverlay(self.window_name, f"Palette palette shuffled!", 800)


        # ---------------------------------------
        # t/T  =>  min line width
        # ---------------------------------------
        elif pressed_key in (ord('t'), ord('T')):
            self.m_misc.MIN_LINE_WIDTH = not self.m_misc.MIN_LINE_WIDTH


        # ---------------------------------------
        # 0-8 -> select to show single class
        # 9 -> show all
        # ---------------------------------------
        elif pressed_key in range(48, 57):  # 0-8 => 48-56
            value = int(chr(pressed_key))
            if value <= self.m_cls.count - 1:
                self.m_misc.SINGLE_CLS_INDEX = value
                if self.with_qt:
                    cv2.displayOverlay(self.window_name, f"Only show class: {self.m_misc.SINGLE_CLS_INDEX} => {self.m_cls.names[self.m_misc.SINGLE_CLS_INDEX]}", 1000)
            else:
                self.m_misc.SINGLE_CLS_INDEX = None
                
                if self.with_qt:
                    cv2.displayOverlay(
                        self.window_name, 
                        f"No class: {value}, Max class is {self.m_cls.count - 1} => {self.m_cls.names[self.m_cls.count - 1]}. Show All bboxes",
                        800
                    )


        elif pressed_key == 57:  # 9
            self.m_misc.SINGLE_CLS_INDEX = None


        # -----------------------------
        # ESC -> quit key listener
        # -----------------------------
        # elif pressed_key == 27:
        #     cv2.destroyAllWindows()




    def window_init(self):
        try:
            cv2.namedWindow('Test')   
            cv2.displayOverlay('Test', 'Test', 1)  
            cv2.displayStatusBar('Test', 'Test', 1)
            self.with_qt = True
            # print("> Using Qt.")
        except cv2.error as e:
            # print(f"> QT is not supported! Add --no-qt (no trackbar, statusbar, overlay)")
            self.with_qt = False
            print("> Not using Qt, press [h/H] for more help")
        cv2.destroyAllWindows()

        self.window_name = 'usls image marker'
        self.window_width, self.window_height = 800, 600
        # cv2.WINDOW_FREERATIO   cv2.WINDOW_KEEPRATIO, WINDOW_GUI_NORMAL, WINDOW_GUI_EXPANDED, cv2.WINDOW_NORMAL
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL) 
        cv2.resizeWindow(self.window_name, self.window_width, self.window_height)





def run_marker(args: DictConfig):

    marker = MarkerApp(
        input_=args.input, 
        classes=args.classes,
        kpts_classes=args.kpts_classes,
        # no_qt=args.no_qt,
    )

    with CONSOLE.status(f"[cyan]Marking...") as status:
        marker.mainloop()
