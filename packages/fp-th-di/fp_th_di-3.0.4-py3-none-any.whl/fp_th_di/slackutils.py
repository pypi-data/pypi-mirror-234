#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""This script contains helper functions to post message to slack channel
"""
from fp_th_di.logger import logger
import requests

class SlackBotMessenger:
  def post_json_to_slack(self, json:dict, channelUrl:str):
    """
      Sends data to Slack channel
      --------
      Args:
        filepath: string, required
          path to file to be sent to the targeted Slack channel
        channelUrl: string, required
          Webhook url of the targeted Slack channel.
    """

    try:
      requests.post(url=channelUrl, json=json)
    except Exception as e:
      logger.error(e)

  def post_message_to_slack(self, message:str, channelUrl:str):
    """
      Sends text message to Slack channel by webhook url
      Uses <@slack_member_id> to mention slack users
      --------
      Args:
        message: string, required
          message to send
        channelUrl: string, required
          Webhook url of the targeted Slack channel.
    """
    self.post_json_to_slack({'text': message}, channelUrl)
