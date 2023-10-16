#!/usr/bin/env python

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from loguru import logger

class SlackConnector():
    """A class for connecting to Slack and sending notifications.

    Parameters
    ----------
    name : str, optional
        The name of the SlackConnector instance. Defaults to 'SlackConnector'.

    Attributes
    ----------
    sc : slack_sdk.web.client.WebClient
        The Slack web client used for sending notifications.
    slack_user_id : str
        The ID of the Slack user to send notifications to.
    name : str
        The name of the SlackConnector instance.

    Raises
    ------
    Exception
        If the Slack token is found but the connection fails.

    Examples
    --------
    >>> import slackconnector
    >>> sc = slackconnector.SlackConnector('name')
    >>> sc.notify('Hello world.')

    """
    def __init__(self, name = None):
        self.sc, self.slack_user_id = None, None
        self.name = name if name else 'Runner'
        if 'SLACK_BOT_TOKEN' in os.environ and 'SLACK_USER_ID' in os.environ:
            self.sc = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
            self.slack_user_id = os.environ.get('SLACK_USER_ID')
            try:
                response = self.sc.auth_test()
                logger.info('Connected to Slack.')
            except SlackApiError as e:
                print(f"Error: {e.response['error']}")
                raise Exception('Slack token found but connection failed.')
        else:
            logger.info('SLACK_BOT_TOKEN and SLACK_USER_ID not found. Cannot connect to Slack.')
    
    def notify(self, msg):
        """Send a notification to a Slack user.

        Parameters
        ----------
        msg : str
            The message to send.

        Raises
        ------
        SlackApiError
            If the notification fails to send.

        Examples
        --------
        >>> sc.notify('Hello world.')

        """
        try:
            m = self.sc.chat_postMessage(channel=self.slack_user_id, text = msg, username=self.name) # , as_user = False 
            assert m["message"]["text"] == msg
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            logger.info(f"Got an error: {e.response['error']}")