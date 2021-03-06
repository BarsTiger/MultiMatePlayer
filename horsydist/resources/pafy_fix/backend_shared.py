import os
import re
import sys
import time
import logging
import subprocess

if sys.version_info[:2] >= (3, 0):
    # pylint: disable=E0611,F0401,I0011
    from urllib.request import urlopen, build_opener
    from urllib.error import HTTPError, URLError
    from urllib.parse import parse_qs, urlparse
    uni, pyver = str, 3

else:
    from urllib2 import urlopen, build_opener, HTTPError, URLError
    from urlparse import parse_qs, urlparse
    uni, pyver = unicode, 2

early_py_version = sys.version_info[:2] < (2, 7)

dbg = logging.debug


def extract_video_id(url):
    """ Extract the video id from a url, return video id as str. """
    idregx = re.compile(r'[\w-]{11}$')
    url = str(url).strip()

    if idregx.match(url):
        return url # ID of video

    if '://' not in url:
        url = '//' + url
    parsedurl = urlparse(url)
    if parsedurl.netloc in ('youtube.com', 'www.youtube.com', 'm.youtube.com', 'gaming.youtube.com'):
        query = parse_qs(parsedurl.query)
        if 'v' in query and idregx.match(query['v'][0]):
            return query['v'][0]
    elif parsedurl.netloc in ('youtu.be', 'www.youtu.be'):
        vidid = parsedurl.path.split('/')[-1] if parsedurl.path else ''
        if idregx.match(vidid):
            return vidid

    err = "Need 11 character video id or the URL of the video. Got %s"
    raise ValueError(err % url)


class BasePafy(object):

    """ Class to represent a YouTube video. """

    def __init__(self, video_url, basic=True, gdata=False,
                 size=False, callback=None, ydl_opts=None):
        """ Set initial values. """
        self.version = 1
        self.videoid = extract_video_id(video_url)
        self.watchv_url = "http://www.youtube.com/watch?v=%s" % self.videoid

        self.callback = callback
        self._have_basic = False
        self._have_gdata = False

        self._description = None
        self._likes = None
        self._dislikes = None
        self._category = None
        self._published = None
        self._username = None

        self._streams = []
        self._oggstreams = []
        self._m4astreams = []
        self._allstreams = []
        self._videostreams = []
        self._audiostreams = []

        self._title = None
        self._rating = None
        self._length = None
        self._author = None
        self._duration = None
        self._keywords = None
        self._bigthumb = None
        self._viewcount = None
        self._bigthumbhd = None
        self._bestthumb = None
        self._mix_pl = None
        self.expiry = None

        if basic:
            self._fetch_basic()

        if gdata:
            self._fetch_gdata()

        if size:
            for s in self.allstreams:
                # pylint: disable=W0104
                s.get_filesize()


    def _fetch_basic(self):
        """ Fetch basic data and streams. """
        raise NotImplementedError


    def _fetch_gdata(self):
        """ Extract gdata values, fetch gdata if necessary. """
        raise NotImplementedError


    def _process_streams(self):
        """ Create Stream object lists from internal stream maps. """
        raise NotImplementedError


    def __repr__(self):
        """ Print video metadata. Return utf8 string. """
        if self._have_basic:
            info = [("Title", self.title),
                    ("Author", self.author),
                    ("ID", self.videoid),
                    ("Duration", self.duration),
                    ("Rating", self.rating),
                    ("Views", self.viewcount)]

            nfo = "\n".join(["%s: %s" % i for i in info])

        else:
            nfo = "Pafy object: %s [%s]" % (self.videoid,
                                            self.title[:45] + "..")

        return nfo.encode("utf8", "replace") if pyver == 2 else nfo

    @property
    def streams(self):
        """ The streams for a video. Returns list."""
        if not self._streams:
            self._process_streams()

        return self._streams

    @property
    def allstreams(self):
        """ All stream types for a video. Returns list. """
        if not self._allstreams:
            self._process_streams()

        return self._allstreams

    @property
    def audiostreams(self):
        """ Return a list of audio Stream objects. """
        if not self._audiostreams:
            self._process_streams()

        return self._audiostreams

    @property
    def videostreams(self):
        """ The video streams for a video. Returns list. """
        if not self._videostreams:
            self._process_streams()

        return self._videostreams

    @property
    def oggstreams(self):
        """ Return a list of ogg encoded Stream objects. """
        if not self._oggstreams:
            self._process_streams()

        return self._oggstreams

    @property
    def m4astreams(self):
        """ Return a list of m4a encoded Stream objects. """
        if not self._m4astreams:
            self._process_streams()

        return self._m4astreams

    @property
    def title(self):
        """ Return YouTube video title as a string. """
        if not self._title:
            self._fetch_basic()

        return self._title

    @property
    def author(self):
        """ The uploader of the video. Returns str. """
        if not self._author:
            self._fetch_basic()

        return self._author

    @property
    def rating(self):
        """ Rating for a video. Returns float. """
        if not self._rating:
            self._fetch_basic()

        return self._rating

    @property
    def length(self):
        """ Length of a video in seconds. Returns int. """
        if not self._length:
            self._fetch_basic()

        return self._length

    @property
    def viewcount(self):
        """ Number of views for a video. Returns int. """
        if not self._viewcount:
            self._fetch_basic()

        return self._viewcount

    @property
    def bigthumb(self):
        """ Large thumbnail image url. Returns str. """
        self._fetch_basic()
        return self._bigthumb

    @property
    def bigthumbhd(self):
        """ Extra large thumbnail image url. Returns str. """
        self._fetch_basic()
        return self._bigthumbhd

    @property
    def duration(self):
        """ Duration of a video (HH:MM:SS). Returns str. """
        if not self._length:
            self._fetch_basic()

        self._duration = time.strftime('%H:%M:%S', time.gmtime(self._length))
        self._duration = uni(self._duration)

        return self._duration

    @property
    def keywords(self):
        """ Return keywords as list of str. """
        if not self._keywords:
            self._fetch_gdata()

        return self._keywords

    @property
    def category(self):
        """ YouTube category of the video. Returns string. """
        if not self._category:
            self._fetch_gdata()

        return self._category

    @property
    def description(self):
        """ Description of the video. Returns string. """
        if not self._description:
            self._fetch_gdata()

        return self._description

    @property
    def username(self):
        """ Return the username of the uploader. """
        if not self._username:
            self._fetch_basic()

        return self._username

    @property
    def published(self):
        """ The upload date and time of the video. Returns string. """
        if not self._published:
            self._fetch_gdata()

        return self._published.replace(".000Z", "").replace("T", " ")

    @property
    def likes(self):
        """ The number of likes for the video. Returns int. """
        if not self._likes:
            self._fetch_basic()

        return self._likes

    @property
    def dislikes(self):
        """ The number of dislikes for the video. Returns int. """
        if not self._dislikes:
            self._fetch_basic()

        return self._dislikes

    def _getbest(self, preftype="any", ftypestrict=True, vidonly=False):
        """
        Return the highest resolution video available.

        Select from video-only streams if vidonly is True
        """
        streams = self.videostreams if vidonly else self.streams

        if not streams:
            return None

        def _sortkey(x, key3d=0, keyres=0, keyftype=0):
            """ sort function for max(). """
            key3d = "3D" not in x.resolution
            keyres = int(x.resolution.split("x")[0])
            keyftype = preftype == x.extension
            strict = (key3d, keyftype, keyres)
            nonstrict = (key3d, keyres, keyftype)
            return strict if ftypestrict else nonstrict

        r = max(streams, key=_sortkey)

        if ftypestrict and preftype != "any" and r.extension != preftype:
            return None

        else:
            return r

    def getbestvideo(self, preftype="any", ftypestrict=True):
        """
        Return the best resolution video-only stream.

        set ftypestrict to False to return a non-preferred format if that
        has a higher resolution
        """
        return self._getbest(preftype, ftypestrict, vidonly=True)

    def getbest(self, preftype="any", ftypestrict=True):
        """
        Return the highest resolution video+audio stream.

        set ftypestrict to False to return a non-preferred format if that
        has a higher resolution
        """
        return self._getbest(preftype, ftypestrict, vidonly=False)

    def getbestaudio(self, preftype="any", ftypestrict=True):
        """ Return the highest bitrate audio Stream object."""
        if not self.audiostreams:
            return None

        def _sortkey(x, keybitrate=0, keyftype=0):
            """ Sort function for max(). """
            keybitrate = int(x.rawbitrate)
            keyftype = preftype == x.extension
            strict, nonstrict = (keyftype, keybitrate), (keybitrate, keyftype)
            return strict if ftypestrict else nonstrict

        r = max(self.audiostreams, key=_sortkey)

        if ftypestrict and preftype != "any" and r.extension != preftype:
            return None

        else:
            return r

    @classmethod
    def _content_available(cls, url):
        try:
            response = urlopen(url)
        except HTTPError:
            return False
        else:
            return response.getcode() < 300

    def getbestthumb(self):
        """ Return the best available thumbnail."""
        if not self._bestthumb:
            part_url = "http://i.ytimg.com/vi/%s/" % self.videoid
            # Thumbnail resolution sorted in descending order
            thumbs = ("maxresdefault.jpg",
                      "sddefault.jpg",
                      "hqdefault.jpg",
                      "mqdefault.jpg",
                      "default.jpg")
            for thumb in thumbs:
                url = part_url + thumb
                if self._content_available(url):
                    return url

        return self._bestthumb

    def populate_from_playlist(self, pl_data):
        """ Populate Pafy object with items fetched from playlist data. """
        self._title = pl_data.get("title")
        self._author = pl_data.get("author")
        self._length = int(pl_data.get("length_seconds", 0))
        self._rating = pl_data.get("rating", 0.0)
        self._viewcount = "".join(re.findall(r"\d", "{0}".format(pl_data.get("views", "0"))))
        self._viewcount = int(self._viewcount)
        self._description = pl_data.get("description")


class BaseStream(object):

    """ YouTube video stream class. """

    def __init__(self, parent):
        """ Set initial values. """
        self._itag = None
        self._mediatype = None
        self._threed = None
        self._rawbitrate = None
        self._resolution = None
        self._quality = None
        self._dimensions = None
        self._bitrate = None
        self._extension = None
        self.encrypted = None
        self._notes = None
        self._url = None
        self._rawurl = None

        self._parent = parent
        self._filename = None
        self._fsize = None
        self._active = False


    @property
    def rawbitrate(self):
        """ Return raw bitrate value. """
        return self._rawbitrate

    @property
    def threed(self):
        """ Return bool, True if stream is 3D. """
        return self._threed

    @property
    def itag(self):
        """ Return itag value of stream. """
        return self._itag

    @property
    def resolution(self):
        """ Return resolution of stream as str. 0x0 if audio. """
        return self._resolution

    @property
    def dimensions(self):
        """ Return dimensions of stream as tuple.  (0, 0) if audio. """
        return self._dimensions

    @property
    def quality(self):
        """ Return quality of stream (bitrate or resolution).

        eg, 128k or 640x480 (str)
        """
        return self._quality

    @property
    def title(self):
        """ Return YouTube video title as a string. """
        return self._parent.title

    @property
    def extension(self):
        """ Return appropriate file extension for stream (str).

        Possible values are: 3gp, m4a, m4v, mp4, webm, ogg
        """
        return self._extension

    @property
    def bitrate(self):
        """ Return bitrate of an audio stream. """
        return self._bitrate

    @property
    def mediatype(self):
        """ Return mediatype string (normal, audio or video).

        (normal means a stream containing both video and audio.)
        """
        return self._mediatype

    @property
    def notes(self):
        """ Return additional notes regarding the stream format. """
        return self._notes

    @property
    def url(self):
        """ Return the url, decrypt if required. """
        return self._url

    @property
    def url_https(self):
        """ Return https url. """
        return self.url.replace("http://", "https://")

    def __repr__(self):
        """ Return string representation. """
        out = "%s:%s@%s" % (self.mediatype, self.extension, self.quality)
        return out

    def cancel(self):
        """ Cancel an active download. """
        if self._active:
            self._active = False
            return True

def remux(infile, outfile, quiet=False, muxer="ffmpeg"):
    """ Remux audio. """
    muxer = muxer if isinstance(muxer, str) else "ffmpeg"

    for tool in set([muxer, "ffmpeg", "avconv"]):
        cmd = [tool, "-y", "-i", infile, "-acodec", "copy", "-vn", outfile]

        try:
            with open(os.devnull, "w") as devnull:
                subprocess.call(cmd, stdout=devnull, stderr=subprocess.STDOUT)

        except OSError:
            dbg("Failed to remux audio using %s", tool)

        else:
            os.unlink(infile)
            dbg("remuxed audio file using %s" % tool)

            if not quiet:
                sys.stdout.write("\nAudio remuxed.\n")

            break

    else:
        logging.warning("audio remux failed")
        os.rename(infile, outfile)


def get_size_done(bytesdone, progress):
    _progress_dict = {'KB': 1024.0, 'MB': 1048576.0, 'GB': 1073741824.0}
    return round(bytesdone/_progress_dict.get(progress, 1.0), 2)


def get_status_string(progress):
    status_string = ('  {:,} ' + progress + ' [{:.2%}] received. Rate: [{:4.0f} '
                     'KB/s].  ETA: [{:.0f} secs]')

    if early_py_version:
        status_string = ('  {0:} ' + progress + ' [{1:.2%}] received. Rate:'
                         ' [{2:4.0f} KB/s].  ETA: [{3:.0f} secs]')

    return status_string
