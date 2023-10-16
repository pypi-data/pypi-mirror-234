import cv2
from pathlib import Path
import shutil
import argparse
import uuid
import urllib.request
import os
from tqdm import tqdm
import sys
import random
import time
import glob
import re
import rich
from rich.console import Console
from datetime import datetime
import contextlib
import numpy as np
from typing import Union, List, Dict, Optional, Any
from PIL import ExifTags, Image, ImageOps
from enum import Enum, auto, unique
from dataclasses import dataclass, field
import hashlib
import time
# from loguru import logger as LOGGER
# LOGGER.configure(
#     handlers=[
#         dict(sink=sys.stdout, format="[{time:MM-DD HH:mm:ss}] [{level}] --> {message}", level="DEBUG"),
#         # dict(sink="file.log", enqueue=True, serialize=True),
#     ],
#     # levels=[dict(name="NEW", no=13, icon="¤", color="")],
#     # extra={"common_to_all": "default"},
#     # patcher=lambda record: record["extra"].update(some_value=42),
#     # activation=[("my_module.secret", False), ("another_library.module", True)],
# )




CONSOLE = Console()
IMG_FORMAT = ('.jpg', '.jpeg', '.png', '.bmp')
LABEL_FORMAT = ('.txt', '.xml', '.yaml', '.csv')
VIDEO_FORMAT = ('.mp4', '.flv', '.avi', '.mov')
STREAM_FORMAT = ('rtsp://', 'rtmp://', 'http://', 'https://')
FEAT_WEIGHTS_URL = 'https://github.com/jamjamjon/assets/releases/download/usls/fe-224.onnx'
ASCII_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
EMOJIS ="🍇🍈🍉🍊🍋🍌🍍🥭🍎🍏🍐🍑🍒🍓🫐🥝🍅🫒🥥🥑🍆🥔🥕🌽🌶️🫑🥒🥬🥦🧄🧅🍄🥜🌰🍞🥐🥖🫓🥨 \
	🥯🥞🧇🧀🍖🍗🥩🥓🍔🍟🍕🌭🥪🌮🌯🫔🥙🧆🥚🍳🥘🍲🫕🥣🥗🍿🧈🧂🥫🍱🍘🍙🍚🍛🍜🍝🍠🍢🍣' \
	🍤🍥🥮🍡🥟🥠🥡🦪🍦🍧🍨🍩🍪🎂🍰🧁🥧🍫🍬🍭🍮🍯🍼🥛☕🫖🍵🍶🍾🍷🍸🍹🍺🍻🥂🥃🥤🧋🧃🧉\
	🧊🥢💥💫💦💨🐵🐒🦍🦧🐶🐕🦮🐕‍🦺🐩🐺🦊🦝🐱🐈🐈‍⬛🦁🐯🐅🐆🐴🐎🦄🦓🦌🦬🐮🐂🐃🐄🐷🐖🐗🐽🐏\
	🐨🐼🦥🦦🦨🦘🦡🐾🦃🐔🐓🐣🐤🐥🐦🐧🕊️🦅🦆🦢🦉🦤🪶🦩🦚🦜🐸🐊🐢🦎🐍🐲🐉🦕🦖🐳🐋🐬🦭🐟\
	🐠🐡🦈🐙🐚🐌🦋🐛🐜🐝🪲🐞🦗🪳🕷️🕸️🦂🦟🪰🪱🦠💐🌸💮🏵️🌹🥀🌺🌻🌼🌷🌱🪴🌲🌳🌴🌵🌾🌿☘️\
	🍀🍁🍂🍃🍄🌰🦀🦞🦐🦑🌍🌎🌏🌐🪨🌑🌒🌓🌔🌕🌖🌗🌘🌙🌚🌛🌜☀️🌝🌞⭐🌟🌠☁️⛅⛈️🌤️🌥️🌦️🌧️\
	🌨️🌩️🌪️🌫️🌬️🌈☂️☔⚡❄️☃️⛄☄️🔥💧🌊🎄✨🎋🎍😀😃😄😁😆😅🤣😂🙂🙃😉😊😇🥰😍🤩😘😗☺️😚😙🥲\
	😋😛😜🤪😝🤑🤗🤭🤫🤔🤐🤨😐😑😶😏😒🙄😬🤥😌😔😪🤤😴😷🤒🤕🤢🤮🤧🥵🥶🥴😵🤯🤠🥳🥸😎🤓\
	🧐😕😟🙁☹️😮😯😲😳🥺😦😧😨😰😥😢😭😱😖😣😞😓😩😫🥱😤😡😠🤬😈👿💀☠️💩🤡👹👺👻👽👾🤖\
	😺😸😹😻😼😽🙀😿😾💋👋🤚🖐️✋🖖👌🤌🤏✌️🤞🤟🤘🤙👈👉👆🖕👇☝️👍👎✊👊🤛🤜👏🙌👐🤲🤝🙏\
	✍️💅🤳💪🦾🦿🦵🦶👂🦻👃🧠🫀🫁🦷🦴👀👁️👅👄👶🧒👦👧🧑👱👨🧔👨‍🦰👨‍🦱👨‍🦳👨‍🦲👩👩‍🦰🧑‍🦰👩‍🦱🧑‍🦱👩‍🦳🧑‍🦳👩‍🦲🧑‍🦲\
	🧑‍🏫👨‍🏫👩‍🏫🧑‍⚖️👨‍⚖️👩‍⚖️🧑‍🌾👨‍🌾👩‍🌾🧑‍🍳👨‍🍳👩‍🍳🧑‍🔧👨‍🔧👩‍🔧🧑‍🏭👨‍🏭👩‍🏭🧑‍💼👨‍💼👩‍💼🧑‍🔬👨‍🔬👩‍🔬🧑‍💻👨‍💻👩‍💻🧑‍🎤👨‍🎤👩‍🎤🧑‍🎨👨‍🎨👩‍🎨🧑‍✈️👨‍✈️👩‍✈️🧑‍🚀👨‍🚀👩‍🚀🧑‍🚒👨‍🚒\
	🦼🛢️🛎️🧳⌛⏳⌚⏰⏱️⏲️🕰️🌡️⛱️🧨🎈🎉🎊🎎🎏🎐🧧🎀🎁🤿🪀🪁🔮🪄🧿🕹️🧸🪅🪆🖼️🧵🪡🧶🪢🛍️📿💎\
	🔴🟠🟡🟢🔵🟣🟤⚫⚪🟥🟧🟨🟩🟦🟪🟫⬛⬜\
"




@dataclass
class Point:
    x: Union[int, float] = -1
    y: Union[int, float] = -1
    z: Union[int, float] = -1
    conf: Optional[float] = None
    id_: Optional[int] = None



@dataclass
class BBox:
    tl: Point = field(default_factory=Point)   # top-left point 
    br: Point = field(default_factory=Point)    # bottom-right point
    id_: Optional[int] = None   # class id
    conf_: Union[int, float, None] = None   # score & conf
    cxcy: Point = field(default_factory=Point)  # center-xy point, optional
    kpts: Optional[List[Point]] = None # field(default_factory=list)   # kpts binds to bbox

    def init_kpts(self, x):
        self.kpts = [Point] * x

    @property
    def id(self):
        return self.id_

    @id.setter
    def id(self, x):
        self.id_ = x

    @property
    def conf(self):
        return self.conf

    @conf.setter
    def conf(self, x):
        self.conf_ = x


    @property
    def height(self):
        return self.br.y - self.tl.y


    @property
    def width(self):
        return self.br.x - self.tl.x


    @property
    def area(self):
        return (self.br.y - self.tl.y) * (self.br.x - self.tl.x)



    def str_cxcywh_n(
            self, 
            img_w, 
            img_h, 
            eps=1e-8
        ):
    	# return str of cxcywh normalized

        # boundary check and rectify
        self.tl.x = min(max(eps, self.tl.x), img_w - eps) 
        self.br.x = min(max(eps, self.br.x), img_w - eps) 
        self.tl.y = min(max(eps, self.tl.y), img_h - eps) 
        self.br.y = min(max(eps, self.br.y), img_h - eps)


        # convert
        cx = float((self.tl.x + self.br.x) / (2.0 * img_w) )
        cy = float((self.tl.y + self.br.y) / (2.0 * img_h))
        w = float(abs(self.br.x - self.tl.x)) / img_w
        h = float(abs(self.br.y - self.tl.y)) / img_h

        # double check of boundary
        if not all([0 <= x <= 1 for x in [cx, cy, w, h]]):
            sys.exit(f"Wrong coordination -> cx: {cx}, cy: {cy}, w: {w}, h: {h}.")

        items = map(str, [cx, cy, w, h])
        return ' '.join(items)



    # @cxcy.setter
    # def cxcy(self, x):
    #     self.cxcy = x


    # @property
    # def tlbr(self):
    #     pass

    # @property
    # def tlbrs(self):
    #     pass


    # @property
    # def tlwh(self):
    #     pass


    # @property
    # def tlwhs(self):
    #     pass


    # @property
    # def cxywh(self):
    #     pass


    # @property
    # def cxywhs(self):
    #     pass




@dataclass
class ImageManager:
    _idx: int = 0
    paths: Optional[List[str]] = None   # image path list
    # images_nd: Optional[List[np.ndarray]] = None  # image ndarray list
    # objects: Optional[List] = None

    image: np.ndarray = None   # image current
    bboxes: List[BBox] = field(default_factory=list)   # saving det-bboxs of current image 
    id_selected_bbox: int = -1  # id of selected box in bboxes 
    has_bbox_selected: bool = False  # has any bbox been selected
    # has_bbox_point_tl_selected: bool = False  # has any bbox point been selected
    # has_bbox_point_br_selected: bool = False  # has any bbox point been selected
    deprecated_img_set: set = field(default_factory=set)    # save precatec images
    id_selected_bbox_by_pt: int = -1  # id of selected box in bboxes bind to point
    has_bbox_bind_to_point: bool = False  # has any bbox been bind to point



    @property
    def bbox_selected(self):
    	return self.bboxes[self.id_selected_bbox]

    def set_idx(self, x):
        self.idx = x

    def to_next(self):
        self.idx = 0 if self.idx - 1 < 0 else self.idx - 1


    def to_last(self):
        self.idx = self.count - 1 if self.idx + 1 > self.count - 1 else self.idx + 1


    @property
    def path(self) -> str:
        # current image path
        return self.paths[self._idx]


    @property
    def path_label(self):
        # corresponding label path
        return Path(self.path).with_suffix('.txt')


    @property
    def height(self) -> Union[int, float, None]:
        return None if self.image is None else self.image.shape[0]


    @property
    def width(self) -> Union[int, float, None]:
        return None if self.image is None else self.image.shape[1]


    @property
    def count(self):
        return len(self.paths) 


    @property
    def idx(self):
        return self._idx


    @idx.setter
    def idx(self, x):
        self._idx = x

        # set image_np at the same time
        self.image = cv2.imread(self.paths[self.idx])
        if self.image is None:
            self.image = np.ones((800, 600, 3))  # create a empty img

            # put notification on it
            cv2.putText(
                self.image, 
                "Deprecated image!", 
                (10, self.image.shape[0]//2), 
                cv2.FONT_HERSHEY_SIMPLEX,
                1, 
                (0,0,0), 
                thickness=2, 
                lineType=cv2.LINE_AA
            )

            # TODO
            # # save wrong images path, delete all these image at the end of the program
            # self.deprecated_img_set.add(p)
            self.deprecated_img_set.add(self.paths[self.idx])


    def load(self, d):
        # load images from directory

        self.paths = [str(x) for x in Path(d).iterdir() if x.suffix.lower() in IMG_FORMAT]
        if len(self.paths) < 1:
            sys.exit(f'> No images found. Go checking the directory: {path(d).resolve()}')



@dataclass
class ClassesManager:
    names: Optional[List] = None
    names_kpts: Optional[List] = None
    _idx: int = 0
    _idxk: int = 0

    def parse(self, x: List[str]):
        # from list => txt; yaml; array/list
        # from labels dir => read all *.txt and calculate the max one for 
        s = ''
        auto_parse = False
        if len(x) == 1:
            if x[0].endswith('.txt'):   # .txt name file
                with open(x, 'r') as f:
                    for line in f:
                        self.names.append(line.strip())

            elif x[0].endswith('.yaml') or x[0].endswith('.yml'):  # .yaml name file
                # TODO: format not fixed
                pass
            elif Path(x[0]).is_dir():   # auto setting classes from labels directory
                s = '(Auto parsing)'
                auto_parse = True
                _max = 0
                for p in Path(x[0]).rglob('*.txt'):
                    with open(p, 'r') as f:
                        for line in f:
                            _max = max(int(line.strip().split(' ')[0]), _max)
                self.names = [str(x) for x in range(_max + 1)]

            else:
                self.names = x
        else: 
            self.names = x


        # duplicates checking
        if len(self.names) == len(set(self.names)):
            print(f'> Class names: {self.names} {s}')
        else:
            s_error = f'> Error: [--classes] | [-c] has duplicates: {self.names}'
            sys.exit(s_error)

        # may add new class
        # # check if match auto parse
        # if not auto_parse:
        #     _max = 0
        #     for p in Path(x[0]).rglob('*.txt'):
        #         with open(p, 'r') as f:
        #             for line in f:
        #                 _max = max(int(line.strip().split(' ')[0]), _max)

        #     # check if match
        #     if _max != len(self.names):
        #         s_error = f'> Error: number of classes does not match! Supposed: {_max}, In fact:{self.names}, '
        #         sys.exit(s_error)








    def parse_kpts(self, x: List[str]):
        # TODO: auto parsing
        self.names_kpts = x
        print(f'> Classes-kpts: {self.names_kpts}')






    def to_next(self):
        self.idx = self.count - 1 if self.idx - 1 < 0 else self.idx - 1


    def to_last(self):
        self.idx = 0 if self.idx + 1 > self.count - 1 else self.idx + 1


    def to_next_kpt(self):
        self.idxk = self.count_kpts - 1 if self.idxk - 1 < 0 else self.idxk - 1


    def to_last_kpt(self):
        self.idxk = 0 if self.idxk + 1 > self.count_kpts - 1 else self.idxk + 1




    @property
    def count(self):
        return len(self.names) 


    @property
    def count_kpts(self):
        return len(self.names_kpts) if self.names_kpts is not None else 0



    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, x):
        self._idx = x


    @property
    def idxk(self):
        return self._idxk

    @idxk.setter
    def idxk(self, x):
        self._idxk = x







def gen_emojis(k=20):
	return ''.join(random.choices(EMOJIS, k=k))


def is_hidden(p):
	"""Checking if hidden file or directory."""
	return True if re.search(os.sep + '\.', str(p)) else False 


def whats_in_directory(
	directory: str,
	*,
	fmt: List[str] = [],
	recursive: bool = True,
	# include_hidden: bool = False,
	case_insensitive: bool = False,  # case censitive by default
	verbose: bool = True,
	status_txt: str = 'Working on it...',
	spinner: str = 'flip',
) -> (List, List, List, Dict):
	"""
		Summary/info of a directory.
		-> files_1 list, sub-dirs list, same_files_list, mapping_dict
	"""

	# error checking
	if not Path(directory).is_dir():
		raise TypeError(f'Type of {Path(directory)} should be directory, not {type(directory)}')
		sys.exit()

	# saveout
	c = {
		# all hidden files
		'hidden': {
			'files': [],
			'directories': [],
			# 'mapping_suffix': {},  # TODO
			# 'mapping_stem': {}, 
		},

		# all visible files  & mappings
		'visible': {
			'files': [],
			'directories': [],
			'mapping_suffix': {},
			'mapping_stem': {},
		},

		'attrs': {
			'nd': 0,
			'nf': 0,
			'nhd': 0,
			'nhf': 0,
			'no': 0,
		}
	}


	# case insensitive --> lower
	if case_insensitive and len(fmt) != 0:
		fmt = [x.lower() for x in fmt]


	# glob
	nt = 0 # number of total
	with CONSOLE.status(f"[b]{status_txt}", spinner=spinner) as _:  # status spinner
		for x in Path(directory).glob('**/*' if recursive else '*'):   # generator, not using tqdm
			nt += 1 	# count
			x = x.resolve() 	# use abs 

			# check if is valid (files & directories)
			if not x.is_file() and not x.is_dir():  
				continue
			
			# hidden files & directories
			if is_hidden(x):
				if x.is_dir():
					c['hidden']['directories'].append(x)
				else:
					# check format
					if (x.suffix.lower() if case_insensitive else x.suffix) in fmt or len(fmt) == 0:
						c['hidden']['files'].append(x)

			# normal directories
			else:
				if x.is_dir():   
					c['visible']['directories'].append(x)

				# normal files
				if x.is_file():
					# check format
					if (x.suffix.lower() if case_insensitive else x.suffix) in fmt or len(fmt) == 0:
						c['visible']['files'].append(x)

						# mapping
						c['visible']['mapping_stem'].setdefault(x.stem.lower() if case_insensitive else x.stem, []).append(x)
						c['visible']['mapping_suffix'].setdefault(x.suffix[1:].lower() if case_insensitive else x.suffix[1:], []).append(x)


	# save attrs					
	nd, nf = len(c['visible']['directories']), len(c['visible']['files'])
	nhd, nhf = len(c['hidden']['directories']), len(c['hidden']['files'])
	no = nt - nf - nd - nhd -nhf  # number of others
	c['attrs']['nd'] = nd
	c['attrs']['nf'] = nf
	c['attrs']['nhd'] = nhd
	c['attrs']['nhf'] = nhf
	c['attrs']['no'] = no
	c['attrs']['nt'] = nt


	# info
	if verbose:
		# file format
		if len(fmt) != 0:
			s = f"\n> File Format: {fmt}\n" 
			s += f"> Find {nf} visible files, {nhf} hidden files"
		else:
			s = f"> Find {nf} visible files, {nd} visible directories, {nhf} hidden files, {nhd} hidden directories"

		# num of others
		if no > 0:
			s += f", {no} others (other format files)."
		elif no == 0:
			s += '.'
		elif no < 0:
			raise ValueError(f"> ValueError: number of other can not be smaller than 0")
		CONSOLE.print(s) 	# info
	return c



def rename(
	directory, 
	*,
	with_prefix: str = '',
	with_num: bool = False,
	with_znum: bool = False,
	with_random: bool = False,
	with_uuid: bool = False,
	with_time: bool = False,
	bits: int = 16,  # with random
	least_zeros: bool = False, # znum with least zero
	start_from: int = 0,  # with num & znum
	fmt: List[str] = [],  # Default: all type files + dir, lower-case
	case_insensitive: bool = False,   # No need to change
	include_subdirs: bool = False,  # rename sub-dir at the same time
	only_subdirs: bool = False,  # only rename sub-dir
	recursive: bool = False,  # Not recursive
	alignment: bool = True,  # same name file should has same name after renaming
	verbose: bool = True,
):
	"""Rename sub-dirs or files within directory"""

	# ===> argparser will do this by default
	# ------------------------------------------------
	# # check ways, only one will work
	# if not any((with_znum, with_num, with_random, with_uuid)):
	# 	rich.print(f'> Attention: No method selected. Using [b cyan i]random[/b i cyan] strings default.')
	# 	with_random = True

	# # error checking
	# if sum((with_znum, with_num, with_random, with_uuid)) > 1:
	# 	raise ValueError(
	# 		f'Methods selected too much at the same time:'
	# 		f'\n\twith_znum: {with_znum}'
	# 		f'\n\twith_num: {with_num}'
	# 		f'\n\twith_random: {with_random}'
	# 		f'\n\twith_uuid: {with_uuid}'
	# 	)
	# ------------------------------------------------

	# make sure to do it
	while True: 
		_input = CONSOLE.input(prompt=f"🤔 Sure to rename?\n> ")

		# check input
		if _input.lower() in (
			'n', 'no', 'false', 'f', 'bu', 'gun',
			'fuck off', 'bububu', 'bule'
		):
			CONSOLE.print(f"> Cancelled ❌")
			sys.exit()
		elif _input.lower() in (
				'y', 'yes', 'true', 't', 'of course', 'yeah', 
				'enen', 'en', 'enenen', 'shide', 'shi', 'dui', 'ok', 'go',
				'haode', 'duide', 'gaokuaidian', 'zouni'
			):
			break


	# glob files & directories at 1st
	c = whats_in_directory(
		directory,
		recursive=recursive,  # false 
		fmt=fmt,  # []
		case_insensitive=case_insensitive, 	# false
		verbose=verbose,
		status_txt='Loading all files...',
	)

	# file or sub-dirs or both
	if only_subdirs:  # only sub-dirs
		fs = dict()
		for _d in c['visible']['directories']:
			fs.update({'___dir_' + _d.name: [_d]})
	else: # files(+ sub-dirs)
		fs = c['visible']['mapping_stem']
		if include_subdirs:  # rename sub-dirs or not
			for _d in c['visible']['directories']:
				fs.update({'___dir_' + _d.name: [_d]})


	# check empty
	if len(fs) == 0:
		CONSOLE.print(f"> Nothing found!")
		sys.exit()

	
	# uuid4 & random
	if with_uuid or with_random:
		_strings = set()

	# num & znum
	if with_num or with_znum:
		idx = 0
		fs_copy = list()

	# iter
	for _, p in tqdm(fs.items(), desc='renaming', total=len(fs)):
		if with_uuid:
			_new_stem = str(uuid.uuid4())
			while (_new_stem in _strings) or (any([x.with_stem(_new_stem).exists() for x in p])):  # exists
				_new_stem = str(uuid.uuid4()) 
			_strings.add(_new_stem) 	# get valid uuid4
			[x.rename(x.with_stem(_new_stem)) for x in p] # rename 
		elif with_random:
			_new_stem = ''.join(random.choices(ASCII_LETTERS, k=bits))
			while (_new_stem in _strings) or (any([x.with_stem(_new_stem).exists() for x in p])):  # exists
				_new_stem = ''.join(random.choices(ASCII_LETTERS, k=bits))
			_strings.add(_new_stem) 	# get valid random string
			[x.rename(x.with_stem(_new_stem)) for x in p] # rename 
		elif with_prefix:
			[x.rename(x.with_stem(with_prefix + '-_-' + x.stem)) for x in p]
		elif with_num or with_time or with_znum:
			# with time
			time.sleep(1e-6)
			_now = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"  
			if with_num or with_znum:
				fs_copy.append([x.rename(x.with_stem(_now)) for x in p]) 	# rename 
			else:
				[x.rename(x.with_stem(_now)) for x in p] 	# rename 

	# num or znum
	if with_num or with_znum:
		for idx, p in tqdm(enumerate(fs_copy, start=start_from), desc='checking again', total=len(fs_copy)):
			if with_num:
				[x.rename(x.with_stem(str(idx))) for x in p]
			elif with_znum:
				if least_zeros:
					_new_stem = str(idx).zfill(len(str(len(fs))))
				else:
					_new_stem = str(idx).zfill(bits)   
				[x.rename(x.with_stem(_new_stem)) for x in p]



def check_image_integrity(path) -> (bool, Optional[str]):
	"""check single image's integrity."""
	_check_again = True  # flag
	
	# PIL check 1st, and restore corrupt JPEG
	try: 
		with Image.open(str(path)) as im:
			im.verify()   # PIL image quality check
			if im.format.lower() in ('jpeg', 'jpg'): # jpeg checking & restore 
				with open(path, "rb") as f:
					f.seek(-2, 2)
					if f.read() != b'\xff\xd9':     # corrupt JPEG
						ImageOps.exif_transpose(Image.open(path)).save(path, 'JPEG', subsampling=0, quality=100)
						# CONSOLE.print(f"> Corrupt JPEG restored automatically: {path}")
	except OSError:
		_check_again = False  # set flag
		return False, f"PIL verify failed! | {path}"

	# opencv check again
	if _check_again:
		try:
			if cv2.imread(str(path)) is None:  
				return False, f"Image can not be read by OpenCV | {path}"
		except Exception as e:
			return False, f"OpenCV exceptions: {e} | {path}"
	return True, None


def check_images_integrity(
	directory_i: str,
	*,
	directory_o: str = 'output-deprecated',
	fmt: List[str] = [],  # Default: all type files + dir, lower-case
	case_sensitive: bool = False,   # case censitive by default
	recursive: bool = True,  # true
	verbose: bool = False,
	status_txt: str = 'Loading files...',
	spinner: str = 'flip',
):
	has_deprecated = False  # flag

	# check saveout directory
	saveout_dir = Path(directory_o)
	if not saveout_dir.exists():
		saveout_dir.mkdir()
	else:
		CONSOLE.print(
			f"[red]Error[/red] -> Saveout directory: [u]{saveout_dir.resolve()}[/u] exists. Try somewhere else."
		)
		sys.exit()	

	# glob
	c = whats_in_directory(
		directory_i,
		fmt=fmt,
		case_insensitive=not case_sensitive,  # false
		recursive=recursive,  # true
		verbose=verbose,
		status_txt=status_txt,
		spinner=spinner,
	)


	# integrity checking
	for f in tqdm(c['visible']['files'], desc=f"integrity checking", total=len(c['visible']['files'])):
		if not check_image_integrity(f)[0]:
			has_deprecated = True
			shutil.move(str(f), str(saveout_dir))

	# rmdir -> empty
	s = f"✅ Image integrity complete."
	if not has_deprecated:
		saveout_dir.rmdir() 	
		s += f" Every image is OK."
	else:
		s += f"\n✅ The deprecated saved at: [u]{saveout_dir.resolve()}"

	# info
	if verbose:
		CONSOLE.print(s)


def dir_combine(
	directory_i: str,
	*,
	directory_o: str = 'output-conbined',
	move: bool = False,
	fmt: List[str] = [],  # Default: all type files + dir, lower-case
	case_insensitive: bool = False,   # false
	non_recursive: bool = False,  # recursive
	verbose: bool = True,
	delimiter: str = '-',
	status_txt: str = 'Loading files...',
	spinner: str = 'flip',
):

	# check saveout directory
	saveout_dir = Path(directory_o)
	if not saveout_dir.exists():
		saveout_dir.mkdir()
	else:
		CONSOLE.print(
			f"[red]Error[/red] -> Saveout directory: [u]{saveout_dir.resolve()}[/u] exists. Try somewhere else."
		)
		sys.exit()	

	# glob
	c = whats_in_directory(
		directory_i,
		fmt=fmt,
		case_insensitive=case_insensitive,  # false
		recursive=not non_recursive,  # true
		verbose=verbose,
		status_txt=status_txt,
		spinner=spinner,
	)


	# combining
	if len(c['visible']['files']) == 0:
		CONSOLE.print(
			f'[red]Error[/red] -> Files Not Found! Go check out '
			f'directory_i: [u]{Path(directory_i).resolve()}[/u]' 
		)
		saveout_dir.rmdir() 	# remove saveout directory
		sys.exit()
	else:
		_method = 'move' if move else 'copy'
		for d in tqdm(c['visible']['files'], desc=f"Combining [{_method}]", total=len(c['visible']['files'])):

			# cut to reletive
			for i, x in enumerate(d.parts):
				if Path(directory_i).resolve().name == x:
					d_ = delimiter.join(d.parts[i:])
					break
			des_path = saveout_dir / d_

			# copy or move
			if move:  
				shutil.move(str(d.resolve()), str(des_path))
			else:
				shutil.copy(str(d.resolve()), str(des_path))
	CONSOLE.print(f"> Saved at: [u green]{saveout_dir.resolve()}")   # saveout log




def images_deduplicate(
	directory_i: str,
	*,
	directory_duplicated: str = 'output-duplicated',
	fmt: List[str] = [],  # Default: all type files + dir, lower-case
	case_sensitive: bool = False,   # false
	recursive: bool = True,  # true
	verbose: bool = True,
	base_method: bool = False,
	nn_method: bool = False,
	threshold: float = 0.9,
	device: str = 'cpu',
	status_txt: str = 'Loading files...',
	spinner: str = 'flip',
):

	# make sure to do it
	while True: 
		_input = CONSOLE.input(prompt=f"🤔 Sure all images are valid? If not, go checking image integrity first!\n> ")

		# check input
		if _input.lower() in (
			'n', 'no', 'false', 'f', 'bu', 'gun',
			'fuck off', 'bububu', 'bule'
		):
			CONSOLE.print(f"> Cancelled ❌")
			sys.exit()
		elif _input.lower() in (
				'y', 'yes', 'true', 't', 'of course', 'yeah', 
				'enen', 'en', 'enenen', 'shide', 'shi', 'dui', 'ok', 'go',
				'haode', 'duide', 'gaokuaidian', 'zouni'
			):
			break


	# check duplicated directory
	has_duplicated = False  # flag
	directory_duplicated = Path(directory_duplicated)
	if not directory_duplicated.exists():
		directory_duplicated.mkdir()
	else:
		CONSOLE.print(
			f"[red]Error[/red] -> directory_duplicated: [u]{directory_duplicated.resolve()}[/u] exists. Try somewhere else."
		)
		sys.exit()	


	# glob
	c = whats_in_directory(
		directory_i,
		fmt=fmt,
		case_insensitive=not case_sensitive, # case insensitive
		recursive=recursive,  # true
		verbose=verbose,
		status_txt=status_txt,
		spinner=spinner,
	)


	# ==> base method
	if base_method:
		md5_img_dict = {}   # {md5: img_path}
		for f in tqdm(c['visible']['files'], desc="de-duplicating", total=len(c['visible']['files'])):
			md5 = get_md5(str(f))  # get file md5

			# compare and save 
			if md5 in md5_img_dict.keys(): 
				similar_img_path = md5_img_dict[md5] 
				shutil.move(str(f), str(directory_duplicated)) 
				has_duplicated = True
			else: 
				md5_img_dict[md5] = f 


	# ==> nn method
	if nn_method:
		from usls.src.feature_extractor import FeatureExtractor
		model = FeatureExtractor() # build model
		CONSOLE.print(f"✅ nn model built.")

		for f in tqdm(c['visible']['files'], desc="de-duplicating", total=len(c['visible']['files'])):
			
			# input
			model.model.setInput(cv2.dnn.blobFromImage(cv2.imread(str(f)), scalefactor=1 / 255, size=(224, 224), swapRB=True))
			y_q = model.model.forward()   # query feat
			y_q = np.divide(y_q, np.sqrt(np.sum(np.square(y_q), axis=1, keepdims=True))) 	# normalize, IP

			if model.num_feats == 0:
				model.index.add(y_q)    # register when empty
				continue

			D, I = model.index.search(y_q, 1)  # query 

			if D[0][0] >= threshold:

				shutil.move(str(f), str(directory_duplicated)) 
				has_duplicated = True
			else:
				model.index.add(y_q)    # register



	# deal with saveout directory
	s = f"✅ Images deduplicate complete."

	if not has_duplicated:
		directory_duplicated.rmdir() 	
		s += f"\n✅ No image is duplicated."
	else:
		s += f"\n✅ The duplicated saved at: {directory_duplicated.resolve()}"

	# info
	CONSOLE.print(s)






def download_from_url(url, saveout, prefix='downloading'):

    # check saveout 
    if Path(saveout).exists() and Path(saveout).is_file():
        # print(f'{saveout} is already exists, return None.')
        return saveout
    else:
        # urllib.request.urlretrieve(str(url), filename=str(saveout))
        with urllib.request.urlopen(url) as source, open(saveout, "wb") as output:
            with tqdm(
                desc=prefix,
                total=int(source.info().get("Content-Length")),
                ncols=100,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as loop:
                while True:
                    buffer = source.read(8192)
                    if not buffer:
                        break
                    output.write(buffer)
                    loop.update(len(buffer))

        # print(f'{saveout} downloaded!')
        return saveout


def get_md5(f):
    m = hashlib.md5(open(f,'rb').read())
    return m.hexdigest()



def natural_sort(x, _pattern=re.compile('([0-9]+)'), mixed=True):
    return [int(_x) if _x.isdigit() else _x for _x in _pattern.split(str(x) if mixed else x)]


class TIMER(contextlib.ContextDecorator):

    def __init__(self, prefix='Inspector', verbose=True):
        self.prefix = prefix
        self.verbose = verbose

    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, type, value, traceback):
        self.duration = time.time() - self.t0
        if self.verbose:
            print(f"[{self.prefix}] --> {(time.time() - self.t0) * 1e3:.2f} ms.")

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            t0 = time.time()
            ret = func(*args, **kwargs)
            if self.verbose:
                print(f"[{self.prefix}] --> {(time.time() - t0) * 1e3:.2f} ms.")

            return ret
        return wrapper



class Palette:
    """colors palette"""

    def __init__(self, shuffle=False):
        _hex_colors = [
            '33FF00', '9933FF', 'CC0000', 'FFCC00', '99FFFF', '3300FF',
            'FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', 
            '1A9334', '00D4BB', '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', 
            '520085', 'CB38FF', 'FF95C8', 'FF37C7', '#F0F8FF', '#4682B4', '#0000CD', '#9932CC',  
            '#FFB6C1', '#FFC0CB', '#DC143C', '#FFF0F5', '#DB7093', '#FF69B4', '#FF1493', '#C71585',  
            '#DDA0DD', '#EE82EE', '#FF00FF', '#FF00FF', '#8B008B', '#800080', '#BA55D3', '#9400D3',   
            '#8A2BE2', '#9370DB', '#7B68EE', '#6A5ACD', '#483D8B', '#E6E6FA', '#F8F8FF', '#0000FF', 
            '#00008B', '#000080', '#4169E1', '#6495ED', '#B0C4DE', '#778899', '#708090', '#1E90FF', 
            '#87CEFA', '#87CEEB', '#00BFFF', '#808080', '#696969', '#000000', '#DA70D6', '#D8BFD8', 
            '#ADD8E6', '#B0E0E6', '#5F9EA0', '#F0FFFF', '#E1FFFF', '#AFEEEE', '#00FFFF', '#00FFFF', 
            '#008B8B', '#008080', '#48D1CC', '#20B2AA', '#40E0D0', '#7FFFAA', '#00FA9A', '#F5FFFA',  
            '#2E8B57', '#F0FFF0', '#90EE90', '#98FB98', '#8FBC8F', '#32CD32', '#00FF00', '#228B22',  
            '#7FFF00', '#7CFC00', '#ADFF2F', '#556B2F', '#6B8E23', '#FAFAD2', '#FFFFF0', '#FFFFE0',  
            '#BDB76B', '#FFFACD', '#EEE8AA', '#F0E68C', '#FFD700', '#FFF8DC', '#DAA520', '#FFFAF0',  
            '#FFE4B5', '#FFA500', '#FFEFD5', '#FFEBCD', '#FFDEAD', '#FAEBD7', '#D2B48C', '#DEB887',
            '#FAF0E6', '#CD853F', '#FFDAB9', '#F4A460', '#D2691E', '#8B4513', '#FFF5EE', '#A0522D', 
            '#FF4500', '#E9967A', '#FF6347', '#FFE4E1', '#FA8072', '#FFFAFA', '#F08080', '#BC8F8F', 
            '#A52A2A', '#B22222', '#8B0000', '#800000', '#FFFFFF', '#F5F5F5', '#DCDCDC', '#D3D3D3', 
            '#191970', '#9932CC', '#00CED1', '#2F4F4F', '#C0C0C0', '#A9A9A9', '#CD5C5C', '#FF0000',
            '#FFA07A', '#FF7F50', '#FFE4C4', '#FF8C00', '#FDF5E6', '#F5DEB3', '#FFFF00', '#808000',
            '#008000', '#006400', '#00FF7F', '#3CB371', '#4B0082',
        ]
        
        # shuffle color 
        if shuffle:
            random.shuffle(_hex_colors)

        self.palette = [self.hex2rgb(c) if c.startswith('#') else self.hex2rgb('#' + c) for c in _hex_colors]
        self.n = len(self.palette)


    def __call__(self, i, bgr=False):    
        """ int -> rgb color """    
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod  
    def hex2rgb(h):
        """
        int('CC', base=16) hex -> 10
        RGB的数值 = 16 * HEX的第一位 + HEX的第二位
        RGB: 92, 184, 232 
        92 / 16 = 5余12 -> 5C
        184 / 16 = 11余8 -> B8
        232 / 16 = 14余8 -> E8
        HEX = 5CB8E8
        """
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))



def smart_path(path='', *, exist_ok=False, sep='-', mkdir=False, method=0):
    # Increment file or directory path

    # random string in currnet path
    if path == '':
        if method == 0:
            _ASCII_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            path = Path.cwd() / (''.join(random.choices(_ASCII_LETTERS, k=8)))
        elif method == 1:
            path = Path.cwd() / str(uuid.uuid4())
        elif method == 2:
             path = Path.cwd() / datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = Path(path)  # os-agnostic

    # make increment
    if path.exists() and not exist_ok:
        path, suffix = (path.with_suffix(''), path.suffix) if path.is_file() else (path, '')

        # increment path
        for n in range(2, 9999):
            p = f'{path}{sep}{n}{suffix}'  
            if not os.path.exists(p):  # non-exist will break
                break
        path = Path(p)

        # path, suffix = (path.with_suffix(''), path.suffix) if path.is_file() else (path, '')
        # dirs = glob.glob(f"{path}{sep}*")  # similar paths
        # matches = [re.search(rf"%s{sep}(\d+)" % path.stem, d) for d in dirs]
        # i = [int(m.groups()[0]) for m in matches if m]  # indices
        # n = max(i) + 1 if i else 2  # increment number
        # path = Path(f"{path}{sep}{n}{suffix}")  # increment path

    # make dir directly
    if mkdir:
        path.mkdir(parents=True, exist_ok=True)  # make directory

    return path





class USLS:

	def __init__(
		self, 
		name="usls"
		# *, 
	):
		self.name = name
		self._ASCII_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


	def _is_hidden(self, p):
		"""Checking if hidden file or directory."""
		return True if re.search(os.sep + '\.', str(p)) else False 


	def inspect(
		self,
		directory: str,
		*,
		fmt: List[str] = [],
		recursive: bool = True,
		include_hidden: bool = False,
		case_sensitive: bool = False,
		verbose: bool = True
	) -> (List, Dict):
		"""Summary of a directory."""

		# error checking
		if not Path(directory).is_dir():
			raise TypeError(f'Type of {Path(directory)} should be directory, not {type(directory)}')
			sys.exit()

		# saveout
		fs, mapping, ds = list(), dict(), list()
		# nf, nd, nhf, nhd = 0, 0, 0, 0  # num_file, num_dir, num_hidden_file, num_hidden_dir
		nt = 0 # number of total

		# glob
		with CONSOLE.status("[b]Working on it...", spinner='flip') as _:  # status spinner
			for x in Path(directory).glob('**/*' if recursive else '*'):   # generator, not using tqdm
				nt += 1 	# count
				x = x.resolve() 	# use abs path
				
				if not include_hidden:
					if self._is_hidden(x):    # if not show hidden
						continue
				
				if x.is_dir():   # is dir 
					ds.append(str(x))
					mapping.setdefault('directories', []).append(x)
				
				if not x.is_file():  # not valie file
					continue

				# saveout
				if (x.suffix if case_sensitive else x.suffix.lower()) in fmt or len(fmt) == 0:  # empty means every type
					fs.append(str(x))
					if x.suffix == '':   # no suffix file (only cope with last suffix)
						mapping.setdefault(x.stem, []).append(x)
					else:
						mapping.setdefault(x.suffix[1:] if case_sensitive else x.suffix[1:].lower(), []).append(x)

		# info
		if verbose:
			nd, nf = len(ds), len(fs)
			no = nt - nf - nd
			s = f"> Find {nf} files, {nd} directories"
			if no > 0:
				s += f", {no} others (other format file | hidden files | hidden directories)."
			elif no == 0:
				s += '.'
			elif no < 0:
				raise ValueError(f"> ValueError: number of other can not be smaller than 0")
			CONSOLE.print(s) 	# info
		
		return fs, ds, mapping



	def rename(
		self,
		directory, 
		*,
		with_prefix: str = '',
		with_num: bool = False,
		with_znum: bool = False,
		with_random: bool = False,
		with_uuid: bool = False,
		bits: int = 16,
		fmt: List[str] = [],  # Default: all type files + dir, lower-case
		case_sensitive: bool = False,   # No need to change
		include_hidden: bool = False,  # Hidden files should not be renamed!
		with_dir: bool = False,  # rename dir at the same time
		recursive: bool = False,  # Not recursive
		verbose: bool = True
	):
		"""Rename sub-dirs or files within directory"""

		# check ways, only one will work
		if not any((with_znum, with_num, with_random, with_uuid)):
			rich.print(f'> Attention: No method selected. Using [b cyan i]random[/b i cyan] strings default.')
			with_random = True

		# error checking
		if sum((with_znum, with_num, with_random, with_uuid)) > 1:
			raise ValueError(
				f'Methods selected too much at the same time:'
				f'\n\twith_znum: {with_znum}'
				f'\n\twith_num: {with_num}'
				f'\n\twith_random: {with_random}'
				f'\n\twith_uuid: {with_uuid}'
			)

		# glob files & directories
		f_list, d_list, _ = self.inspect(
			directory,
			recursive=recursive,  # false 
			fmt=fmt,  # []
			case_sensitive=case_sensitive, # false
			include_hidden=include_hidden,  # false
			verbose=verbose
		)

		# counting file
		if with_dir:
			f_list += d_list

		# uuid4 & random
		if with_uuid or with_random:
			sets_string = set()

			# gen uuid4/random string
			while len(sets_string) != len(f_list):
				sets_string.add(str(uuid.uuid4()) if with_uuid else ''.join(random.choices(self._ASCII_LETTERS, k=bits)))

			# rename
			for x, x_ in tqdm(zip(f_list, sets_string), desc='renaming', total=len(f_list)):
				x = Path(x)
				x.rename(x.with_stem(x_))


		# with num & znum & random letters
		if with_num or with_znum or with_prefix:

			# method with prefix
			if with_prefix:
				for x in tqdm(f_list, desc='renaming', total=len(f_list)): 
					x = Path(x)
					x.rename(x.with_stem(with_prefix + '-' + x.stem))
			else:  # make sure aligned
				for x in tqdm(f_list, desc='alignment', total=len(f_list)):
					x = Path(x)
					x.rename(x.with_stem('j1a2m3j4a5m6j7o8n9' + '-' + x.stem))        

			# method with num & znum
			if with_num or with_znum:

				# laod again
				f_list, d_list, _ = self.inspect(
					directory,
					recursive=recursive,
					fmt=fmt,
					case_sensitive=case_sensitive,
					include_hidden=include_hidden,
					verbose=False
				)

				if with_dir:
					f_list += d_list

				# rename
				idx = 0
				for x in tqdm(f_list, desc='renaming', total=len(f_list)):
					x = Path(x)
					x.rename(x.with_stem(str(idx) if with_num else str(idx).zfill(len(str(len(f_list))))))
					idx += 1


	def combine(
		self,
		directory_i: str,
		*,
		directory_o: str = 'output-conbined',
		move: bool = False,
		fmt: List[str] = [],  # Default: all type files + dir, lower-case
		case_sensitive: bool = False,   # false
		include_hidden: bool = False,  # false! Hidden files should not be combined!
		recursive: bool = True,  # true
		verbose: bool = True
	):

		# dir checking
		if not Path(directory_i).is_dir():
			raise TypeError(f'Type of {Path(directory_i)} should be directory, not {type(directory_i)}')

		# check saveout directory
		saveout_dir = Path(directory_o)
		if not saveout_dir.exists():
			saveout_dir.mkdir()
		else:
			CONSOLE.print(
				f"[red]Error[/red] -> Saveout directory: [u]{saveout_dir.resolve()}[/u] exists. Try somewhere else."
			)
			sys.exit()	

		# glob
		f_list, d_list, _ = self.inspect(
			directory_i,
			fmt=fmt,
			case_sensitive=case_sensitive,  # false
			include_hidden=include_hidden,  # false
			recursive=recursive,  # true
			verbose=verbose
		)

		# combining
		if len(f_list) == 0:
			CONSOLE.print(
				f'[red]Error[/red] -> Files Not Found! Go check out '
				f'directory_i: [u]{Path(directory_i).resolve()}[/u]' 
				# f'fmt: {fmt} (empty means all)'
			)
			saveout_dir.rmdir() 	# remove saveout directory
			sys.exit()
		else:

			_method = 'move' if move else 'copy'
			for d in tqdm(f_list, desc=f"Combining [{_method}]", total=len(f_list)):

				# cut to reletive
				for i, x in enumerate(Path(d).parts):
					if Path(directory_i).name == x:
						d_ = '-'.join(Path(d).parts[i:])
						break

				des_path = saveout_dir.resolve() / d_

				# copy or move
				if move:  
					shutil.move(str(Path(d).resolve()), str(des_path))
				else:
					shutil.copy(str(Path(d).resolve()), str(des_path))
		CONSOLE.print(f"> Saved at: [u green]{saveout_dir.resolve()}")   # saveout log



	def _check_image_integrity(self, path) -> (bool, Optional[str]):
		"""check single image's integrity."""
		_check_again = True  # flag
		
		# PIL check 1st, and restore corrupt JPEG
		try: 
			with Image.open(str(path)) as im:
				im.verify()   # PIL image quality check
				if im.format.lower() in ('jpeg', 'jpg'): # jpeg checking & restore 
					with open(path, "rb") as f:
						f.seek(-2, 2)
						if f.read() != b'\xff\xd9':     # corrupt JPEG
							ImageOps.exif_transpose(Image.open(path)).save(path, 'JPEG', subsampling=0, quality=100)
							CONSOLE.print(f"> Corrupt JPEG restored automatically: {path}")
		except OSError:
			_check_again = False  # set flag
			return False, f"PIL verify failed! | {path}"

		# opencv check again
		if _check_again:
			try:
				if cv2.imread(str(path)) is None:  
					return False, f"Image can not be read by OpenCV | {path}"
			except Exception as e:
				return False, f"OpenCV exceptions: {e} | {path}"
		return True, None



	def images_integrity_checking(
		self, 
		directory_i: str,
		*,
		directory_o: str = 'output-deprecated',
		fmt: List[str] = [],  # Default: all type files + dir, lower-case
		case_sensitive: bool = False,   # false
		include_hidden: bool = False,  # false! Hidden files should not be combined!
		recursive: bool = True,  # true
		verbose: bool = True
	):
		has_deprecated = False  # flag

		# check saveout directory
		saveout_dir = Path(directory_o)
		if not saveout_dir.exists():
			saveout_dir.mkdir()
		else:
			CONSOLE.print(
				f"[red]Error[/red] -> Saveout directory: [u]{saveout_dir.resolve()}[/u] exists. Try somewhere else."
			)
			sys.exit()	

		# glob
		f_list, _, _ = self.inspect(
			directory_i,
			fmt=fmt,
			case_sensitive=case_sensitive,  # false
			include_hidden=include_hidden,  # false
			recursive=recursive,  # true
			verbose=verbose
		)

		# integrity checking
		for f in tqdm(f_list, desc=f"integrity check", total=len(f_list)):
			if not self._check_image_integrity(f)[0]:
				has_deprecated = True
				shutil.move(str(f), str(saveout_dir))

		# rmdir -> empty
		s = f"✅ Image integrity complete."
		if not has_deprecated:
			saveout_dir.rmdir() 	
			s += f" Every image is OK."
		else:
			s += f"\n✅ The deprecated saved at: [u]{saveout_dir.resolve()}"

		# info
		if verbose:
			CONSOLE.print(s)




	def deduplicate(
		self, 
		directory_i: str,
		*,
		directory_deprecated: str = 'output-deprecated',
		directory_duplicated: str = 'output-duplicated',
		fmt: List[str] = [],  # Default: all type files + dir, lower-case
		case_sensitive: bool = False,   # false
		include_hidden: bool = False,  # false! Hidden files should not be combined!
		recursive: bool = True,  # true
		verbose: bool = True,
		base_method: bool = False,
		nn_method: bool = False,
		threshold: float = 0.9,
		check_integrity_first: bool = False, 	# check image integrity first 
		device: str = 'cpu'
	):


		# check duplicated directory
		has_duplicated = False  # flag
		directory_duplicated = Path(directory_duplicated)
		if not directory_duplicated.exists():
			directory_duplicated.mkdir()
		else:
			CONSOLE.print(
				f"[red]Error[/red] -> directory_duplicated: [u]{directory_duplicated.resolve()}[/u] exists. Try somewhere else."
			)
			sys.exit()	


		# check deprecated directory
		if check_integrity_first:
			has_deprecated = False  # flag
			directory_deprecated = Path(directory_deprecated)
			if not directory_deprecated.exists():
				directory_deprecated.mkdir()
			else:
				CONSOLE.print(
					f"[red]Error[/red] -> directory_deprecated: [u]{directory_deprecated.resolve()}[/u] exists. Try somewhere else."
				)
				sys.exit()	




		# glob
		f_list, _, _ = self.inspect(
			directory_i,
			fmt=fmt,
			case_sensitive=case_sensitive,  # false
			include_hidden=include_hidden,  # false
			recursive=recursive,  # true
			verbose=True
		)

		# ==> base method
		if base_method:
			md5_img_dict = {}   # {md5: img_path}
			for f in tqdm(
				f_list, 
				desc=f"integrity checking & de-duplicating" if check_integrity_first else "de-duplicating", 
				total=len(f_list)
			):
				if check_integrity_first:  # integrity checking
					if not self._check_image_integrity(f)[0]:   
						shutil.move(str(f), str(directory_deprecated))
						has_deprecated = True
						continue

				# pass checking
				md5 = get_md5(str(f))

				# compare and save 
				if md5 in md5_img_dict.keys(): 
					similar_img_path = md5_img_dict[md5] 
					shutil.move(str(f), str(directory_duplicated)) 
					has_duplicated = True
				else: 
					md5_img_dict[md5] = f 


		# ==> nn method
		if nn_method:
			from usls.src.feature_extractor import FeatureExtractor
			model = FeatureExtractor() # build model

			# model.register()

			x = '/Users/jamjon/Desktop/bbb/a.jpg'

			# if isinstance(x, str):
			# 	x = cv2.imread(x)
			# assert isinstance(x, np.ndarray), f"x should be np.ndarray"
			# print(x.shape)
			# blob = cv2.dnn.blobFromImage(x, scalefactor=1 / 255, size=(224, 224), swapRB=True)
			# model.model.setInput(blob)
			# y = model.model.forward()
			# print(y.shape)

			# model.index.add(y)    # register
			# print(model.num_feats)

			# exit()

			for f in tqdm(
				f_list, 
				desc=f"integrity checking & de-duplicating" if check_integrity_first else "de-duplicating", 
				total=len(f_list)
			):
				if check_integrity_first:  # integrity checking
					if not self._check_image_integrity(f)[0]:   
						shutil.move(str(f), str(directory_deprecated))
						has_deprecated = True
						continue

				# infer
				print(f"f--> {f}")
				if isinstance(f, str):
					f = cv2.imread(f)
				assert isinstance(f, np.ndarray), f"f should be np.ndarray"
				print(f.shape)
				blob = cv2.dnn.blobFromImage(f, scalefactor=1 / 255, size=(224, 224), swapRB=True)
				model.model.setInput(blob)
				y_q = model.model.forward()
				print(y_q.shape)


				if model.num_feats == 0:
					# model.register(xs=[str(f)])
					model.index.add(y_q)    # register
					continue

				# y_q = model(f) # query feature
				D, I = model.index.search(y_q, 1)  # query 

				if D[0][0] >= threshold:
					shutil.move(str(f), str(directory_duplicated)) 
					has_duplicated = True
				else:
					# nn_model.register(xs=[str(f)])
					model.index.add(y_q)    # register



		# deal with saveout directory
		s = f"✅ Images deduplicate complete."

		if check_integrity_first:
			if not has_deprecated:
				s += f"\n✅ No image is deprecated."
				directory_deprecated.rmdir() 	
			else:
				s += f"\n✅ The deprecated saved at: {directory_deprecated.resolve()}"


		if not has_duplicated:
			directory_duplicated.rmdir() 	
			s += f"\n✅ No image is duplicated."
		else:
			s += f"\n✅ The duplicated saved at: {directory_duplicated.resolve()}"

		# info
		if verbose:
			CONSOLE.print(s)



class CenterCrop:
    def __init__(self, size=224):
        super().__init__()
        self.h, self.w = (size, size) if isinstance(size, int) else size

    def __call__(self, im):  # im = np.array HWC
        imh, imw = im.shape[:2]
        m = min(imh, imw)  # min dimension
        top, left = (imh - m) // 2, (imw - m) // 2
        return cv2.resize(im[top:top + m, left:left + m], (self.w, self.h), interpolation=cv2.INTER_LINEAR)


class Normalize:
    def __init__(self, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
        super().__init__()
        self.mean = mean
        self.std = std

    def __call__(self, x): 
        if not isinstance(self.mean, np.ndarray):
            self.mean = np.array(self.mean, dtype=np.float32)
        if not isinstance(self.std, np.ndarray):
            self.std = np.array(self.std, dtype=np.float32)
        if self.mean.ndim == 1:
            self.mean = np.reshape(self.mean, (-1, 1, 1))
        if self.std.ndim == 1:
            self.std = np.reshape(self.std, (-1, 1, 1))
        _max = np.max(abs(x))
        _div = np.divide(x, _max)  # i.e. _div = data / _max
        _sub = np.subtract(_div, self.mean)  # i.e. arrays = _div - mean
        arrays = np.divide(_sub, self.std)  # i.e. arrays = (_div - mean) / std
        return arrays


class Softmax:
    def __init__(self, dim=1):
        super().__init__()
        self.dim = dim

    def __call__(self, x):
        exp_x = np.exp(x)
        return exp_x / np.sum(exp_x, axis=self.dim)


def scale_boxes_batch(
        boxes, 
        ims_shape, 
        im0s_shape, 
        min_bbox_size=None, 
        masks=False,
        # min_wh_ratio=None
    ):
    # Batch Rescale boxes (xyxy) to original image size

    for i in range(len(boxes)):
        if len(boxes) > 0:
            boxes[i][:, :4] = scale_boxes(ims_shape[i].shape[1:], boxes[i][:, :4], im0s_shape[i].shape[:-1]) # .round()
    
        # min bbox filter
        if min_bbox_size:
            filtered = (boxes[i][:, [2, 3]] - boxes[i][:, [0, 1]] >= min_bbox_size).all(axis=1)
            boxes[i] = boxes[i][filtered]

        if masks:
            boxes[i] = boxes[i][:, :6]

        # if min_wh_ratio:
        #     filtered = ((boxes[i][:, 2] - boxes[i][:, 0]) / (boxes[i][:, 3] - boxes[i][:, 1]) >= min_wh_ratio).all(axis=1)
        
    return boxes



def scale_boxes(img1_shape, boxes, img0_shape, ratio_pad=None):
    # Rescale boxes (xyxy) from img1_shape to img0_shape

    if ratio_pad is None:  # calculate from img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    boxes[:, [0, 2]] -= pad[0]  # x padding
    boxes[:, [1, 3]] -= pad[1]  # y padding
    boxes[:, :4] /= gain

    # clip boxes
    boxes[:, [0, 2]] = boxes[:, [0, 2]].clip(0, img0_shape[1])  # x1, x2
    boxes[:, [1, 3]] = boxes[:, [1, 3]].clip(0, img0_shape[0])  # y1, y2
    return boxes


# @jit
def batched_nms(prediction, *, conf_thres=0.25, iou_thres=0.45, max_det=100, nm=0, v8=False):
    """Non-Maximum Suppression (NMS) on inference results to reject overlapping detections
    Returns:
         list of detections, on (n,6) tensor per image [xyxy, conf, cls]
    """

    if isinstance(prediction, (list, tuple)):  # YOLOv5 model in validation model, output = (inference_out, loss_out)
        prediction = prediction[0]  # select only inference output
    if v8:
        prediction = np.einsum('qwe->qew', prediction)
    bs = prediction.shape[0]  # batch size
    nc = prediction.shape[2] - nm - 4 if v8 else prediction.shape[2] - nm - 5 # number of classes

    if v8:
        mi = 4 + nc  # mask start index
        xc = np.amax(prediction[..., 4:mi], axis=-1) > conf_thres   #  (1, 8400)
    else:
        mi = 5 + nc  # mask start index
        xc = prediction[..., 4] > conf_thres  # candidates    # (1, 25200)


    assert 0 <= conf_thres <= 1, f'Invalid Confidence threshold {conf_thres}, valid values are between 0.0 and 1.0'
    assert 0 <= iou_thres <= 1, f'Invalid IoU {iou_thres}, valid values are between 0.0 and 1.0'

    # Settings
    max_wh = 7680  # (pixels) maximum box width and height
    max_nms = 30000  # maximum number of boxes into torchvision.ops.nms()
    time_limit = 0.5 + 0.05 * bs  # seconds to quit after
    t = time.time()
    output = [np.zeros((0, 6 + nm), dtype=np.float32)] * bs

    for xi, x in enumerate(prediction):  # image index, image inference
        x = x[xc[xi]]  # confidence

        # If none remain process next image
        if not x.shape[0]:
            continue

        if not v8:
            x[:, 5:] *= x[:, 4:5]  # conf = obj_conf * cls_conf

        # Box/Mask
        box = xywh2xyxy(x[:, :4])  # center_x, center_y, width, height) to (x1, y1, x2, y2)
        mask = x[:, mi:]  # zero columns if no masks

        # Detections matrix nx6 (xyxy, conf, cls)
        if v8:
            conf, j = x[:, 4:mi].max(1, keepdims=True), x[:, 4:mi].argmax(1, keepdims=True).astype('float32')
        else:
            conf, j = x[:, 5:mi].max(1, keepdims=True), x[:, 5:mi].argmax(1, keepdims=True).astype('float32')
        x = np.concatenate((box, conf, j, mask), 1)[conf.reshape(-1) > conf_thres]


        # Check shape
        n = x.shape[0]  # number of boxes
        if not n:  # no boxes
            continue
        elif n > max_nms:  # excess boxes
            x = x[np.argsort(-x[:, 4][:max_nms])]
        else:
            x = x[np.argsort(-x[:, 4])]

        # Batched NMS
        c = x[:, 5:6] * max_wh  # classes
        boxes, scores = x[:, :4] + c, x[:, 4]  # boxes (offset by class), scores
        i = nms_vanil(boxes, scores, iou_thres)  # NMS

        # limit detections
        if i.shape[0] > max_det:  
            i = i[:max_det]
        output[xi] = x[i]

        # timer limits
        if (time.time() - t) > time_limit:
            CONSOLE.print("NMS time limit exceeded!")
            break  # time limit exceeded
    return output



def nms_vanil(boxes, scores, threshold):
    # vanilla nms

    boxes_area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
    keep_indices = []
    indices = scores.argsort()[::-1]
    while indices.size > 0:
        i = indices[0]
        keep_indices.append(i)
        w = np.maximum(0, np.minimum(boxes[:, 2][i], boxes[:, 2][indices[1:]]) - np.maximum(boxes[:, 0][i], boxes[:, 0][indices[1:]]))
        h = np.maximum(0, np.minimum(boxes[:, 3][i], boxes[:, 3][indices[1:]]) - np.maximum(boxes[:, 1][i], boxes[:, 1][indices[1:]]))
        intersection = w * h
        ious = intersection / (boxes_area[i] + boxes_area[indices[1:]] - intersection) 
        indices = indices[np.where(ious <= threshold)[0] + 1]
    return np.asarray(keep_indices)



def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y



def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=False, scaleFill=False, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, ratio, (dw, dh)









