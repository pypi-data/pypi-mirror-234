# Copyright (c) 2023 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import asyncio                          # concurrency
import concurrent.futures               # multithreading
import inspect
from KFSfstr import KFSfstr
from KFSlog import KFSlog
import logging
import PIL, PIL.Image, PIL.ImageFile    # conversion to PDF
import os
import requests
import time
import typing                           # function type hint


class ConversionError(Exception):
    pass

def convert_images_to_PDF(images_filepath: list[str], PDF_filepath: str|None=None, if_success_delete_images: bool=True) -> list[PIL.Image.Image]:
    """
    Converts images at filepaths to PDF and returns PDF. Upon failure exception will contain list of filepaths that failed.

    Arguments:
    - images_filepath: filepaths to the images to convert and merge to PDF
    - PDF_filepath: if not None, tries to save PDF at filepath
    - if_success_delete_images: if conversion successful cleans up the source images

    Returns:
    - PDF: converted PDF

    Raises:
    - ConversionError: Converting \"{image_filepath}\" to PDF failed, because image could not be found or is corrupted. Exception contains list of filepaths that failed.
    """

    conversion_failures_filepath: list[str]=[]  # conversion failures
    logger: logging.Logger                      # logger
    PDF: list[PIL.Image.Image]=[]               # images converted for saving as pdf
    success: bool=True                          # conversion successful?


    images_filepath=list(images_filepath)
    PDF_filepath=str(PDF_filepath)

    if 1<=len(logging.getLogger("").handlers):  # if root logger defined handlers:
        logger=logging.getLogger("")            # also use root logger to match formats defined outside KFS
    else:                                       # if no root logger defined:
        logger=KFSlog.setup_logging("KFS")      # use KFS default format
    
    PIL.ImageFile.LOAD_TRUNCATED_IMAGES=True    # set true or raises unnecessary exception sometimes


    logger.info("Converting images to PDF...")
    for image_filepath in images_filepath:                              # convert all saved images
        try:
            with PIL.Image.open(image_filepath) as image_file:          # open image
                PDF.append(image_file.convert("RGBA").convert("RGB"))   # convert, append to PDF

        except FileNotFoundError:                               # if user gave wrong filepath:
            success=False                                       # conversion not successful
            logger.error(f"Converting \"{image_filepath}\" to PDF failed, because image could not be found.")
            conversion_failures_filepath.append(image_filepath) # append to failure list so parent function can retry downloading
        
        except PIL.UnidentifiedImageError:                      # if image is corrupted, earlier download may have failed:
            success=False                                       # conversion not successful
            logger.error(f"Converting \"{image_filepath}\" to PDF failed, because image is corrupted.")
            conversion_failures_filepath.append(image_filepath) # append to failure list so parent function can retry downloading

            for i in range(3):  # try to delete corrupt image
                logger.info(f"Deleting corrupted image \"{image_filepath}\"...")
                try:
                    os.remove(image_filepath)   # remove image, redownload later
                except PermissionError:         # if could not be removed: try again, give up after try 3
                    if i<2:
                        logger.error(f"\rDeleting corrupted image \"{image_filepath}\" failed. Retrying after waiting 1s...")
                        time.sleep(1)
                        continue
                    else:                       # if removing corrupted image failed after 10th try: give hentai up
                        logger.error(f"\rDeleting corrupted image \"{image_filepath}\" failed 3 times. Giving up.")
                else:
                    logger.info(f"\rDeleted corrupted image \"{image_filepath}\".")
                    break                       # break out of inner loop, but keep trying to convert images to PDF to remove all other corrupt images in this function call already and not later
    
    if success==False:  # if unsuccessful: throw exception with failure list
        raise ConversionError(conversion_failures_filepath)
    else:
        logger.info("\rConverted images to PDF.")


    if PDF_filepath!=None:   # if filepath given: save PDF
        logger.info(f"Saving \"{PDF_filepath}\"...")
        PDF[0].save(PDF_filepath, save_all=True, append_images=PDF[1:])
        logger.info(f"\rSaved \"{PDF_filepath}\".")

    if if_success_delete_images==True:    # try to delete all source images if desired
        for image_filepath in images_filepath:
            try:
                os.remove(image_filepath)
            except PermissionError:
                logger.error(f"Deleting \"{image_filepath}\" failed. Skipping image.")

    return PDF  # return PDF in case needed internally


def download_media_default(media_URL: str, media_filepath: str|None=None) -> bytes:
    """
    Downloads media from URL and saves it in media_filepath. Default worker function for download_medias(...).

    Arguments:
    - media_URL: direct media URL to download media from. For custom website scraping, implement custom worker function.
    - media_filepath: media filepath to save media at

    Returns:
    - media: downloaded media

    Raises:
    - requests.HTTPError: media_URL did not return status ok.
    """

    media: bytes    # media downloaded


    media_URL=str(media_URL)
    if media_filepath!=None:
        media_filepath=str(media_filepath)

    page=requests.get(media_URL)    # download media, exception handling outside
    if page.ok==False:              # if something went wrong: exception handling outside
        raise requests.HTTPError(response=page)
    media=page.content              # if everything ok: copy media


    if media_filepath!=None:                            # if media should be saved
        with open(media_filepath, "wb") as media_file:  # save media
            media_file.write(media)

    return media


async def download_media_default_async(media_URL: str, media_filepath: str|None=None) -> bytes:
    """
    Downloads media from URL and saves it in media_filepath. Default worker function for download_medias_async(...).

    Arguments:
    - media_URL: direct media URL to download media from. For custom website scraping, implement custom worker function.
    - media_filepath: media filepath to save media at

    Returns:
    - media: downloaded media

    Raises:
    - requests.HTTPError: media_URL did not return status ok.
    """

    return download_media_default(media_URL, media_filepath)    # TODO use aiohttp to actually make asynchronous downloads


def download_medias(medias_URL: list[str], medias_filepath: list[str|None],
                    worker_function: typing.Callable=download_media_default, workers_max: int|None=None,
                    **kwargs) -> list[bytes]: 
    """
    Downloads medias from medias_URL and saves as specified in medias_filepath. Exceptions from worker function will not be catched. If file already exists at media filepath, assumes that this media has already been downloaded and does not redownload it. Also loads it and uses it in return list.

    Arguments:
    - medias_URL: media URL to download media from. If no custom worker_function is defined, uses download_media_default(...) and expects direct media URL.
    - medias_filepath: media filepaths to save medias at. Must have same length as medias_URL. If an entry is None, does not try to save that media.
    - worker_function: function to download 1 particular media. Must at least take parameters "media_URL" and "media_filepath". Additional **kwargs are forwarded.
    - workers_max: maximum number of worker threads at the same time. Use 1 for single thread operation and None for unrestricted number of workers.
    - **kwargs: additional keyword arguments to forward to custom worker function, no *args so user is forced to accept media_URL and media_filepath and no confusion ensues because of unexpected parameter passing

    Returns:
    - medias: downloaded or loaded medias

    Raises:
    - DownloadError: Downloading media \"{medias_URL[i]}\" failed. Exception contains list of URL that failed.
    - ValueError: Length of medias_URL and medias_filepath must be the same.
    """

    download_failures_URL: list[str]=[]                             # download failures
    medias: list[None|bytes]=[None for _ in range(len(medias_URL))] # medias downloaded or loaded, order should be kept even if multithreaded that's why initialised with None and results are placed at correct i
    medias_downloaded_count: int=0                                  # how many already loaded or downloaded
    medias_downloaded_count_old: int=0                              # how many already loaded or downloaded in iteration previous
    logger: logging.Logger                                          # logger
    success: bool=True                                              # download successful?
    threads: list[concurrent.futures.Future|None]=[]                # worker threads for download, None means no worker thread was necessary for that media, used to keep media order
    

    medias_URL=list(medias_URL)
    medias_filepath=list(medias_filepath)

    if 1<=len(logging.getLogger("").handlers):  # if root logger defined handlers:
        logger=logging.getLogger("")            # also use root logger to match formats defined outside KFS
    else:                                       # if no root logger defined:
        logger=KFSlog.setup_logging("KFS")      # use KFS default format

    if len(medias_URL)!=len(medias_filepath):   # check if every media to download has exactly 1 filepath to save to
        logging.error("Length of medias_URL and medias_filepath must be the same.")
        raise ValueError(f"Error in {download_medias.__name__}{inspect.signature(download_medias)}: Length of medias_URL and medias_filepath must be the same.")


    logger.info(f"Downloading medias...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers_max) as thread_manager:  # open threadpool with maximum amount of workers as specified
        for i in range(len(medias_URL)):                                                    # download missing medias and save as specified
            if medias_filepath[i]!=None:                                                    # if media could interact with file system:
                if os.path.isfile(medias_filepath[i])==True:                                # if media already exists: skip downloading, load for return # type:ignore
                    with open(medias_filepath[i], "rb") as media_file:                      # type:ignore
                        medias[i]=media_file.read()
                    threads.append(None)
                    continue
                elif os.path.dirname(medias_filepath[i])!="":                               # if media does not exist already and filepath contains directory part: # type:ignore
                    os.makedirs(os.path.dirname(medias_filepath[i]), exist_ok=True)         # create necessary directories for media file # type:ignore
            
            threads.append(thread_manager.submit(worker_function, media_URL=medias_URL[i], media_filepath=medias_filepath[i], **kwargs))    # download and save media in worker thread


        medias_downloaded_count=len(medias)-medias.count(None)+[thread.done() for thread in threads if thread!=None].count(True)                                            # number of loaded medias + number of downloaded, don't use os.isfile because slower and filepath may be None
        logger.info(f"Download media thread {KFSfstr.notation_abs(medias_downloaded_count, 0, True)}/{KFSfstr.notation_abs(len(medias_URL), 0, True)} finished.")
        while all([thread.done() for thread in threads if thread!=None])==False:                                                                                            # as long as threads still not done: loop here for updating progress
            medias_downloaded_count=len(medias)-medias.count(None)+[thread.done() for thread in threads if thread!=None].count(True)                                        # number of loaded medias + number of downloaded, don't use os.isfile because slower and filepath may be None
            if medias_downloaded_count_old!=medias_downloaded_count:                                                                                                        # only if number changed:
                logger.debug("")
                logger.info(f"\rDownload media thread {KFSfstr.notation_abs(medias_downloaded_count, 0, True)}/{KFSfstr.notation_abs(len(medias_URL), 0, True)} finished.") # refresh console
                medias_downloaded_count_old=medias_downloaded_count                                                                                                         # update count old
            time.sleep(0.1)                                                                                                                                                 # sleep in any case to not throttle code by refreshing with more than 10Hz
        medias_downloaded_count=len(medias)-medias.count(None)+[thread.done() for thread in threads if thread!=None].count(True)                                            # number of loaded medias + number of downloaded, don't use os.isfile because slower and filepath may be None
        logger.debug("")
        logger.info(f"\rDownload media thread {KFSfstr.notation_abs(medias_downloaded_count, 0, True)}/{KFSfstr.notation_abs(len(medias_URL), 0, True)} finished.")

        for i, thread in enumerate(threads):                # collect results
            if thread==None:                                # if thread is None: skip
                continue
            try:
                medias[i]=thread.result()                   # enter result, because of None threads: i fits
            except requests.HTTPError as e:
                success=False                               # download not successful
                logger.error(f"Downloading media \"{medias_URL[i]}\" failed with status code {e.response.status_code}.")
                download_failures_URL.append(medias_URL[i]) # append to failure list so parent function can retry downloading
            except (requests.exceptions.ChunkedEncodingError, requests.ConnectionError, requests.Timeout) as e:
                success=False                               # download not successful
                logger.error(f"Downloading media \"{medias_URL[i]}\" failed with {KFSfstr.full_class_name(e)}. Error message: {e.args}.")
                download_failures_URL.append(medias_URL[i]) # append to failure list so parent function can retry downloading
        
        if success==False:  # if unsuccessful: throw exception with failure list
            raise DownloadError(download_failures_URL)
        else:
            logger.info("Downloaded medias.")

    return medias   # type:ignore


async def download_medias_async(medias_URL: list, medias_filepath: list,
                                worker_function: typing.Callable=download_media_default_async,
                                **kwargs) -> None:
    """
    Downloads medias from medias_URL and saves as specified in medias_filepath. Exceptions from worker function will not be catched. If file already exists at media filepath, assumes that this media has already been downloaded and does not redownload it. Also loads it and uses it in return list.

    Arguments:
    - medias_URL: media URL to download media from. If no custom worker_function is defined, uses download_media_default(...) and expects direct media URL.
    - medias_filepath: media filepaths to save medias at. Must have same length as medias_URL. If an entry is None, does not try to save that media.
    - worker_function: function to download 1 particular media. Must at least take parameters "media_URL" and "media_filepath". Additional **kwargs are forwarded.
    - workers_max: maximum number of worker threads at the same time. Use 1 for single thread operation and None for unrestricted number of workers.
    - **kwargs: additional keyword arguments to forward to custom worker function, no *args so user is forced to accept media_URL and media_filepath and no confusion ensues because of unexpected parameter passing

    Returns:
    - medias: downloaded or loaded medias

    Raises:
    - DownloadError: Downloading media \"{medias_URL[i]}\" failed. Exception contains list of URL that failed.
    - ValueError: Length of medias_URL and medias_filepath must be the same.
    """

    download_failures_URL: list[str]=[]                             # download failures
    medias: list[None|bytes]=[None for _ in range(len(medias_URL))] # medias downloaded or loaded, order should be kept even if multithreaded that's why initialised with None and results are placed at correct i
    medias_downloaded_count: int=0                                  # how many already loaded or downloaded
    medias_downloaded_count_old: int=0                              # how many already loaded or downloaded in iteration previous
    logger: logging.Logger                                          # logger
    success: bool=True                                              # download successful?
    tasks: list[asyncio.Future|None]=[]                             # worker tasks for download, None means no worker task was necessary for that media, used to keep media order
    

    medias_URL=list(medias_URL)
    medias_filepath=list(medias_filepath)

    if 1<=len(logging.getLogger("").handlers):  # if root logger defined handlers:
        logger=logging.getLogger("")            # also use root logger to match formats defined outside KFS
    else:                                       # if no root logger defined:
        logger=KFSlog.setup_logging("KFS")      # use KFS default format

    if len(medias_URL)!=len(medias_filepath):   # check if every media to download has exactly 1 filepath to save to
        logging.error("Length of medias_URL and medias_filepath must be the same.")
        raise ValueError(f"Error in {download_medias.__name__}{inspect.signature(download_medias)}: Length of medias_URL and medias_filepath must be the same.")


    logger.info(f"Downloading medias...")
    async with asyncio.TaskGroup() as task_manager:                                 # open taskpool with maximum amount of workers as specified
        for i in range(len(medias_URL)):                                            # download missing medias and save as specified
            if medias_filepath[i]!=None:                                            # if media could interact with file system:
                if os.path.isfile(medias_filepath[i])==True:                        # if media already exists: skip downloading, load for return # type:ignore
                    with open(medias_filepath[i], "rb") as media_file:              # type:ignore
                        medias[i]=media_file.read()
                    tasks.append(None)
                    continue
                elif os.path.dirname(medias_filepath[i])!="":                       # if media does not exist already and filepath contains directory part: # type:ignore
                    os.makedirs(os.path.dirname(medias_filepath[i]), exist_ok=True) # create necessary directories for media file # type:ignore
            
            tasks.append(task_manager.create_task(worker_function(media_URL=medias_URL[i], media_filepath=medias_filepath[i], **kwargs)))   # download and save media in worker task

        
        medias_downloaded_count=len(medias)-medias.count(None)+[task.done() for task in tasks if task!=None].count(True)                                                        # number of loaded medias + number of downloaded, don't use os.isfile because slower and filepath may be None
        logger.info(f"\rDownload media thread {KFSfstr.notation_abs(medias_downloaded_count, 0, True)}/{KFSfstr.notation_abs(len(medias_URL), 0, True)} finished.")
        while all([task.done() for task in tasks if task!=None])==False:                                                                                                        # as long as threads still not done: loop here for updating progress
            medias_downloaded_count=len(medias)-medias.count(None)+[task.done() for task in tasks if task!=None].count(True)                                                    # number of loaded medias + number of downloaded, don't use os.isfile because slower and filepath may be None
            if medias_downloaded_count_old!=medias_downloaded_count:                                                                                                            # only if number changed:
                logger.debug("")
                logger.info(f"\rDownload media thread {KFSfstr.notation_abs(medias_downloaded_count, 0, True)}/{KFSfstr.notation_abs(len(medias_URL), 0, True)} finished.")     # refresh console
                medias_downloaded_count_old=medias_downloaded_count                                                                                                             # update count old
            await asyncio.sleep(0.1)                                                                                                                                            # sleep in any case to not throttle code by refreshing with more than 10Hz
        medias_downloaded_count=len(medias)-medias.count(None)+[task.done() for task in tasks if task!=None].count(True)                                                        # number of loaded medias + number of downloaded, don't use os.isfile because slower and filepath may be None
        logger.debug("")
        logger.info(f"\rDownload media thread {KFSfstr.notation_abs(medias_downloaded_count, 0, True)}/{KFSfstr.notation_abs(len(medias_URL), 0, True)} finished.")

        for i, task in enumerate(tasks):    # collect results
            if task==None:                  # if task is None: skip
                continue
            try:
                medias[i]=task.result()                     # enter result, because of None tasks: i fits
            except requests.HTTPError as e:
                success=False                               # download not successful
                logger.error(f"Downloading media \"{medias_URL[i]}\" failed with status code {e.response.status_code}.")
                download_failures_URL.append(medias_URL[i]) # append to failure list so parent function can retry downloading
            except (requests.exceptions.ChunkedEncodingError, requests.ConnectionError, requests.Timeout) as e:
                success=False                               # download not successful
                logger.error(f"Downloading media \"{medias_URL[i]}\" failed with {KFSfstr.full_class_name(e)}. Error message: {e.args}.")
                download_failures_URL.append(medias_URL[i]) # append to failure list so parent function can retry downloading
        
        if success==False:  # if unsuccessful: throw exception with failure list
            raise DownloadError(download_failures_URL)
        else:
            logger.info("Downloaded medias.")

    return medias   # type:ignore


class DownloadError(Exception):
    pass