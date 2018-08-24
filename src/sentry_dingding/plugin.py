# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_dingding
from .forms import DingDingOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'icherish'
    author_url = 'https://github.com/icherisher/sentry-dingding2'
    version = sentry_dingding.VERSION
    description = 'Send error counts to DingDing.'
    slug = 'DingDing'
    title = 'DingDing'
    conf_key = slug
    conf_title = title
    resource_links = [
        ('Source', 'https://github.com/icherisher/sentry-dingding2'),
        ('Bug Tracker', 'https://github.com/icherisher/sentry-dingding2/issues'),
        ('README', 'https://github.com/icherisher/sentry-dingding2/blob/master/README.md'),
    ]
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def post_process(self, group, event, is_new, is_sample, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        access_token = self.get_option('access_token', group.project)

        send_url = DingTalk_API.format(token=access_token)

        metadata = event.get_event_metadata()

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "{0}".format(metadata["type"]),
                "text": "#### {title}  \n > {message} [href]({url})".format(
                    # title=metadata["type"],
                    title='我的测试服额',
                    message=event.message,
                    url="{0}events/{1}/".format(group.get_absolute_url(), event.id)
                )
            }
        }

        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
