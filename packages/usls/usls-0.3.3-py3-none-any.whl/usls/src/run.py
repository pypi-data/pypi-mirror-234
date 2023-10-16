from pathlib import Path
import rich
from omegaconf import OmegaConf, DictConfig
from datetime import datetime
from typing import Dict, List

from usls.src.utils import (
    CONSOLE, USLS, 
    # whats_in_directory, 
    # rename,
    # check_images_integrity,
    # dir_combine,
    # images_deduplicate
)


# def run_directory_info(args: DictConfig):
#     c = whats_in_directory(
#         directory=args.dir,
#         fmt=args.fmt,
#         recursive=not args.non_recursive,
#         case_insensitive=args.case_insensitive,
#         verbose=args.verbose
#     )

#     # display
#     table = rich.table.Table(
#         # title=f"[i]\n{Path(args.dir).resolve()}", 
#         title_style='left',
#         box=rich.box.ASCII2,  
#         # show_lines=True, 
#         show_header=True,
#         # caption=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
#         caption=f"[i]{Path(args.dir).resolve()}\n", 
#         caption_justify='center',
#         header_style='',
#         footer_style='',
#         show_footer=True,
#     )
#     table.add_column(
#         "Format", 
#         footer=f"files visible\nfiles hidden\ndirectory visible\ndirectory hidden", 
#         justify="left", 
#         no_wrap=True
#     )
#     table.add_column(
#         "Count", 
#         footer=f"{c['attrs']['nf']}\n{c['attrs']['nhf']}\n{c['attrs']['nd']}\n{c['attrs']['nhd']}", 
#         justify="right", 
#         no_wrap=True
#     )
#     for k, v in c['visible']['mapping_suffix'].items():
#         table.add_row('No suffix' if k == '' else f'.{k}', f"{len(v)}", end_section=False)
#     CONSOLE.print(table)




# def run_rename(args: DictConfig):
#     rename(
#         directory=args.dir, 
#         with_prefix=args.prefix,
#         with_num=args.number,
#         with_znum=args.zero_number,
#         with_random=args.random,
#         with_uuid=args.uuid,
#         with_time=args.time,
#         bits=args.bits,  # 16
#         least_zeros=args.least_zeros,
#         fmt=args.fmt,  # Default: all type files + dir, lower-case
#         case_insensitive=args.case_insensitive,   # false
#         include_subdirs=args.include_subdirs,  # false -> Only rename sub-dirs
#         only_subdirs=args.only_subdirs,
#         recursive=args.recursive,  # false
#         verbose=args.verbose,
#     )



# def run_check_images_integrity(args: DictConfig):
#     check_images_integrity(
#         directory_i=args.dir,
#         directory_o=args.output_dir,
#         fmt=args.fmt,  
#         case_sensitive=args.case_sensitive,   # false
#         recursive=not args.non_recursive,  # false
#         verbose=args.verbose
#     )


# def run_dir_combine(args: DictConfig):
#     dir_combine(
#         directory_i=args.dir,
#         directory_o=args.output_dir,
#         move=args.move,
#         fmt=args.fmt,  # Default: all type files + dir, lower-case
#         case_insensitive=args.case_insensitive,   # false
#         non_recursive=args.non_recursive,  # false
#         verbose=args.verbose,
#         delimiter=args.delimiter
#     )



# def run_deduplicate(args: DictConfig):
#     # usls = USLS()   # instance
#     # usls.deduplicate(
#     #     directory_i=args.dir,
#     #     directory_deprecated=args.deprecated_dir,
#     #     directory_duplicated=args.duplicated_dir,
#     #     fmt=args.fmt,  # Default: all type files + dir, lower-case
#     #     case_sensitive=args.case_sensitive,   # false
#     #     include_hidden=args.include_hidden,  # false! Hidden files should not be combined!
#     #     recursive=not args.non_recursive,  # true
#     #     base_method=args.base,
#     #     nn_method=args.nn,
#     #     threshold=args.thresh,
#     #     check_integrity_first=args.check_integrity_first,     # false
#     #     device=args.device,
#     #     verbose=True,
#     # )
#     images_deduplicate(
#         directory_i=args.dir,
#         directory_duplicated=args.output_dir,
#         fmt=args.fmt,  # Default: all type files + dir, lower-case
#         case_sensitive=args.case_sensitive,   # false
#         recursive=not args.non_recursive,  # true
#         base_method=args.base,
#         nn_method=args.nn,
#         threshold=args.thresh,
#         device=args.device,
#         verbose=args.verbose,
#     )
