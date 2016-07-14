from System.Diagnostics import *
from System.IO import *
from Newtonsoft.Json import *

from Deadline.Events import *
from Deadline.Scripting import *

import sys
import os
import json
import traceback
import urllib
import urllib2

##############################################################################################
## This is the function called by Deadline to get an instance of the FFmpeg event listener.
##############################################################################################
def GetDeadlineEventListener():
    return FFmpegEventListener()

def CleanupDeadlineEventListener( eventListener ):
    eventListener.Cleanup()

###############################################################
## The FFmpeg event listener class.
###############################################################
class FFmpegEventListener (DeadlineEventListener):
    def __init__( self ):
        self.OnJobFinishedCallback += self.OnJobFinished
    
    def Cleanup( self ):
        del self.OnJobFinishedCallback

    ## This is called when the job finishes rendering.
    def OnJobFinished( self, job ):
        
        if job.PluginName == "Nuke":

            try:
                outputCount = len(job.JobOutputFileNames)
                for i in range( 0, outputCount ):
                    
                    # OutputDirectory0=/Users/craigmorris/Google Drive/memory-lane-test-render/output
                    # OutputFilename0=cadbury_memory_lane_v02_####.jpeg

                    # Input image file constructed from Nuke output dir/filenames
                    jobInputDir = job.JobOutputDirectories[i]
                    jobInputFileName = job.JobOutputFileNames[i]
                    jobInputFileName = jobInputFileName.replace( "####", "%04d" )

                    jobInputFile = Path.Combine( jobInputDir, jobInputFileName )
                    jobInputFile = RepositoryUtils.CheckPathMapping( jobInputFile, True )
                    jobInputFile = PathUtils.ToPlatformIndependentPath( jobInputFile )
                    ClientUtils.LogText( "#########################################################################################" )
                    ClientUtils.LogText( "Script v12" )
                    ClientUtils.LogText( "FFmpeg Input Img Seq: %s" % jobInputFile )

                    ffmpegAudioFile = self.GetConfigEntryWithDefault( "AudioFile", "/etc/c.mp3" )
                    ClientUtils.LogText( "FFmpeg Audio File: %s" % ffmpegAudioFile )

                    # ffmpeg output directory construction with override sub-dir and create directory if missing
                    jobOutputDir = job.JobOutputDirectories[i]
                    relativeFolder = self.GetConfigEntryWithDefault( "OutputFolder", "FFmpeg" )
                    
                    ffmpegOutputFolder = Path.Combine( jobOutputDir, relativeFolder )
                    ffmpegOutputFolder = RepositoryUtils.CheckPathMapping( ffmpegOutputFolder, True )

                    if not Directory.Exists( ffmpegOutputFolder ):
                        ClientUtils.LogText( "Creating output directory '%s'..." % ffmpegOutputFolder )
                        Directory.CreateDirectory( ffmpegOutputFolder )

                    ffmpegOutputFile = Path.Combine( ffmpegOutputFolder, "out.mp4" )
                    ffmpegOutputFile = PathUtils.ToPlatformIndependentPath( ffmpegOutputFile )

                    ClientUtils.LogText( "FFmpeg Output Movie File: %s" % ffmpegOutputFile )
                    ClientUtils.LogText( "#########################################################################################" )
                            
                    # ./ffmpeg -y -threads 64 -r 25 -i /Users/owenm/Downloads/renders/teapots_%04d.jpeg -i /Users/owenm/Downloads/renders/Cadbury_v2_160628.mp3 -pix_fmt yuv420p -c:v libx264 /Users/owenm/Downloads/renders/output.mp4
                    
                    # ffmpeg arguments
                    args = "-y -threads 64 -r 25 "
                    args += "-i " + "\"" + jobInputFile + "\" "
                    args += "-i " + "\"" + ffmpegAudioFile + "\" "
                    args += " -pix_fmt yuv420p -c:v libx264 "
                    args += "\"" + ffmpegOutputFile + "\""

                    # execute ffmpeg
                    FFmpegExe = self.GetConfigEntryWithDefault( "FFmpegExe", "/usr/bin/ffmpeg" )

                    process = ProcessUtils.SpawnProcess( FFmpegExe, args )
                    ProcessUtils.WaitForExit( process, -1 )
                    
                    if( process.ExitCode == 0 ):
                        ClientUtils.LogText( "Successfully created FFmpeg movie: %s" % ffmpegOutputFile )
                        
                        job.SetJobExtraInfoKeyValue("Movie", ffmpegOutputFile)
                        jsonJobObject = JsonConvert.SerializeObject( job )

                        # url = self.GetConfigEntryWithDefault( "URL", "" )
                        url = job.GetJobExtraInfoKeyValueWithDefault("CallbackURL", self.GetConfigEntryWithDefault( "URL", "" ))                        

                        ClientUtils.LogText( "#########################################################################################" )
                        ClientUtils.LogText( "url: %s" % url )
                        ClientUtils.LogText( "json object: %s" % jsonJobObject )
                        ClientUtils.LogText( "#########################################################################################" )

                        # Send signal to web server here
                        req = urllib2.Request( url, jsonJobObject, {"Content-Type": "application/json"} )
                        response = urllib2.urlopen( req )

                        ClientUtils.LogText( "response: %s" % response.read() )

                    else:
                        ClientUtils.LogText( "ERROR" )

            except:
                ClientUtils.LogText( traceback.format_exc() )
