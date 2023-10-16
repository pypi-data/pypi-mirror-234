import logging
from datetime import datetime

import requests
from aprsd import packets, plugin, plugin_utils
from aprsd.utils import trace
from oslo_config import cfg

import aprsd_wxnow_plugin
from aprsd_wxnow_plugin import conf  # noqa


CONF = cfg.CONF
LOG = logging.getLogger("APRSD")

API_KEY_HEADER = "X-Api-Key"


class InvalidRequest(Exception):
    message = "Couldn't decipher request"


class NoAPRSFIApiKeyException(Exception):
    message = "No aprs.fi ApiKey found in config"


class NoAPRSFILocationException(Exception):
    message = "Unable to find location from aprs.fi"


class WXNowPlugin(
    plugin.APRSDRegexCommandPluginBase,
    plugin.APRSFIKEYMixin,
):

    version = aprsd_wxnow_plugin.__version__
    command_regex = r"^([n]|[n]\s|nearest)"
    command_name = "nearest"

    enabled = False

    def setup(self):
        """Allows the plugin to do some 'setup' type checks in here.

        If the setup checks fail, set the self.enabled = False.  This
        will prevent the plugin from being called when packets are
        received."""
        # Do some checks here?
        LOG.info("WXNowPlugin::setup()")
        self.enabled = True
        self.ensure_aprs_fi_key()
        if not CONF.aprsd_wxnow_plugin.haminfo_apiKey:
            LOG.error("Missing aprsd_wxnow_plugin.haminfo_apiKey")
            self.enabled = False

        if not CONF.aprsd_wxnow_plugin.haminfo_base_url:
            LOG.error("Missing aprsd_wxnow_plugin.haminfo_base_url")
            self.enabled = False

    def help(self):
        _help = [
            "nearest: Return nearest weather to your last beacon.",
            "nearest: Send 'n [count]'",
        ]
        return _help

    @staticmethod
    def is_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def fetch_data(self, packet):
        fromcall = packet.from_call
        message = packet.message_text

        # get last location of a callsign, get descriptive name from weather service
        api_key = CONF.aprs_fi.apiKey

        try:
            aprs_data = plugin_utils.get_aprs_fi(api_key, fromcall)
        except Exception as ex:
            LOG.exception(ex)
            LOG.error(f"Failed to fetch aprs.fi '{ex}'")
            raise NoAPRSFILocationException()

        if not len(aprs_data["entries"]):
            LOG.error("Didn't get any entries from aprs.fi")
            raise NoAPRSFILocationException()

        lat = aprs_data["entries"][0]["lat"]
        lon = aprs_data["entries"][0]["lng"]

        command_parts = message.split(" ")
        LOG.info(command_parts)

        count = None
        for part in command_parts[1:]:
            if self.is_int(part):
                # this is the number of stations
                count = int(part)
                # Lets max out at 10 replies
                if count > 5:
                    count = 5
            elif not part:
                continue
            else:
                # We don't know what they are asking for
                raise InvalidRequest()

        if not count:
            count = 1

        LOG.info(
            f"Looking for the nearest {count} weather stations"
            f" from {lat}/{lon}",
        )

        try:
            url = "{}/wxnearest".format(
                CONF.aprsd_wxnow_plugin.haminfo_base_url,
            )
            api_key = CONF.aprsd_wxnow_plugin.haminfo_apiKey
            params = {
                "lat": lat, "lon": lon,
                "count": count,
                "callsign": fromcall,
            }

            headers = {API_KEY_HEADER: api_key}
            result = requests.post(url=url, json=params, headers=headers)
            data = result.json()

        except Exception as ex:
            LOG.error(f"Couldn't fetch nearest stations '{ex}'")
            data = None

        return data

    @trace.trace
    def process(self, packet: packets.core.Packet):
        """This is called when a received packet matches self.command_regex.

        This is only called when self.enabled = True and the command_regex
        matches in the contents of the packet["message_text"]."""

        LOG.info("WXNowPlugin Plugin Called")

        packet.from_call
        packet.message_text

        try:
            data = self.fetch_data(packet)
        except NoAPRSFILocationException as ex:
            return ex.message
        except NoAPRSFILocationException as ex:
            return ex.message
        except InvalidRequest as ex:
            return ex.message
        except Exception:
            return "Failed to fetch data"

        if data:
            # just do the first one for now
            replies = []
            for entry in data:
                LOG.info(f"Using {entry}")

                # US and UK are in miles, everywhere else is metric?
                # by default units are meters
                distance = entry["distance"]
                units = entry["distance_units"]
                if entry["distance_units"] == "meters":
                    units = "m"
                # Convert C to F
                temperature = (entry["report"]["temperature"] * 1.8) + 32
                wind_dir = entry["report"]["wind_direction"]
                wind_speed = entry["report"]["wind_gust"]

                date = datetime.strptime(entry["report"]["time"], "%Y-%m-%d %H:%M:%S")
                date_str = date.strftime("%m/%d %H:%M")
                reply1 = (
                    f"{entry['callsign']} "
                    f"{date_str} "
                    f"{distance}{units} {entry['direction']} "
                    f"{temperature:.0f}F "
                    f"{entry['report']['humidity']}% "
                    f"{entry['report']['pressure']}mbar "
                )
                reply2 = (
                    f"{entry['callsign']} "
                    f"Wind {wind_dir}@{wind_speed:.0f} "
                    f"Rain1h {entry['report']['rain_1h']} "
                    f"Rain24h {entry['report']['rain_24h']} "
                )
                replies.append(reply1)
                replies.append(reply2)
            return replies
        else:
            return "None Found"
