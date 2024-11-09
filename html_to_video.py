import os
import cv2
import numpy as np
import concurrent.futures
from . import utils
from . import render


def create_video_from_htmls(
        html_file_paths,
        video_file_path,
        threads=None,
        script_to_append=None,
        append_inplace=False,
        fps=5,
        width_height=None,
        render_wait_max=30,
        post_render_wait=0.2,
        ):
    '''
    Create a video from a list of HTML files.
    '''
    pngs = create_pngs(
        html_file_paths,
        threads=threads,
        script_to_append=script_to_append,
        inplace=append_inplace,
        render_wait_max=render_wait_max,
        post_render_wait=post_render_wait,
        )
    create_video(
        pngs,
        video_file_path,
        fps=fps,
        width_height=width_height,
        )


def create_pngs(
        html_file_paths,
        threads=None,
        script_to_append=None,
        append_inplace=False,
        render_wait_max=30,
        post_render_wait=0.2,
        ):
    '''
    Render a list of HTML files to PNGs.
    '''
    threads = threads or os.cpu_count()
    if script_to_append and not append_inplace:
        html_file_paths = utils.create_temp_files(html_file_paths)
    if script_to_append:
        utils.append_script(html_file_paths, script_to_append)

    batches = utils.batch_files(html_file_paths, threads)
    pngs = []
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=threads) as executor:
        done = executor.map(
            render.pngify_batch,
            batches,
            [render_wait_max] * len(batches),
            [post_render_wait] * len(batches)
        )
        for batch in done:
            pngs.extend(batch)
    return pngs


def create_video(
        pngs,
        video_file_path,
        fps=5,
        width_height=None,
        ):
    '''
    Create a video from a list of PNGs.
    '''
    imgs = [cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)
            for png in pngs]
    height, width, _ = width_height or imgs[0].shape
    video = cv2.VideoWriter(video_file_path, 0, fps, (width, height))

    for png in pngs:
        nparr = np.frombuffer(png, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        video.write(img)

    video.release()
