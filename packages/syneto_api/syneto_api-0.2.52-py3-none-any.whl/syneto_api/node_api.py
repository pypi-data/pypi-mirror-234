import os
from .api_client import APIClientBase


class Node(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(url_base or os.environ.get("NODE_SERVICE", ""), **kwargs)

    def get_installed_version(self):
        return self.get_request("/software/installed")

    def get_available_upgrade_versions(self):
        return self.get_request("/software/available")

    def check_available_updates(self):
        return self.post_request("/software/available")

    def get_update_job(self):
        return self.get_request("/software/update")

    def start_update_job(
        self,
        upgrade_branch: str,
        upgrade_channel: str,
        enable_hotfix_channels: bool = False,
        enable_dev_channels: bool = False,
    ):
        body = {
            "upgradeBranch": upgrade_branch,
            "upgradeChannel": upgrade_channel,
            "enableHotfixChannels": enable_hotfix_channels,
            "enableDevChannels": enable_dev_channels,
        }
        return self.post_request("/software/update", body=body)

    def update_job_acknowledge(self):
        return self.put_request("/software/update/acknowledge")

    def get_system_details(self):
        return self.get_request("/system")

    def get_system_health(self):
        return self.get_request("/health")

    def get_time(self):
        return self.get_request("/time")

    def set_time(self, date: str, timezone: str, require_reboot: bool, ntp: dict):
        body = {
            "date": date,
            "timezone": timezone,
            "requireReboot": require_reboot,
            "ntp": ntp,
        }
        return self.post_request("/time", body=body)

    def get_available_timezones(self):
        return self.get_request("/time/timezones")

    def sync_clock_with_ntp(self, require_reboot: bool = False):
        body = {
            "requireReboot": require_reboot,
        }
        return self.put_request("/time/ntp/sync-clock", body=body)

    def reboot_host(self):
        return self.put_request("/reboot")

    def poweroff_host(self):
        return self.put_request("/poweroff")

    def add_user_event(self, _type: str, client_time: str, order: int, properties: dict):
        body = {
            "type": _type,
            "clientTime": client_time,
            "order": order,
            "properties": properties,
        }
        return self.post_request("/bond/user-events", body=body)

    def get_interfaces(self):
        return self.get_request("/interfaces")
