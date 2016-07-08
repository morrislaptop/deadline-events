import urllib.request

from Deadline.Events import *
from Deadline.Scripting import *

######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
######################################################################
def GetDeadlineEventListener():
    return NotifyEvent()

######################################################################
## This is the function that Deadline calls when the event plugin is
## no longer in use so that it can get cleaned up.
######################################################################
def CleanupDeadlineEventListener( deadlinePlugin ):
    deadlinePlugin.Cleanup()

######################################################################
## This is the main DeadlineEventListener class for MyEvent.
######################################################################
class NotifyEvent (DeadlineEventListener):

    def __init__( self ):
        # Set up the event callbacks here
        self.OnJobSubmittedCallback += self.OnJobSubmitted
        self.OnJobFinishedCallback += self.OnJobFinished

    def Cleanup( self ):
        del self.OnJobSubmittedCallback
        del self.OnJobFinishedCallback

    def OnJobSubmitted( self, job ):
        # TODO: Connect to pipeline site to notify it that a job has been submitted
        # for a particular shot or task.
        pass

    def OnJobFinished( self, job ):
        
        pass
        # Only submit a QT job for finished Nuke jobs, and only if a QT settings file has been set.
        # if job.JobPlugin != "Nuke":
            # return

        # callbackUrl = job.GetJobExtraInfoKeyValueWithDefault("CallbackURL", "false")
        
        # ClientUtils.LogText("CallbackURL=%s" % callbackUrl)
        
        # urllib.request.urlopen(callbackUrl).read()
