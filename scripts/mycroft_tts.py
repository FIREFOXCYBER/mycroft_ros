# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
    Mycroft audio service.
    This handles playback of audio and speech
"""
#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from mycroft.configuration import Configuration
from mycroft.messagebus.client.ws import WebsocketClient
from mycroft.messagebus.message import Message
from mycroft.util import reset_sigint_handler, wait_for_exit_signal, \
    create_daemon, create_echo_function, check_for_signal
from mycroft.util.log import LOG

import mycroft.audio.speech as speech
from mycroft.audio.audioservice import AudioService

bus = None

def handle_speak(data):
    global bus
    bus.emit(Message('speak', {'utterance': data.data}))

def handle_stop(data):
    global bus
    bus.emit(Message('mycroft.stop'))

def main():
    rospy.init_node('mycroft_tts')
    rospy.loginfo(rospy.get_caller_id() + " started")
    rospy.Subscriber("mycroft/speak", String, handle_speak)
    rospy.Subscriber("mycroft/stop", String, handle_stop)
    """ Main function. Run when file is invoked. """
    global bus
    reset_sigint_handler()
    check_for_signal("isSpeaking")
    bus = WebsocketClient()  # Connect to the Mycroft Messagebus
    Configuration.init(bus)
    speech.init(bus)

    LOG.info("Starting Audio Services")
    bus.on('message', create_echo_function('AUDIO', ['mycroft.audio.service']))
    audio = AudioService(bus)  # Connect audio service instance to message bus
    create_daemon(bus.run_forever)

    wait_for_exit_signal()

    speech.shutdown()
    audio.shutdown()
    # keep node running
    rospy.spin()


if __name__ == "__main__":
    main()
