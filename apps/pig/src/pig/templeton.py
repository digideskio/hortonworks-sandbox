# -*- coding: utf-8 -*-
# Licensed to Hortonworks, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Hortonworks, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib
import urllib2
import simplejson as json


TEMPLETON_URL = "http://localhost:50111/templeton/v1/"


class Templeton(object):

    def __init__(self, user="hdfs"):
        self.user = user

    def get(self, url, data=None):
        """
        Make GET query to templeton url.
        """
        if data is not None:
            data['user.name'] = self.user
        else:
            data = {"user.name": self.user}
        data = urllib.urlencode(data)
        response = urllib2.urlopen(TEMPLETON_URL + url + "?" + data)
        return json.loads(response.read())

    def post(self, url, data=None):
        """
        Make POST query to templeton url.
        """
        if data is not None:
            data['user.name'] = self.user
        else:
            data = {"user.name": self.user}
        data = urllib.urlencode(data)
        req = urllib2.Request(TEMPLETON_URL + url, data)
        response = urllib2.urlopen(req)
        return json.loads(response.read())

    def delete(self, url, data=None):
        """
        Make DELETE query to templeton url.
        """
        if data is not None:
            data['user.name'] = "sandbox"
        else:
            data = {"user.name": "sandbox"}
        data = urllib.urlencode(data)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        req = urllib2.Request(TEMPLETON_URL + url + "?" + data)
        req.get_method = lambda: 'DELETE'
        response = opener.open(req)
        return json.loads(response.read())


    def pig_query(self, execute=None, pig_file=None, statusdir=None, callback=None):
        """
        Create and queue a Pig job.

        Keyword arguments:
        user -- Hue/Hadoop user
        execute -- String containing an entire, short pig program to run. (e.g. pwd)
        file -- HDFS file name of a pig program to run. (One of either "execcute" or "file" is required )
        statusdir -- A directory where Templeton will write the status of the Pig job. If
                     provided, it is the caller's responsibility to remove this directory when done.
        callback -- Define a URL to Optional be called upon job completion. You may embed a specific job
                    ID into this URL using $jobId. This tag will be replaced in the callback URL with this job's job
                    ID.

        Returns dict:
        id -- A string containing the job ID similar to "job_201110132141_0001".
        info -- A JSON object containing the information returned when the job was queued.
        """        
        if not any([execute, pig_file]):
            raise Exception("""One of either "execcute" or "file" is required""")
        data = {}
        if execute:
            data['execute'] = execute
        if pig_file:
            data['file'] = pig_file
        if statusdir:
            data['statusdir'] = statusdir
        if callback:
            data['callback'] = callback
        return self.post("pig", data)

    def check_job(self, job_id):
        """
        Check the status of a job and get related job information given its job ID.
        """
        return self.get("queue/%s" % job_id)

    def kill_job(self, job_id):
        """
        Kill a job given its job ID.
        """
        return self.delete("queue/%s" % job_id)
