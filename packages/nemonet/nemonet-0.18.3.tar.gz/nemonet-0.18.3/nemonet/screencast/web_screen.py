import uuid
import os
import tempfile
from datetime import datetime
import glob
import cv2
import zipfile
import logging
from PIL import Image

logger = logging.getLogger(__name__)


class ImageRecording(object):

    def __init__(self):
        self.aGuid = str(uuid.uuid4())
        self.dir_name = None
        self.list_to_zip = []  # containing the complete file list with absolute path
        self.file_name_glob = None
        self.enabled = False
        self.mean_height = 0
        self.mean_width = 0
        self.number_of_images = 0
        self.calculation_mean_done = False

    def enable_recording(self):
        self.dir_name = tempfile.mkdtemp(suffix='-video', prefix=self.aGuid)
        logger.debug("Recording Folder: " + str(self.get_dir_name()))
        self.file_name_glob = '%s%sscreenshot_????????-??????.??????-*-????????-????-????-????-????????????.png' % (
        self.get_dir_name(), os.sep)
        self.enabled = True

    def is_enabled(self):
        return self.enabled

    def get_dir_name(self):
        return self.dir_name

    def generate_screenshot_filename(self, name):
        now = datetime.now()
        file_name = "screenshot_" + now.strftime("%Y%m%d-%H%M%S.%f") + "-" \
                    + name + "-" \
                    + str(uuid.uuid4()) + ".png"
        path_and_file = os.path.join(self.get_dir_name(), file_name)
        self.list_to_zip.append(path_and_file)
        return path_and_file

    # needs to be reworked according the project image_recorder
    # 1. calc the mean 2. resize 3. create video
    def calculate_images_mean(self):
        if not self.calculation_mean_done:
            for file in glob.glob(self.file_name_glob):
                self.number_of_images += 1
                image = Image.open(file)
                width, height = image.size
                self.mean_width += width
                self.mean_height += height
            self.calculation_mean_done = True
        return (int(self.mean_width / self.number_of_images), int(self.mean_height / self.number_of_images))
    # resize 3. create video
    def resize_images(self):
        width, height = self.calculate_images_mean()
        for file in glob.glob(self.file_name_glob):
            im = Image.open(file)
            imResize = im.resize((width,height), Image.Resampling.LANCZOS)
            imResize.save(file, 'JPEG', quality=95)
    # Finding the mean height and width of all images.
    # This is required because the video frame needs
    # to be set with same width and height. Otherwise
    # images not equal to that width height will not get
    # embedded into the video
    # AND
    # Resizing of the images to give
    # them same width and height
    # 3. create video and store in zip
    def store(self):
        if not self.is_enabled():
            return
        self.resize_images()
        logger.debug("Store the screenshots and create avi")
        video_file_name_prefix = (os.path.join(self.get_dir_name()))
        video_file_name = '%s-video.avi' % (video_file_name_prefix)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        nbr = 0
        height = width = layers = 0
        video = None

        for file in glob.glob(self.file_name_glob):
            logger.debug("png file=%s" % (file))
            if nbr == 0:
                frame = cv2.imread(file)
                height, width, layers = frame.shape
                logger.debug("frame.shape: height=%d, width=%d, layers=%d" % (height, width, layers))
                #video = cv2.VideoWriter(video_file_name, fourcc, 2, (width, height), True)
                video = cv2.VideoWriter(video_file_name, 0, 1, (width, height))
                video.write(cv2.imread(file))
            else:
                video.write(cv2.imread(file))

            nbr += 1
        cv2.destroyAllWindows()
        video.release()
        self.list_to_zip.append(video_file_name)
        with zipfile.ZipFile(self.aGuid + '.zip', 'w') as myzip:
             for f in self.list_to_zip:
                 myzip.write(f,arcname=os.path.basename(f))
