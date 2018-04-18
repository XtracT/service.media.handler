import xbmc
import xbmcaddon
import xbmcgui
import os
import shutil
import time
import datetime
import feedparser
import resources.lib.untangle as untangle
import httplib2
import subprocess
import simplecache


from pickle import load, dump
from os import path
from sys import exit 
from json import dumps

#  scp service.py root@libreelec:~/.kodi/addons/service.media.handler/
# zip -r service.media.handler.zip service.media.handler/ && scp service.media.handler.zip root@libreelec:~/

#Get addon data
DEV_MODE = False

addon       = xbmcaddon.Addon()
__addonname__   = addon.getAddonInfo('name')
__settings__   = xbmcaddon.Addon(addon.getAddonInfo('id'))
__addondir__    = xbmc.translatePath( addon.getAddonInfo('profile') ) 
__icon__ = addon.getAddonInfo('icon')

def find_fileType(fileName):
    video_file_extensions = (
        '.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec',
        '.aep', '.aepx', '.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf',
        '.asx', '.avb', '.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik',
        '.bin', '.bix', '.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel', '.cine',
        '.cip', '.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat',
        '.dav', '.dce', '.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm','.dmsm3d', '.dmss',
        '.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms','.dvx', '.dxr',
        '.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp','.fcproject',
        '.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp','.h264', '.hdmov',
        '.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf','.ivr', '.ivs',
        '.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg','.m1v', '.m21',
        '.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv','.mj2', '.mjp',
        '.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov', '.movie','.mp21',
        '.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2', '.mpgindex','.mpl',
        '.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv', '.mvb','.mvc',
        '.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv','.nvc', '.ogm',
        '.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs', '.playlist','.plproj',
        '.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva', '.pvr','.pxv',
        '.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm', '.rmd','.rmd',
        '.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl', '.sbk','.sbt',
        '.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv', '.smi','.smi',
        '.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf', '.ssm', '.stl', '.str', '.stx', '.svi', '.swf','.swi',
        '.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp', '.ts','.tsp', '.ttxt',
        '.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg', '.vem', '.vep', '.vf','.vft',
        '.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3', '.vp6', '.vp7','.vpj',
        '.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv', '.wmx','.wot', '.wp3',
        '.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog',
        '.yuv', '.zeg','.zm1', '.zm2', '.zm3', '.zmv')

    audio_file_extensions = (
        '.midi', '.aiff', '.wave', '.aiff', '.ac3', '.dts', '.alac', '.amr', '.flac,', '.ape', '.ym', '.adpcm', '.cdda','.m4a',
        '.m4b', '.wv', '.webm', '.realaudio', '.shn', '.wavpack,', '.mpc', '.shorten', '.speex', '.it', '.s3m', '.mod','.xm',
        '.nsf', '.spc', '.gym', '.sid', '.adlib', '.3gp', '.aa', '.aac', '.aax', '.act', '.aiff', '.amr', '.ape', '.au','.awb',
        '.dct', '.dss', 'dvf', '.flac', '.gsm', '.iklax', '.ivs', '.m4p', '.mmf', '.mp3', '.mpc', '.msv', '.ogg', '.oga','.mogg',
        '.opus', '.ra', '.rm', '.raw', '.sln', '.tta', '.vox', '.wav', '.wma')

    if fileName.endswith((video_file_extensions)):
        return "Video"
    elif fileName.endswith((audio_file_extensions)):
        return "Audio"
    else:
        return "Unknown"

def is_not_sample_file(fullfileName):
    keywords = ('Sample','sample','SAMPLE','Trailer','trailer','TRAILER')
    size_file = os.path.getsize(fullfileName)
    not_a_sample = [False for match in keywords if match in fullfileName]

    if (not_a_sample == []) or (size_file > 100 * 1024 * 1024):
        not_a_sample = True
    else:
        not_a_sample = False
    return not_a_sample

def move_to_folder(fullfileName,folder,fileName):
    # Create destination folder if it does not exist and move file
    if not os.path.exists(folder):
        os.makedirs(folder)
    shutil.move(fullfileName, os.path.join(folder, fileName))

class LogOutput:
    def __init__(self):
        xbmc.log("Logging enabled", level=xbmc.LOGINFO)
    def info(self, msg):
        xbmc.log(msg , level=xbmc.LOGINFO)
    def debug(self, msg):
        xbmc.log(msg , level=xbmc.LOGDEBUG)
    def warn(self, msg):
        xbmc.log(msg , level=xbmc.LOGWARNING)
    def error(self, msg):
        xbmc.log(msg , level=xbmc.LOGERROR)

class advNotifications:
    def __init__(self):
        self.enableNotifications = bool(__settings__.getSetting("show_notifications"))
    def send(self,text,time):
        if self.enableNotifications:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, text, time, __icon__))
    def sendOverride(self,text,time):
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, text, time, __icon__))

class mediaOrganizer:
    def __init__(self):
        self.runPeriodically = False
        self.intervalRun = 60		
        self.paths = {'source': [], 'check': [], 'movies': [], 'shows': [], 'anime': [], 'music': [] }
        self.deleteFiles = bool(__settings__.getSetting("delete_files"))
        self.updateLibraries = bool(__settings__.getSetting("update_libraries"))
        self.interval = int(__settings__.getSetting("mo_sleep_time"))
        self.deleteFiles = False
        self.updateLibraries = True

        for key in self.paths.iteritems():
            self.paths[key[0]] = xbmc.translatePath(__settings__.getSetting( str(key[0]) + "_folder"))
            if not os.path.isdir(self.paths[key[0]]):
                self.paths[key[0]] = self.paths['source']
        self.checkSettings()
    
    def checkSettings(self):
        if not os.path.isdir(self.paths['source']):
            out.error('Source path is not a valid directory')
            notifier.sendOverride('Source path is not a valid directory. Change, restart service!', 2000)
            return False
        if not os.path.isdir(self.paths['check']):
            out.error('Source path is not a valid directory')
            notifier.sendOverride('Check path is not a valid directory. Change, restart service!', 2000)
            return False
        return True

    def run(self):
        if not self.checkSettings():
            return False
            
        fileCounter = 0
        videoOrganized = False
        audioOrganized = False

        for root, dirs, files in os.walk(self.paths['source'], topdown=False):
            for fileName in files:
                fileCounter += 1

        if fileCounter > 0:
            fileNum = 0
            for root, dirs, files in os.walk(self.paths['source'], topdown=False):
                for fileName in files:
                    fileNum = fileNum + 1
                    fullfileName = os.path.join(root, fileName)
                    fileType = find_fileType(fullfileName)
                    out.debug(str(fullfileName) + str(fileType))
                    if fileType=="Video":
                        videoOrganized = True
                        info = untangle.Untangle(fileName, use_meta_info=False)  # Get info from the file
                        if bool(info.id) & is_not_sample_file(fullfileName): #
                            if info.type_video == "MOVIE":
                                destination_folder = os.path.join(self.paths['movies'],info.proper_title + " (" + str(info.year) + ")" )
                            elif info.type_video == "SHOW":
                                destination_folder = os.path.join(self.paths['shows'],info.proper_title, "Season "  + str(info.season).zfill(2))
                            elif info.type_video == "ANIME":
                                destination_folder = os.path.join(self.paths['anime'], info.proper_title, "Season " + str(info.season).zfill(2))
                            else:
                                destination_folder = os.path.join(self.paths['check'],info.proper_title + " (" + str(info.year) + ")" )
                            move_to_folder(fullfileName, destination_folder, fileName)
                        elif not is_not_sample_file(fullfileName):
                            os.remove(fullfileName)
                        else:
                            if self.deleteFiles:
                                out.debug('I am deleting video file bitch')
                                os.remove(fullfileName)
                            else:
                                move_to_folder(fullfileName, self.paths['check'], fileName)
                    elif fileType=="Audio":
                        audioOrganized = True
                        fileFolder = root.replace(self.paths['source'], '')
                        destination_folder = os.path.join(self.paths['music'], fileFolder)
                        move_to_folder(fullfileName, destination_folder, fileName)
                    else:
                        if self.deleteFiles:
                            out.debug('I am deleting unknown file bitch')
                            os.remove(fullfileName)
                        else:
                            out.debug('moving file to folder ' + str(fullfileName) + str(self.paths['check']) + str(fileName))
                            move_to_folder(fullfileName, self.paths['check'], fileName)

                # Remove empty directories
                if os.listdir(root) == [] :
                    if root!=self.paths['source']:
                        os.rmdir(root)
            
            if fileCounter >= 1:
                notifier.send(str(fileCounter) + ' files organized!', 500)

        if self.updateLibraries and videoOrganized:
            xbmc.executebuiltin('UpdateLibrary(video)')
            time.sleep(0.1)
            xbmc.executebuiltin('CleanLibrary(video)')
        elif self.updateLibraries and audioOrganized:
            xbmc.executebuiltin('UpdateLibrary(music)')
            time.sleep(0.1)
            xbmc.executebuiltin('CleanLibrary(music)')

class showRssParser():
    def __init__(self,transmission):
        # initialize the cache
        self.transmission = transmission
        self.cache = RotatingCache("ShowRssParser.Cache")
        self.feedUrl = 'http://showrss.info/user/38432.rss?magnets=true&namespaces=true&name=null&quality=null&re=null'
        self.feedUrl = __settings__.getSetting("feed_url")
        self.interval = int(__settings__.getSetting("showrss_sleep_time"))
        if self.checkSettings():
            pass
        else:
            __settings__.openSettings()
 
    def checkSettings(self):
        # check the feed uri
        if self.feedUrl.find('namespaces=true') == -1 or self.feedUrl.find('magnets=true') == -1:
            out.error('Invalid feed URL. Magnets and namespaces are required')
            notifier.sendOverride('Invalid feed URL. Magnets and namespaces are required', 2000)
            return False

        # try to get the feed
        try:
            feed = feedparser.parse(self.feedUrl)
        except Exception as e:
            out.error('Error getting the feed: %s' % e)
            notifier.sendOverride('Error getting to the feed. Check connection!', 2000)
            return False

    def run(self):
        if not self.checkSettings():
            return False

        # get feed and check is read ok and it correct
        feed = feedparser.parse(self.feedUrl)
        if feed.bozo:
            out.error('Bozo feed: %s' % feed.bozo_exception.getMessage())
            return False

        numLinksParsed = 0
        # iterate over the entries
        for entry in reversed(feed.entries):
            if not entry.has_key('tv_episode_id'):
                out.warn('Found entry with missing episode id ... skipping')
                continue
            id = entry['tv_episode_id']
            
            if id in self.cache.items:
                out.info('Entry "%s": already downloaded ... skipping' % id)
                continue

            if not entry.has_key('tv_show_name'):
                out.warn('Entry "%s": no showname found ... skipping' % id)
                continue
            show = entry['tv_show_name']

            if len(entry.enclosures) >= 1:
                link = entry.enclosures[0].href
            else:
                out.warn('Entry "%s": no magnet link available ... skipping' % id)
                continue

            try:
                body = dumps( { "method": "torrent-add", "arguments": { "filename": link } } )		
                response, content = self.transmission.getData(body)

            except Exception as e:
                out.error('Error sending to transmission: %s' % e)
            else:
                if str(content).find("success") == -1:
                    out.warn("Could not send link to transmission: " + content)
                else:
                    out.info('Started download of new episode of "%s" ' % (show))
                    self.cache.add(id)
                    numLinksParsed = numLinksParsed + 1 
        self.cache.write()
        if numLinksParsed >= 1:
            notifier.send('Sent ' + str(numLinksParsed) + ' episodes to transmission' , 2000)


class transmissionProxy:
    def __init__(self):
        self.host= __settings__.getSetting("host")
        self.port = __settings__.getSetting("port")
        self.user = __settings__.getSetting("user")
        self.pwd = __settings__.getSetting("pwd")
        self.url = 'http://' + self.host + ':' + self.port + '/transmission/rpc'
        self.h = httplib2.Http(__addondir__ + "/.cache" , timeout=5.0)
        if self.user:
            self.h.add_credentials(self.user, self.pwd)

        if self.checkSettings():
            pass
        else:
            __settings__.openSettings()

    def checkSettings(self):
        # check connection to transmission-rpc
        if not self.user or not self.pwd:
            notifier.sendOverride('Transmission needs to have auth on (user:pwd) to work ', 2000)
            return False

        try:
            resp, content = self.h.request(self.url, "GET")
            self.headers = { "X-Transmission-Session-Id": resp['x-transmission-session-id'] }
        except Exception as e:
            out.error('Error getting transmission: %s' % e)
            notifier.sendOverride('Could not reach transmission-rpc. Check settings', 2000)
            return False
        return True

    def getData(self, body):
        try:
            response, content = self.h.request(self.url, 'POST', headers=self.headers, body=body)
        except Exception as e:
            out.error('Error sending to transmission: %s' % e)
            return False
        else:
            return response, content

    def start(self):
        hey = 1
        return True
    
    def stop(self):
        hey = 2
        return True

    def setAltSpeed(self,state):	
        if state:
            body = dumps( {"method":"session-set","arguments":{"alt-speed-enabled":"true"} } )
        else:
            body = dumps( {"method":"session-set","arguments":{"alt-speed-enabled":"false"} } )
        self.getData(body)

class RotatingCache:
    cachesize = 120
    needsupdate = False
    def __init__(self,name):
        self.cache = simplecache.SimpleCache()
        self.name = name
        self.items = self.cache.get(self.name)
        if not self.items or DEV_MODE:
            self.items = []
    def add(self, new):
        self.items.insert(0, new)
        self.needsupdate = True
    def write(self):
        if self.needsupdate:
            self.items = self.items[:self.cachesize] 
            self.cache.set( self.name, self.items, expiration=datetime.timedelta(days=60))
            self.needsupdate = False


class Monitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)
        self.id = xbmcaddon.Addon().getAddonInfo('id')
        self.idle = False

    def onSettingsChanged(self):
        subprocess.call(['systemctl', 'restart', self.id])
    
    def onScreensaverActivated(self):
        self.idle = True 
    
    def onScreensaverDeactivated(self):
        self.idle = False

class transmissionCtrl:
    def __init__(self,transmission):
        self.trans = transmission
        self.interval = 10 # seconds

    def run(self):
        if monitor.idle:
            self.trans.setAltSpeed(False)
        else:
            self.trans.setAltSpeed(True)
        
        if xbmc.Player().isPlaying():
            self.trans.stop()
        else:
            self.trans.start()

class taskCtrl:
    class taskData:
        def __init__(self,fun):
            self.fun = fun
            self.lastTimeStamp = 0

    def __init__(self, *arg):
        self.tasks = []
        for i in range(len(arg)):
            if arg[i].interval:
                task = self.taskData(arg[i])
                self.tasks.append(task)
            else:
                out.warn('this task does not have an specified interval')
    
    def runTasks(self):
        for i in range(len(self.tasks)) : 
            if self.tasks[i].fun.interval < 0 :
                continue

            elapsed = time.time() - self.tasks[i].lastTimeStamp
            if elapsed >= self.tasks[i].fun.interval :
                self.tasks[i].lastTimeStamp = time.time()
                self.tasks[i].fun.run()

out = LogOutput()
notifier = advNotifications()
monitor = Monitor()

if __name__ == '__main__':
    playNice = bool(__settings__.getSetting("play_nice"))
    transmission = transmissionProxy()
    parser = showRssParser(transmission)
    organizer = mediaOrganizer()
    transControl = transmissionCtrl(transmission)
    tasker = taskCtrl(parser,organizer,transControl)

    while not monitor.abortRequested():
        if playNice:
            transControl.run()
            while xbmc.Player().isPlaying() and not monitor.abortRequested():
                monitor.waitForAbort(5)
        tasker.runTasks()
        monitor.waitForAbort(5)