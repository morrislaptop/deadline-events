from Deadline.Events import *
from Deadline.Scripting import *

######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
######################################################################
def GetDeadlineEventListener():
    return MyEvent()

######################################################################
## This is the function that Deadline calls when the event plugin is
## no longer in use so that it can get cleaned up.
######################################################################
def CleanupDeadlineEventListener( deadlinePlugin ):
    deadlinePlugin.Cleanup()

######################################################################
## This is the main DeadlineEventListener class for MyEvent.
######################################################################
class MyEvent (DeadlineEventListener):

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
		ClientUtils.LogText("Job Submitted CRAIG")
        pass

    def OnJobFinished( self, job ):
        # TODO: Connect to pipeline site to notify it that the job for a particular
        # shot or task is complete.
		ClientUtils.LogText("Job Finished CRAIG")
        pass
