# mycroft_ros
This package provides capability to run the Text-To-Speech, Speech-To-Text and Skill functionality of Mycroft AI as ROS nodes providing topics, services and actions for communication.

The package makes use of the catkin_virtualenv library to run the Mycroft nodes within a seperate Python virtual environment
## Installation
The dev_setup.sh can be used to install dependencies and configure the package for use. 
## Mycroft Setup
Mycroft can be configured using either **~/.mycroft/mycroft.conf** or **/etc/mycroft/mycroft.conf**
## Topics, Services and Actions
### Topics
* **mycroft/speak (std_msgs/String)** - String for Mycroft TTS to read
* **mycroft/utterance (std_msgs/String)** - String to pass to the intent service
* **mycroft/speech (mycroft_ros/Speech)** - List of Strings received from Mycroft STT
* **mycroft/remove_skill (std_msgs/String)** - Path of skill to remove from SkillManager as a String
### Services
* **mycroft/register_skill (mycroft_ros/MycroftSkill)** - Register the skill in the SkillManager
### Actions
* **mycroft/get_response (mycroft_ros/GetResponse)** - Reads dialog before recording and returning user response
* **mycroft/ask_yesno (mycroft_ros/GetResponse)** - Reads dialog before recording and returning "yes" or "no" based on user 
response
## Example
### Skill/Node Structure
ROS nodes that are to be used as MycroftSkill's should be placed within their own directory with relevent 'vocab', 'dialog' and 'regex' directories to use for intents and entities
### Using the RosMycroftSkill
The mycroft_ros Python module provides helper functions and classes for convenience such as the RosMycroftSkill which can be used to register nodes as a MycroftSkill
``` python
class ExampleSkill(RosMycroftSkill):

    def __init__(self):
        super(ExampleSkill, self).__init__("/home/vagrant/dev/catkin_ws/src/mycroft_ros/scripts/example")
        self.register_intent(IntentBuilder("MycroftRos").require("mycroft").require("ros"), self.example)
        self.register_intent_file("mytest.intent", self.mytest)
        if self.initialise():
            rospy.loginfo("created")
        else:
            rospy.loginfo("not created")

    def example(self, data):
        rospy.loginfo("MycroftRos callback")
        user_response = self.get_response(dialog="say something cool to me")
        rospy.loginfo("Response: " + user_response)

    def mytest(self, data):
        rospy.loginfo("mytest callback")

if __name__ == "__main__":
    rospy.init_node('example_mycroft_ros_skill')
    ExampleSkill()
    rospy.spin()
```
## TODO
* add context to Skills
* add speak_dialog
* add Skill events / repeating events
* error handling for skills
