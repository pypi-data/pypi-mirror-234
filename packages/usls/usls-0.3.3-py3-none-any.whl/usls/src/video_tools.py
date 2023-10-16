import cv2
import os
import rich
from tqdm import tqdm
import argparse
from pathlib import Path
import sys
from omegaconf import OmegaConf, DictConfig
from datetime import datetime


from usls.src.utils import CONSOLE, IMG_FORMAT, VIDEO_FORMAT, LABEL_FORMAT, smart_path



def play_and_record(
        source,
        delay=1, 
        flip=None,
        rotate=None,
        view=True,
        fourcc='mp4v',
        record=False,
        output_dir=None,
    ):
    # video play & record

    # check file
    if Path(source).is_file():
        # raise TypeError(f"{source} is not a valid file.")
        # sys.exit()
        
        # check format
        if not Path(source).suffix in VIDEO_FORMAT:
            raise TypeError(f"{source} is supported video format: {VIDEO_FORMAT}.")
            sys.exit()



    CONSOLE.print(f"Source: {Path(source).resolve()}")


    # flip and rotate
    if flip:
        if flip == 'ud':
            flipCode = 0
        elif flip == 'lr':
            flipCode = 1
        elif flip in('udlr', 'lrud'):
            flipCode = -1


    if rotate:
        if rotate == 90:
            rotateCode = cv2.ROTATE_90_CLOCKWISE
        elif rotate == 180:
            rotateCode = cv2.ROTATE_180
        elif rotate == 270:
            rotateCode = cv2.ROTATE_90_COUNTERCLOCKWISE


    videoCapture = cv2.VideoCapture(source)  # video capture
    fps = int(videoCapture.get(cv2.CAP_PROP_FPS))
    w = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # video_size = (w, h)
    # fourcc_ = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc_ = cv2.VideoWriter_fourcc(*fourcc)
    CONSOLE.print(f"Info: width={w}, height={h}, fps={fps}, fourcc={fourcc_}")


    # record flag
    do_rec = record

    # rec 
    if do_rec:
        CONSOLE.print(f"Rec...")
        save_dir = smart_path(
            Path(output_dir) / datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), 
            exist_ok=False, 
            sep='-'
        )  # increment dir
        save_dir.mkdir(parents=True, exist_ok=True)
        saveout = save_dir / 'rec.mp4' 
        video_writer = cv2.VideoWriter(str(saveout), fourcc_, fps, (w, h))  # build video writer


    while True:
        ret, frame = videoCapture.read()
        if ret:

            if flip:
                frame = cv2.flip(frame, flipCode)
            if rotate:
                frame = cv2.rotate(frame, rotateCode)
            if view:
                frame_s = frame
                   
                # rec notice
                # text_rec = "Press r to record"
                # line_thickness = 1
                # fontScale = 0.8
                # w_text, h_text = cv2.getTextSize(text_rec, 0, fontScale=fontScale, thickness=line_thickness)[0]  # text width, height
                # tl = (frame_s.shape[1]//30, frame_s.shape[0]//10)
                # br =(frame_s.shape[1]//30 + w_text, frame_s.shape[0]//10 - h_text)
                # cv2.rectangle(
                #     frame_s, 
                #     tl, br, 
                #     (0,0,0), 
                #     -1, 
                #     cv2.LINE_AA
                # )  # filled
                # cv2.putText(
                #     frame_s, 
                #     text_rec, 
                #     tl, 
                #     cv2.FONT_HERSHEY_SIMPLEX, 
                #     fontScale,
                #     (255,255,255), 
                #     thickness=line_thickness, 
                #     lineType=cv2.LINE_AA
                # )
                cv2.imshow('frame', frame_s)
            
            # rec
            if do_rec:
                video_writer.write(frame)

            # key detect
            key = cv2.waitKey(delay)

            # esc -> quit
            if key == 27:

                if do_rec:    
                    CONSOLE.print(f"Record saved at: {saveout.resolve()}")

                break

            # r -> record
            if key == ord('r'):
                do_rec = not do_rec   # ~  

                # rec 
                if do_rec:
                    CONSOLE.print(f"Rec...")

                    save_dir = smart_path(
                        Path(output_dir) / datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), 
                        exist_ok=False, 
                        sep='-'
                    )  # increment dir
                    save_dir.mkdir(parents=True, exist_ok=True)
                    saveout = save_dir / 'rec.mp4' 
                    video_writer = cv2.VideoWriter(str(saveout), fourcc_, fps, (w, h))

                else:
                    CONSOLE.print(f"Record saved at: {saveout.resolve()}")
        else:
            break


    # release cap & video cap
    videoCapture.release()
    if view:
        cv2.destroyAllWindows()



def v2is(
        source,      
        output_dir,  
        x=20,         # every 20 frame  to save
        flip=None,
        rotate=None,
        img_fmt=".jpg",
        view=False,
        verbose=True,
    ):
    # video clipping

    # check file
    if not Path(source).is_file():
        raise TypeError(f"{source} is not a valid file.")
        sys.exit()

    # check format
    if not Path(source).suffix in VIDEO_FORMAT:
        raise TypeError(f"{source} is supported video format: {VIDEO_FORMAT}.")
        sys.exit()


    # image dir name
    image_dir = Path(source).stem

    # flip and rotate
    if flip:
        if flip == 'ud':
            flipCode = 0
            image_dir += '-flipud'
        elif flip == 'lr':
            flipCode = 1
            image_dir += '-fliplr'
        elif flip in('udlr', 'lrud'):
            flipCode = -1
            image_dir += '-flipudlr'


    if rotate:
        if rotate == 90:
            rotateCode = cv2.ROTATE_90_CLOCKWISE
            image_dir += '-rotate90'
        elif rotate == 180:
            rotateCode = cv2.ROTATE_180
            image_dir += '-rotate180'
        elif rotate == 270:
            rotateCode = cv2.ROTATE_90_COUNTERCLOCKWISE
            image_dir += '-rotate270'



    # frame count
    idx = 0 

    # save_dir 
    save_dir = smart_path(
        Path(output_dir) / image_dir,
        exist_ok=False, 
        sep='-'
    )  # increment run
    save_dir.mkdir(parents=True, exist_ok=True)  # make dir


    # load video
    cap = cv2.VideoCapture(str(source))

    
    while True:
        ret, frame = cap.read()
        if ret == True:
            if flip:    # flip frame
                frame = cv2.flip(frame, flipCode)   
            if rotate:      # rotate
                frame = cv2.rotate(frame, rotateCode)
            if view:  # show video      
                cv2.imshow('video', frame)

            # clipping
            if idx % x == 0:                
                # img_saveout = save_dir / (Path(source).stem + '_' + str(idx) + img_fmt)
                img_saveout = save_dir / (str(idx) + img_fmt)
                cv2.imwrite(str(img_saveout), frame)
            
            idx += 1    # frame index counting
            if cv2.waitKey(1) & 0xFF == ord('q'):   # 'q' to quit
                break
        else:
            break

    
    cap.release()  # release cap
    if view:  # close opencv windows if opened.
        cv2.destroyAllWindows()


    # success info
    if verbose:
        CONSOLE.print(f"Saved at: {save_dir.resolve()}")




def vs2is(
        directory,      
        output_dir,  
        x=20,       
        flip=None,
        rotate=None,
        img_fmt=".jpg",
        view=False,
    ):
    # videos -> images


    # video list
    video_list = [x for x in Path(directory).glob('**/*') if x.suffix in VIDEO_FORMAT]
    # CONSOLE.print(f"{len(video_list)} videos found.")


    # if empty dir, stop
    if len(video_list) == 0:
        CONSOLE.print(f"No video found.")
        sys.exit()


    # split videos one by one
    for video in tqdm(video_list, desc=f"videos -> images"):
        v2is(
            source=video,           
            output_dir=output_dir,      # save dir
            x=x,
            view=view,
            flip=flip,
            img_fmt=img_fmt,
            verbose=False,
        )

    # success info
    CONSOLE.print(f"Saved at: {Path(output_dir).resolve()}")



# -----------------------------------------------------------------------------
#  run
# -----------------------------------------------------------------------------

def run_v2is(args: DictConfig):

    with CONSOLE.status("[bold green]Video Clipping...", spinner='line') as status:
        v2is(
            source=args.source,      
            output_dir=args.output_dir,  
            x=args.frame,       
            flip=args.flip,
            rotate=args.rotate,
            img_fmt=args.fmt_img,
            view=args.view,
        )


def run_vs2is(args: DictConfig):

    # with CONSOLE.status("[bold green]Video Clipping...", spinner='line') as status:
    vs2is(
        directory=args.dir,      
        output_dir=args.output_dir,  
        x=args.frame,       
        flip=args.flip,
        rotate=args.rotate,
        img_fmt=args.fmt_img,
        view=args.view,
    )


def run_play(args: DictConfig):
    with CONSOLE.status("[green]Playing...\n") as status:

        play_and_record(
            source=args.source,
            delay=args.delay, 
            flip=args.flip,
            rotate=args.rotate,
            view=not args.no_view,
            fourcc=args.fourcc,
            record=args.rec,
            output_dir=args.output_dir,
        )



