import os
import threading
import time
import socket
import json
from queue import Queue
from .adapter import Adapter
from .jobcontext import JobContext


class Channel(threading.Thread):
    def __init__(self, home, logger, devel=False):
        super().__init__()
        self.daemon = True
        self.que = Queue()
        self.hostname = socket.gethostname()
        self.home = home
        self.logger = logger
        self.runnable = True
        self.devel = devel

    def stop(self):
        self.runnable = False

    def run(self):
        adapter = Adapter(self.home, self.logger)
        if not adapter.open():
            self.logger.warning("main, channel: can not open adapter")
            return

        self.logger.debug("main, channel manager start")
        while self.runnable:
            if self.que.qsize() > 0:
                d = self._dequeue()
                adapter.publish(d['exchange'], d['routing_key'], d['body'])
            else:
                time.sleep(5/1000)
        self.logger.debug("main, channel manager stop")
        adapter.close()


    def _dequeue(self):
        return self.que.get()

    def _enqueue(self, exchange, routing_key, json_msg):
        data = {}
        data['exchange'] = exchange
        data['routing_key'] = routing_key
        data['body'] = json_msg
        self.que.put(data)

    """
    TY_METRIC_WM       1
    TY_METRIC_AGENT    2
    TY_METRIC_PLUGIN   3
    TY_METRIC_WORKER   4
    TY_METRIC_APP      5
    """
    def publish_heartbeat(self, namespace, worker_name):
        if self.devel:
            return
        data = {}
        data['metric-type'] = 4
        data['metric-status'] = 0
        data['metric-name'] = 'worker'
        data['namespace'] = namespace
        data['process'] = worker_name
        data['psn'] = 0
        data['hostname'] = self.hostname
        data['timestamp'] = 0
        routing_key = 'sys.' + namespace + '.heartbeat'
        self._enqueue(Adapter.EXCHANGE_METRIC, routing_key, json.dumps(data))

    def publish_job(self, context:JobContext):
        if self.devel:
            return
        data = {}
        data['regkey'] = context.regkey
        data['topic'] = context.topic
        data['author'] = context.author
        data['action-id'] = context.action_id
        data['action-ns'] = context.action_ns
        data['action-app'] = context.action_app
        data['action-params'] = context.action_params
        data['job-id'] = context.job_id
        data['timestamp'] = context.timestamp
        data['filenames'] = context.filenames
        data['msgbox'] = context.msgbox

        if context.timestamp == 0:
            routing_key = 'job.des.cwm.early.' + context.topic
        else:
            routing_key = 'job.des.cwm.now.' + context.topic
        json_str = json.dumps(data)
        self.logger.debug("sent message, %s", json_str)
        self._enqueue(Adapter.EXCHANGE_ACTION, routing_key, json_str)

    """status code
    STATUS_JOB_CREATED    1  /* 작업생성 */
    STATUS_JOB_STARTED    2  /* 작업시작 */
    STATUS_JOB_RUNNING    3  /* 작업수행중 */
    STATUS_JOB_ENDED      4  /* 작업종료(정상) */
    STATUS_JOB_FINISHED   5  /* 액션트리 종료 */
    STATUS_JOB_ARBORTED   6  /* 작업강제중단 */
    STATUS_JOB_FAILED     7  /* 작업오류 */
    STATUS_JOB_RETRY      8  /* 작업오류 재처리 */
    """
    def publish_notify(self, context:JobContext, text='', status=3, elapsed=0):
        if self.devel:
            return
        data = {}
        data['job-id'] = context.job_id
        data['job-status'] = status
        data['job-elapsed'] = elapsed
        data['reg-subject'] = context.regkey.split('@')[0]
        data['reg-version'] = context.regkey.split('@')[1]
        data['reg-topic'] = context.topic
        data['action-id'] = context.action_id
        data['action-app'] = context.action_app
        data['action-ns'] = context.action_ns
        data['hostname'] = self.hostname
        data['timestamp'] = int(time.time())
        filesize = 0
        for file in context.filenames:
            try:
                filesize += os.stat(file).st_size
            except:
                continue

        data['filesize'] = filesize
        data['filenames'] = context.filenames
        data['err-code'] = 0
        data['err-mesg'] = text

        routing_key = 'log.' + context.action_ns
        self._enqueue(Adapter.EXCHANGE_LOGS, routing_key, json.dumps(data))

