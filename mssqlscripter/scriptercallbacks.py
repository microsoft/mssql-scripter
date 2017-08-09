# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import sys


def handle_response(response, display=False):
    """
        Dispatch response based on scripting response or event.
    """

    def handle_script_response(response, display=False):
        if display:
            sys.stderr.write(
                u'Scripting request submitted with request id: {}\n'.format(
                    response.operation_id))

    def handle_script_plan_notification(response, display=False):
        if display:
            sys.stderr.write(
                u'Scripting request: {} plan: {} database objects\n'.format(
                    response.operation_id, response.count))

    def handle_script_progress_notification(response, display=False):
        if display:
            sys.stderr.write(
                u'Scripting progress: Status: {} Progress: {} out of {} objects scripted\n'.format(
                    response.status, response.completed_count, response.total_count))

    def handle_script_complete(response, display=False):
        if response.has_error:
            # Always display error messages.
            sys.stdout.write(
                u'Scripting request: {} encountered error: {}\n'.format(
                    response.operation_id, response.error_message))
            sys.stdout.write(u'Error details: {}\n'.format(response.error_details))
        elif display:
            sys.stderr.write(
                u'Scripting request: {} completed\n'.format(response.operation_id))

    response_handlers = {
        u'ScriptResponse': handle_script_response,
        u'ScriptPlanNotificationEvent': handle_script_plan_notification,
        u'ScriptProgressNotificationEvent': handle_script_progress_notification,
        u'ScriptCompleteEvent': handle_script_complete}

    response_name = type(response).__name__

    if response_name in response_handlers:
        return response_handlers[response_name](response, display)
