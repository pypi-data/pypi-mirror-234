import os
import tempfile
import uuid
import zipfile
from datetime import datetime

class Store( object ):
    def __init__(self, turn_store_on=True):
        if turn_store_on:
            self.aGuid = str(uuid.uuid4())
            self.dir_name = tempfile.mkdtemp(suffix='-video', prefix=self.aGuid)
            self.list_to_zip = [] # containing the complete file list with absolute path
            self.counter = 1

    def get_guid(self):
        return self.aGuid

    def turn_store_on(self):
        self.aGuid = str(uuid.uuid4())
        self.dir_name = tempfile.mkdtemp(suffix='-video', prefix=self.aGuid)
        self.list_to_zip = []  # containing the complete file list with absolute path

    def get_dir_name(self):
        return self.dir_name

    def get_ffmpeg_glob(self):
        file_name_glob = '%s-??????.png' % (os.path.join(self.get_dir_name(), self.get_guid()))
        return file_name_glob

    def get_glob(self):
        file_name_glob = '%s%sscreenshot_????????-??????.??????-*-????????-????-????-????-????????????.png' % (self.get_dir_name(), os.sep)
        return file_name_glob

    def generate_file( self ):
        file_name = "%s-%06d.png" % ( self.get_guid(), self.counter )
        path_and_file = os.path.join( self.get_dir_name(), file_name )
        self.list_to_zip.append( path_and_file )
        self.counter += 1
        return path_and_file

    def add_file(self , name ):
        self.list_to_zip.append( name )

    def add_filepath_with_command(self, commandStr="Dummy"):
        now = datetime.now()
        file_name = "screenshot_" + now.strftime("%Y%m%d-%H%M%S.%f") + "-" \
                    + commandStr + "-" \
                    + str(uuid.uuid4()) + ".png"
        path_and_file = os.path.join(self.get_dir_name(), file_name)
        self.list_to_zip.append(path_and_file)
        return path_and_file

    def zip( self ):
        with zipfile.ZipFile(self.aGuid + '.zip', 'w') as myzip:
             for f in self.list_to_zip:
                 myzip.write(f,arcname=os.path.basename(f))