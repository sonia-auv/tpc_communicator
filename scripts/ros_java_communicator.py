#!/usr/bin/env python

import communication
from observer import Observer
# ROS imports
import rospy
from sonia_msgs.srv import vision_server_execute_cmd as SERVICE_REF

# Set the IP adress of the java socket server, localhost if on the same machine
TCP_IP = '127.0.0.1'
# Set the writing port of the socket |-> reading_port = port + 1
TCP_PORT = 46626
# Name of the current Node
NODE_NAME = 'auv6_communicator'
# ROS Service name
SERVICE_NAME = '/vision_server/vision_server_execute_cmd'


class ROSJavaCommunicator(Observer):

    def __init__(self):
        rospy.init_node(NODE_NAME, anonymous=False)
        self._topics = []

        self.ros_service_line = communication.ROSServiceCommunicationLine(
            SERVICE_NAME, SERVICE_REF)
        self.java_line = communication.JavaCommunicationLine(
            TCP_IP, TCP_PORT)

        self.java_line.attach(self.ros_service_line)
        self.ros_service_line.attach(self)

        rospy.spin()

    def _update(self, service):
        service.recv()  # TODO topic_name = service.recv()
        topic_name = 'test_talker'

        for topic in self._topics:
            if topic.get_name() == topic_name:
                rospy.logwarn(
                    "Sorry, but {!s} is already listening on topic {!s}"
                    .format(self.java_line.get_name(), topic.get_name()))
                return

        topic = communication.ROSTopicCommunicationLine(topic_name)
        topic.attach(self.java_line)
        self._topics.append(topic)

    def get_name(self):
        return "Control Loop"


if __name__ == '__main__':
    ROSJavaCommunicator()
