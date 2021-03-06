#!/usr/bin/env python

# audio.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Contains the audio backend functions


from kano_peripherals.pi_hat.driver.high_level import get_pihat_interface

from kano_settings.config_file import get_setting, set_setting
from kano_settings.boot_config import set_config_value, end_config_transaction
from kano.utils import run_cmd
from kano.logging import logger


amixer_control = "name='PCM Playback Route'"

analogue_value = 1
hdmi_value = 2
hdmi_string = ": values={}".format(hdmi_value)

store_cmd = "service alsa-store restart"
#amixer_set_cmd = "amixer -c 0 cset {control} {{value}}".format(
#    control=amixer_control)
amixer_get_cmd = "amixer -c 0 cget {control}".format(control=amixer_control)

analogue_cmd = "amixer -c 0 cset numid=3 1"
hdmi_cmd = "amixer -c 0 cset numid=3 2"


def is_hdmi_audio_supported():
    '''
    Returns True if the display is HDMI and has audio support
    '''
    if is_hdmi_audio_supported.hdmi_supported is not None:
        return is_hdmi_audio_supported.hdmi_supported
    try:
        from kano_settings.system.display import get_edid
        is_hdmi_audio_supported.hdmi_supported = get_edid()['hdmi_audio']
    except Exception:
        is_hdmi_audio_supported.hdmi_supported = False

    return is_hdmi_audio_supported.hdmi_supported

# local static variable to avoid calling tvservice more than once
is_hdmi_audio_supported.hdmi_supported = None


def is_analogue_audio_supported():
    """
    Check the system to see if audio through the jack is available.

    Unfortunately, the hardware for the PiHat on CK2 Lite requires disabling audio
    through the jack. This is the only instance we need to prevent jack audio.

    Returns:
        supported - True if audio can be set to play through jack, False otherwise
    """
    supported = True

    pihat_iface = get_pihat_interface()
    if pihat_iface and pihat_iface.is_plugged():
        supported = False

    return supported


def set_to_HDMI(HDMI, force=False):
    '''
    Set audio output to HDMI if supported by the display,
    otherwise set it to Analogue output.

    Returns 'HDMI' or 'Analogue', whichever was applied.
    '''

    if not is_hdmi_audio_supported() and not force:
        HDMI = False

    # 1 analog
    # 2 hdmi

    # These are the changes we'll apply if they have changed from what they were
    if HDMI:
        amixer_cmd = hdmi_cmd
        set_config_value('hdmi_ignore_edid_audio', None)
        set_config_value('hdmi_drive', 2)
        config = _("HDMI")
    else:
        amixer_cmd = analogue_cmd
        set_config_value('hdmi_ignore_edid_audio', 1)
        set_config_value('hdmi_drive', None)
        config = _("Analogue")

    end_config_transaction()

    # Set audio path in amixer
    o, e, rc = run_cmd(amixer_cmd)
    if rc:
        logger.warn("error from amixer: {} {} {}".format(o, e, rc))

    # trigger alsa-store to store the path in /var/lib/alsa/asound.state
    o, e, rc = run_cmd(store_cmd)
    if rc:
        logger.warn("error from alsa-store: {} {} {}".format(o, e, rc))

    set_setting('Audio', config)
    return config


# Returns is_HDMI = True or False
def is_HDMI():
    # Find the audio setting
    amixer_string, e, rc = run_cmd(amixer_get_cmd)
    if rc:
        logger.warn("error from amixer: {} {} {}".format(amixer_string, e, rc))

    if amixer_string.find(hdmi_string) != -1:
        # Make sure config file is up to date
        if get_setting('Audio') != _("HDMI"):
            set_setting('Audio', _("HDMI"))
        return True

    # Default to Analogue
    else:
        # Make sure config file is up to date
        if get_setting('Audio') != _("Analogue"):
            set_setting('Audio', _("Analogue"))
        return False
