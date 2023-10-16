import traceback
from ciocore import conductor_submit

from cioblender import submission_dialog
#import bpy

def invoke_submission_dialog(payload):
    """
    Execute the modal submission dialog given nodes.
    """
    try:
        print("Call SubmissionDialog ...")
        submission_dialog.run(payload)

    except Exception as e:
        print("Error in calling SubmissionDialog: {}".format(e))
        pass


def submit_job(payload):

    try:
        #print("Submitting job: ", payload)
        print("upload_paths: ", payload.get("upload_paths"))
        remote_job = conductor_submit.Submit(payload)
        response, response_code = remote_job.main()
    except:
        response = traceback.format_exc()
        response_code = 500
    return {"response": response, "response_code": response_code}
