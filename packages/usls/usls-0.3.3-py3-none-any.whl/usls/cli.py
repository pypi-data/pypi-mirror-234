import sys
import rich
import re
from omegaconf import OmegaConf, DictConfig
import argparse
from enum import Enum, auto, unique
from rich.panel import Panel
from typing import Dict, List, Union, Optional, Any


from usls import __version__
from usls.src.utils import (
	CONSOLE, IMG_FORMAT, LABEL_FORMAT, VIDEO_FORMAT, gen_emojis
)
# from usls.src.run import (   
	# run_directory_info, 
	# run_rename,
	# run_check_images_integrity, 
	# run_dir_combine, 
	# run_deduplicate,
# )  # all runs


from usls.src.labelling import run_marker
# from usls.src.cleanup import run_cleanup
from usls.src.spider import run_spider
from usls.src.video_tools import run_v2is, run_vs2is, run_play 

# ---------------------------------------------------------------------------------------------



def run(opt: DictConfig):
    task_mapping = {
        # 'dir-info': run_directory_info,   # directory info
        # 'rename': run_rename,  # rename
        # 'check': run_check_images_integrity,  # check images integrity  
        # 'dir-combine': run_dir_combine,  # dir-combined
        # 'cleanup': run_cleanup,
        # 'dedu': run_deduplicate, 

        # not now
        'mark': run_marker,
        'spider': run_spider,
        # 'v2is': run_v2is,
        'vs2is': run_vs2is,
        'play': run_play,
    }.get(opt.task)(opt)





def cli() -> None:
	if len(sys.argv) == 1:
		sys.argv.append('-h')

	# CONSOLE.print(_logo)
	args = parse_cli()
	args.update({'task': sys.argv[1]})  # add task
	args = OmegaConf.create(args)
	
	# log
	CONSOLE.print(
		Panel(
			f"[b]{OmegaConf.to_yaml(args)}",
			# f"{args}",
			title='args',
			box=rich.box.ROUNDED,
		)
	)

	# run
	run(args) 	



def parse_cli() -> Dict:

	parser = argparse.ArgumentParser(
		prog='usls',
		description=gen_emojis(),
		epilog=f'version: {__version__} '
	)
	parser.add_argument(
		'--version', '-v', '-V', 
		action='version', 
		version=f'version: {__version__}',
		help='get version',
	)

	subparsers = parser.add_subparsers(
		# title='Tasks',
		description=gen_emojis(),
		help=gen_emojis()
	)

	# # ------------------------------------
	# # 	✅  directory info parser 
	# # ------------------------------------
	# info_parser = subparsers.add_parser(name='dir-info', help=gen_emojis())
	# info_parser.add_argument(
	# 	'--dir',
	# 	required=True, type=str, default=None, help='Directory input'
	# )
	# info_parser.add_argument(
	# 	'--fmt',
	# 	required=False, type=str, nargs="+", default=[], help=f'File format, default [] means everything.'
	# )
	# info_parser.add_argument(
	# 	'--non-recursive',
	# 	required=False, action='store_true', help="Non-recursive, do not iterable all directories"
	# )
	# info_parser.add_argument(
	# 	'--case-insensitive',
	# 	required=False, action='store_true', help="Case sensitive"
	# )
	# info_parser.add_argument(
	# 	'--verbose',
	# 	required=False, action='store_true', help="Show more info"
	# )	


	# # ---------------------
	# # 	✅ rename parser  
	# # ---------------------
	# rename_parser = subparsers.add_parser(name='rename', help=gen_emojis())
	# rename_parser.add_argument(
	# 	'--dir',
	# 	required=True, type=str, default=None, help='Directory input'
	# )
	# rename_parser.add_argument(
	# 	'--bits',
	# 	required=False, type=int, default=16, help='length of random string'
	# )
	# rename_parser.add_argument(
	# 	'--fmt',
	# 	required=False, type=str, nargs="+", default=[], help=f'File format, default [] -> everything.'
	# )
	# rename_parser.add_argument(
	# 	'--recursive',
	# 	required=False, action='store_true', help="iterable all sub-directories"
	# )
	# rename_parser.add_argument(
	# 	'--case-insensitive',
	# 	required=False, action='store_true', help=""
	# )
	# rename_parser.add_argument(
	# 	'--include-subdirs',
	# 	required=False, action='store_true',  help=""
	# )	
	# rename_parser.add_argument(
	# 	'--only-subdirs',
	# 	required=False, action='store_true',  help=""
	# )		
	# rename_parser.add_argument(
	# 	'--least-zeros',
	# 	required=False, action='store_true',  help=""
	# )	   
	# rename_parser.add_argument(
	# 	'--verbose', 
	# 	action='store_true', required=False, help='Show more info'
	# )
	# rename_group = rename_parser.add_mutually_exclusive_group(required=True)
	# rename_group.add_argument(
	# 	'--zero-number', '--znum',
	# 	action='store_true', required=False, help=''
	# )
	# rename_group.add_argument(
	# 	'--number', '--num',
	# 	action='store_true', required=False, help=''
	# )
	# rename_group.add_argument(
	# 	'--random', 
	# 	action='store_true', required=False, help=''
	# )
	# rename_group.add_argument(
	# 	'--uuid', '--uuid4', 
	# 	action='store_true', required=False, help=''
	# )
	# rename_group.add_argument(
	# 	'--time',
	# 	action='store_true', required=False, help=''
	# )	
	# rename_group.add_argument(
	# 	'--prefix',
	# 	required=False, type=str, default=None, help=''
	# )

	# -------------------------------------------
	#  ✅ check images integrity parser
	# -------------------------------------------
	# check_images_integrity_parser = subparsers.add_parser(
	# 	name='check', 
	# 	# aliases=['check-images'], 
	# 	help=gen_emojis()
	# )
	# check_images_integrity_parser.add_argument(
	# 	'--dir',
	# 	required=True, type=str, default=None, help='Directory to be combined'
	# )
	# check_images_integrity_parser.add_argument(
	# 	'--output-dir', '--out',
	# 	required=False, type=str, default='output-deprecated', help='Directory saveout'
	# )
	# check_images_integrity_parser.add_argument(
	# 	'--fmt',
	# 	required=False, type=str, nargs="+", 
	# 	default=IMG_FORMAT, 
	# 	help=f'File format, default IMG_FORMAT.'
	# )
	# check_images_integrity_parser.add_argument(
	# 	'--non-recursive',
	# 	required=False, action='store_true', 
	# 	help="Non-recursive, do not iterable all directories"
	# )
	# check_images_integrity_parser.add_argument(
	# 	'--case-sensitive',
	# 	required=False, action='store_true', 
	# 	help=""
	# )
	# check_images_integrity_parser.add_argument(
	# 	'--verbose',
	# 	required=False, action='store_true', 
	# 	help=""
	# )


	# -----------------------------
	# 	dir_combine parser✅
	# -----------------------------
	# dir_combine_parser = subparsers.add_parser(
	# 	name='dir-combine', 
	# 	# aliases=['dir_combine'], 
	# 	help=gen_emojis()
	# )
	# dir_combine_parser.add_argument(
	# 	'--dir',
	# 	required=True, type=str, default=None, help='Directory to be combined'
	# )
	# dir_combine_parser.add_argument(
	# 	'--output-dir', '--out',
	# 	required=False, type=str, default='output-all-combined', help='Directory saveout'
	# )
	# dir_combine_parser.add_argument(
	# 	'--delimiter',
	# 	required=False, type=str, default='-', help='Directory saveout'
	# )
	# dir_combine_parser.add_argument(
	# 	'--move',
	# 	required=False, action='store_true', 
	# 	help='copy or move, default is copy.'
	# )
	# dir_combine_parser.add_argument(
	# 	'--fmt',
	# 	required=False, type=str, nargs="+", 
	# 	default=[], 
	# 	help=f'File format, default [] -> everything.'
	# )
	# dir_combine_parser.add_argument(
	# 	'--non-recursive',
	# 	required=False, action='store_true', 
	# 	help="Non-recursive, do not iterable all directories"
	# )
	# dir_combine_parser.add_argument(
	# 	'--case-insensitive',
	# 	required=False, action='store_true', 
	# 	help=""
	# )
	# dir_combine_parser.add_argument(
	# 	'--verbose',
	# 	required=False, action='store_true', 
	# 	help=''
	# )


	# --------------------------
	# 	✅ de-duplicator parser  
	# --------------------------
	# de_duplicate_parser = subparsers.add_parser(
	# 	name='dedu', 
	# 	# aliases=['de-duplicate'], 
	# 	help=gen_emojis()
	# )
	# de_duplicate_parser.add_argument(
	# 	'--dir',
	# 	required=True, type=str, default=None, 
	# 	help='Images Directory'
	# )
	# de_duplicate_parser.add_argument(
	# 	'--output-dir', '--out',
	# 	# '--duplicated-dir',
	# 	required=False, type=str, default='output-duplicated', 
	# 	help='Duplicated Items Directory'
	# )
	# de_duplicate_parser.add_argument(
	# 	'--device',
	# 	required=False, type=int, default=0, 
	# 	help='using cpu/gpu device, --device 0(GPU default)'
	# )
	# de_duplicate_parser.add_argument(
	# 	'--thresh',
	# 	required=False, type=float, default=0.98, 
	# 	help='Based on nn, --thresh 0.98(default)'
	# )	
	# de_duplicate_parser.add_argument(
	# 	'--fmt',
	# 	required=False, type=str, nargs="+", 
	# 	default=IMG_FORMAT, 
	# 	help=f'File format, default [] -> everything.'
	# )
	# de_duplicate_parser.add_argument(
	# 	'--non-recursive',
	# 	required=False, action='store_true', 
	# 	help="Non-recursive, do not iterable all directories"
	# )
	# de_duplicate_parser.add_argument(
	# 	'--case-sensitive',
	# 	required=False, action='store_true', 
	# 	help=""
	# )
	# de_duplicate_parser.add_argument(
	# 	'--verbose',
	# 	required=False, action='store_true', 
	# 	help=''
	# )
	# de_duplicate_group = de_duplicate_parser.add_mutually_exclusive_group(
	# 	required=True
	# )
	# de_duplicate_group.add_argument(
	# 	'--base',
	# 	action='store_true',
	# 	required=False,
	# 	help='Method based on MD5, simple but more accurately.(Support .txt files at the same time)'
	# )
	# de_duplicate_group.add_argument(
	# 	'--nn',
	# 	action='store_true',
	# 	required=False, 
	# 	help='Method based on nn similarity, with --conf, more faster (recommended)'
	# )


	# ---------------------
	# 	cleanup parser  ✅
	# ---------------------
	# cleanup_parser = subparsers.add_parser(
	# 	name='cleanup', 
	# 	# aliases=['cleanup'], 
	# 	help=gen_emojis()
	# )
	# cleanup_parser.add_argument(
	# 	'--img-dir', 
	# 	required=True, type=str, default=None, 
	# 	help='image dir'
	# )
	# cleanup_parser.add_argument(
	# 	'--label-dir',
	# 	required=False, type=str, default=None, 
	# 	help='label dir'
	# )
	# cleanup_parser.add_argument(
	# 	'--fmt-img',
	# 	required=False, type=str, default=IMG_FORMAT, 
	# 	help=f'image format: {IMG_FORMAT}'
	# )	
	# cleanup_parser.add_argument(
	# 	'--fmt-label',
	# 	required=False, type=str, default=LABEL_FORMAT, 
	# 	help=f'label format: {LABEL_FORMAT}'
	# )
	# cleanup_parser.add_argument(
	# 	'--filtered-dir',
	# 	required=False, type=str, default='cleanup-filtered', help='filtered dir'
	# )	
	# cleanup_parser.add_argument(
	# 	'--keep-empty-label',
	# 	action='store_true', 
	# 	help='keep empty label file or not'
	# )
	# cleanup_parser.add_argument(
	# 	'--non-recursive',
	# 	required=False, action='store_true', 
	# 	help="Do not iterable all directories"
	# )


	# ---------------------
	# 	spider parser  ✅
	# ---------------------
	spider_parser = subparsers.add_parser(
		name='spider', 
		help=gen_emojis()
	)
	spider_parser.add_argument(
		'--words', 
		default='', nargs="+", required=True, type=str, 
		help='Key words'
	)
	spider_parser.add_argument(
		'--output-dir',
		required=False, type=str, default='baidu-image-spider', help='baidu image spider output dir'
	)	




	# ---------------------
	# 	v2is parser   ✅
	# ---------------------
	# v2is_parser = subparsers.add_parser(
	# 	name='v2is', 
	# 	help=gen_emojis()
	# )
	# v2is_parser.add_argument(
	# 	'--source', '--video', '-v',
	# 	required=True, type=str, default=None, 
	# 	help='Video source input'
	# )
	# v2is_parser.add_argument(
	# 	'--output-dir',
	# 	required=False, type=str, default='v2is', 
	# 	help='Saveout Directory'
	# )	
	# v2is_parser.add_argument(
	# 	'--frame', '--interval',
	# 	required=False, type=int, default=10, 
	# 	help='Frame interval'
	# )	
	# v2is_parser.add_argument(
	# 	'--fmt-img',
	# 	required=False, type=str, default='.jpg', 
	# 	help='Image clipped format'
	# )		
	# v2is_parser.add_argument(
	# 	'--view',
	# 	action='store_true',
	# 	required=False, 
	# 	help='View when clipping'
	# )
	# v2is_parser.add_argument(
	# 	'--flip',
	# 	required=False, type=str, default=None,
	# 	choices=['ud', 'lr', 'udlr', 'lrud'],
	# 	help='Flipping video'
	# )
	# v2is_parser.add_argument(
	# 	'--rotate',
	# 	required=False, type=int, default=None,
	# 	choices=[90, 180, 270],
	# 	help='Counterwise Rotation'
	# )

	# ---------------------
	# 	vs2is parser   ✅
	# ---------------------
	vs2is_parser = subparsers.add_parser(
		name='vs2is', 
		help=gen_emojis()
	)
	vs2is_parser.add_argument(
		'--dir', '--source', '--video', '-v',
		required=True, type=str, default=None, 
		help='Video source input'
	)
	vs2is_parser.add_argument(
		'--output-dir',
		required=False, type=str, default='vs2is', 
		help='Saveout Directory'
	)	
	vs2is_parser.add_argument(
		'--frame', '--interval',
		required=False, type=int, default=10, 
		help='Frame interval'
	)	
	vs2is_parser.add_argument(
		'--fmt-img',
		required=False, type=str, default='.jpg', 
		help='Image clipped format'
	)		
	vs2is_parser.add_argument(
		'--view',
		action='store_true',
		required=False, 
		help='View when clipping'
	)
	vs2is_parser.add_argument(
		'--flip',
		required=False, type=str, default=None,
		choices=['ud', 'lr', 'udlr', 'lrud'],
		help='Flipping video'
	)
	vs2is_parser.add_argument(
		'--rotate',
		required=False, type=int, default=None,
		choices=[90, 180, 270],
		help='Counterwise Rotation'
	)

	# ---------------------------------
	# 	video play & record parser   ✅
	# ---------------------------------
	play_rec_parser = subparsers.add_parser(
		name='play', 
		help=gen_emojis()
	)
	play_rec_parser.add_argument(
		'--source', '--video', '-v',
		required=True, type=str, default=None, 
		help='Video source input'
	)
	play_rec_parser.add_argument(
		'--output-dir',
		required=False, type=str, default='video-records', 
		help='Saveout Directory'
	)	
	play_rec_parser.add_argument(
		'--delay',
		required=False, type=int, default=1, 
		help='Keywait'
	)	
	play_rec_parser.add_argument(
		'--fourcc',
		required=False, type=str, default='mp4v', 
		help='Image clipped format'
	)		
	play_rec_parser.add_argument(
		'--no-view',
		action='store_true',
		required=False, 
		help='Do not view while playing'
	)
	play_rec_parser.add_argument(
		'--rec',
		action='store_true',
		required=False, 
		help='Record at the start'
	)
	play_rec_parser.add_argument(
		'--flip',
		required=False, type=str, default=None,
		choices=['ud', 'lr', 'udlr', 'lrud'],
		help='Flipping video'
	)
	play_rec_parser.add_argument(
		'--rotate',
		required=False, type=int, default=None,
		choices=[90, 180, 270],
		help='Counterwise Rotation'
	)


	# ---------------------
	# 	inspect parser  ✅
	# ---------------------
	inspect_parser = subparsers.add_parser(
		name='mark', # aliases=['label-det'], 
		help=gen_emojis()
	)
	inspect_parser.add_argument(
		'--input', '-i',
		required=True, type=str, default=None, help='input dir'
	)
	inspect_parser.add_argument(
		'--classes', '-c', 
		default=None, nargs="+",
		 required=False, type=str, 
		 help='classes list'
	)
	inspect_parser.add_argument(
		'--kpts-classes', '-kc',
		default=None, nargs="+",
		 required=False, type=str, 
		 help='kpts classes list'
	)

	# inspect_parser.add_argument(
	# 	'--label-dir',
	# 	required=False, type=str, default=None, help='label dir'
	# )
	# inspect_parser.add_argument(
	# 	'--depreacated-dir', 
	# 	required=False, type=str, default="deprecated-images", help='deprecated image dir'
	# )
	# inspect_parser.add_argument('--window-width', default=800, type=int, help='opencv windows width')
	# inspect_parser.add_argument('--window-height', default=600, type=int, help='opencv windows height')
	# inspect_parser.add_argument(
	# 	'--no-qt',
	# 	action='store_true',
	# 	required=False, 
	# 	help='without QT'
	# )

	args = vars(parser.parse_args())
	return args




if __name__ == '__main__':
	cli()
