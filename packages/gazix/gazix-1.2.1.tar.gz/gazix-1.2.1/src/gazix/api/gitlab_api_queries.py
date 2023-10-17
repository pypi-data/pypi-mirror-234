#########################################################################
#                                                                       #
#  This file is part of gazix.                                          #
#                                                                       #
#  gazix is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by #
#  the Free Software Foundation, either version 3 of the License, or    #
#  (at your option) any later version.                                  #
#                                                                       #
#  gazix is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        # 
#  GNU General Public License for more details.                         #
#                                                                       #
#  You should have received a copy of the GNU General Public License    #
#  along with gazix. If not, see <https://www.gnu.org/licenses/>.       #
#                                                                       #
#########################################################################

# -*- coding: utf-8 -*-
import logging

from ..utils.command import *
from ..utils.json import *
from ..utils.log import *
from .gitlab_api_object import *
import urllib.parse


def curl2json(line):
    data = command(line, output=True)
    data = read_json(data)
    return data


def get_jobs(host, project, token, filters={}):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/jobs'
    line += "?"
    for filter in filters:
        line += filter + "=" + str(filters[filter]) + "&"
    line = line[:-1]
    line += '"'
    return curl2json(line)


def get_pipeline_jobs(host, project, token, pipeline, filters={}):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/pipelines/' + str(pipeline) + '/jobs'
    line += "?"
    for filter in filters:
        line += filter + "=" + str(filters[filter]) + "&"
    line = line[:-1]
    line += '"'
    return curl2json(line)


def get_active_jobs(host, project, token):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/jobs?scope[]=pending&scope[]=running"'
    return curl2json(line)





def get_pipeline(host, project, token, pipeline):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/pipelines/' + str(pipeline) + '"'
    return curl2json(line)


def get_pipeline_variable(host, project, token, pipeline):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/pipelines/' + str(pipeline) + '/variables"'
    return curl2json(line)


def terminated(status):
    return status in ["success", "failed", "canceled", "skipped", "manual"]


def pipeline_terminated(host, project, token, pipeline):
    data = get_pipeline(host, project, token, pipeline)
    status = data["status"]
    return terminated(status)


def pipeline_success(host, project, token, pipeline):
    data = get_pipeline(host, project, token, pipeline)
    status = data["status"]
    return status in ["success"]


def get_pipelines(host, project, token, filters={}):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/pipelines'
    line += "?"
    for filter in filters:
        line += filter + "=" + str(filters[filter]) + "&"
    line = line[:-1]
    line += '"'
    return curl2json(line)


def kill_pipeline(host, project, token, pipeline):
    line = "curl -s --request POST --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/pipelines/' + str(pipeline) + '/cancel"'
    return command(line)


def get_merge_request(host, project, token, merge_request_iid, options=None):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(merge_request_iid)
    if options is not None:
        line += "?" + options
    line += '"'
    return curl2json(line)


def update_merge_request(host, project, token, merge_request_iid, options=None):
    line = "curl -s --request PUT --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(merge_request_iid)
    if options is not None:
        line += "?" + options
    line += '"'
    return curl2json(line)


def close_merge_request(host, project, token, merge_request_iid):
    line = "curl -s --request PUT --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(merge_request_iid) + '?state_event=close"'
    return curl2json(line)


def cancel_merge_when_pipeline_succeeds(host, project, token, merge_request_iid):
    line = "curl -s --request POST --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(
        merge_request_iid) + "/cancel_merge_when_pipeline_succeeds"
    line += '"'
    return curl2json(line)


def update_merge_request_merge(host, project, token, merge_request_iid, options=None):
    line = "curl -s --request PUT --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(merge_request_iid) + "/merge"
    if options is not None:
        line += "?" + options
    line += '"'
    return curl2json(line)


def close_issue(host, project, token, iid):
    line = "curl -s --request PUT --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/issues/' + str(iid) + '?state_event=close"'
    return curl2json(line)


def add_label_to_merge_request(host, project, token, merge_request_iid, old_labels, label):
    data = ""
    for lab in old_labels:
        data += lab + ","
    data += label
    line = "curl -s --request PUT --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += ' --data "labels=' + data + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(merge_request_iid) + '"'
    return curl2json(line)


def set_labels_to_merge_request(host, project, token, merge_request_iid, labels):
    data = ""
    for lab in labels:
        data += lab + ","
    data = data[:-1]
    line = "curl -s --request PUT --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += ' --data "labels=' + data + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(merge_request_iid) + '"'
    return curl2json(line)


def add_label_to_issue(host, project, token, iid, old_labels, label):
    data = ""
    for lab in old_labels:
        data += lab + ","
    data += label
    line = "curl -s --request PUT --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += ' --data "labels=' + data + '"'
    line += " " + '"' + host + '/' + project + '/issues/' + str(iid) + '"'
    return curl2json(line)


def set_labels_to_issue(host, project, token, iid, labels):
    data = ""
    for lab in labels:
        data += lab + ","
    data = data[:-1]
    line = "curl -s --request PUT --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += ' --data "labels=' + data + '"'
    line += " " + '"' + host + '/' + project + '/issues/' + str(iid) + '"'
    return curl2json(line)


def get_opened_merge_requests(host, project, token):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests?scope=all&order_by=updated_at&sort=asc&state=opened' + '"'
    return curl2json(line)


def get_ready_merge_requests(host, project, token):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests?scope=all&order_by=updated_at&sort=asc&state=opened&wip=no&target_branch=master' + '"'
    return curl2json(line)


def get_merged_merge_requests(host, project, token):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests?scope=all&order_by=updated_at&sort=desc&state=merged' + '"'
    return curl2json(line)


def get_opened_issues(host, project, token):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/issues?scope=all&order_by=updated_at&sort=asc&state=opened' + '"'
    return curl2json(line)


def get_pipelines_from_merge_request(host, project, token, merge_request_iid):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(merge_request_iid) + '/pipelines"'
    return curl2json(line)


def comment_merge_request(host, project, token, merge_request_iid, message):
    line = "curl --request POST --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(
        merge_request_iid) + '/notes?body=' + urllib.parse.quote(message) + '"'
    return command(line)


def comment_issue(host, project, token, iid, message):
    line = "curl --request POST --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/issues/' + str(iid) + '/notes?body=' + urllib.parse.quote(
        message) + '"'
    return command(line)


def rebase_merge_request(host, project, token, merge_request_iid):
    line = "curl -s --request PUT --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(merge_request_iid) + '/rebase"'
    return curl2json(line)


def is_merge_request_rebased(host, project, token, merge_request_iid):
    return get_merge_request(host, project, token, merge_request_iid, options="include_rebase_in_progress=true")


def download_job_artifacts(host, project, token, job_id, archive):
    line = "curl -s -L --output " + archive
    line += " --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/jobs/' + str(job_id) + '/artifacts"'
    return command(line)


def get_merge_request_approvals(host, project, token, merge_request):
    line = "curl -s --globoff --header "
    line += '"PRIVATE-TOKEN: ' + token + '"'
    line += " " + '"' + host + '/' + project + '/merge_requests/' + str(merge_request) + '/approvals"'
    print(line)
    return curl2json(line)


##


def is_pipeline_terminated(pipeline):
    return pipeline["status"] in ["success", "failed", "canceled", "skipped", "manual"]


class GitLabAPIQueries:

    def __init__(self, access):
        self._access = access

    def GET(self, query, query2=None):
        line = "curl -s --globoff --header "
        line += '"PRIVATE-TOKEN: ' + self._access.get_token() + '"'
        line += " " + '"' + self._access.get_url()
        line += '/projects/' + self._access.get_project() + "/"
        if isinstance(query, str):
            line += query
        if isinstance(query, GitLabAPIObject):
            line += query.get_type() + "/" + query.get_query()
        if query2 is not None:
            if isinstance(query2, str):
                line += "/" + query2
        line += '"'
        return line

    def PUT(self, query, data=None):
        logging.debug(query)
        line = "curl -s --header "
        line += '"PRIVATE-TOKEN: ' + self._access.get_token() + '"'
        if data is not None:
            line += ' --data "' + data + '"'
        line += " " + '"' + self._access.get_url()
        line += '/projects/' + self._access.get_project() + "/" + query + '"'
        return line

    def POST(self, query, data=None, query2=None):
        logging.debug(query)
        line = "curl -s --request POST --header "
        line += '"PRIVATE-TOKEN: ' + self._access.get_token() + '"'
        if data is not None:
            line += ' --data "' + data + '"'
        line += " " + '"' + self._access.get_url()
        line += '/projects/' + self._access.get_project() + "/"
        if isinstance(query, str):
            line += query
        if isinstance(query, GitLabAPIObject):
            line += query.get_type() + "/" + query.get_query()
        if query2 is not None:
            if isinstance(query2, str):
                line += "/" + query2
        line += '"'
        return line

    def list_labels(self):
        return curl2json(self.GET("labels"))

    def create(self, obj):
        return curl2json(self.PUT(obj.get_type(), obj.get_url()))

    def trigger_pipeline(self, reference, variables):
        line = "curl -s -X POST"
        line += " -F token=" + self._access.get_token()
        line += ' -F "ref=' + reference + '"'
        for var in variables:
            line += ' -F "variables[' + var + ']=' + variables[var] + '"'
            line += " " + '"' + self._access.get_url()
            line += '/projects/' + self._access.get_project()
            line += '/trigger/pipeline"'
        return curl2json(line)

    def is_pipeline_terminated(self, pipeline):
        return is_pipeline_terminated(self.GET(pipeline))

