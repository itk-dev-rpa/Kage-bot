"""This module contains the main process of the robot."""

from datetime import datetime
import os
import json

import yaml
from itk_dev_shared_components.smtp import smtp_util
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection

from robot_framework import config


# pylint: disable-next=unused-argument
def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")

    mail_list = json.loads(orchestrator_connection.process_arguments)

    with open("kageliste.yaml", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    year = datetime.today().year
    week = datetime.today().isocalendar().week

    person = data[year][week]

    if not person:
        orchestrator_connection.log_info(f"No person on the cake list this week. Week: {week}")
        return

    mail = mail_list[person]

    orchestrator_connection.log_info(f"It is now week {week}. Sending mail to {person} at {mail}")

    smtp_util.send_email(
        receiver=f"{mail}@aarhus.dk",
        sender="kagebot@friend.dk",
        subject="Du skal have kage med!",
        body=f"Hejsa {person}\n\nVidste du at det er din tur til at have kage med i denne uge?\n\nVenlig hilsen\nKagebot",
        smtp_server=config.SMTP_SERVER,
        smtp_port=config.SMTP_PORT
    )


if __name__ == '__main__':
    conn_string = os.getenv("OpenOrchestratorConnString")
    crypto_key = os.getenv("OpenOrchestratorKey")
    oc = OrchestratorConnection("Kagebot test", conn_string, crypto_key, "", "")
    process(oc)
