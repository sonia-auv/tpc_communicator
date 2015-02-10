#!/usr/bin/env python

import communication
# ROS imports
import rospy
from auv6_communicator.srv import Test as SERVICE_REF
import parser

# Set the IP adress of the java socket server, localhost if on the same machine
TCP_IP = '127.0.0.1'
# Set the writing port of the socket |-> reading_port = port + 1
TCP_PORT = 46626
# Name of this current Node
NODE_NAME = 'auv6_communicator'
# ROS Service name
SERVICE_NAME = 'test_service_server'


class ROSJavaCommunicator(object):

    def __init__(self):
        rospy.init_node(NODE_NAME, anonymous=False)
        self.topics = []

        self.java_line = communication.JavaCommunicationLine(
            TCP_IP, TCP_PORT)
        self.ros_service_line = communication.ROSServiceCommunicationLine(
            SERVICE_NAME, SERVICE_REF)

        self.java_line.attach(self.ros_service_line)
        self.ros_service_line.attach(self)

        self.java_line.start()
        self.ros_service_line.start()

        rospy.spin()

    def update(self, service):
        response = service.recv()
        parsed_response = parser.parse_service_response(response)
        topic = communication.ROSTopicCommunicationLine(
            parsed_response[0], parsed_response[1])
        topic.attach(self.java_line)
        self.topics.append(topic)


if __name__ == '__main__':
    ROSJavaCommunicator()
