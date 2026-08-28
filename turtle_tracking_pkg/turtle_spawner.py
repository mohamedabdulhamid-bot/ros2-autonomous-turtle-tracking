#!/usr/bin/env python3#
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
import time
import random
from my_interfaces.msg import NewTurtlePose


class My_turtle(Node):
    def __init__(self):
        super().__init__('spawner')
        self.spawner_client_=self.create_client(
            Spawn,'/spawn')
        self.get_logger().info('Spawner node has been started')
        #publishing the new turtle pose
        self.pose_pub=self.create_publisher(
            NewTurtlePose,'NewTurtlePose',10)
    
        
    
    def send_request(self,x_,y_,theta_,name_):
        while not self.spawner_client_.wait_for_service(1):
            self.get_logger().warn('waiting for the service.......')
            
        request=Spawn.Request()
        request.x=x_
        request.y=y_
        request.theta=theta_
        request.name=name_
        future=self.spawner_client_.call_async(request)
        rclpy.spin_until_future_complete(self,future)
        response=future.result()
        
        self.get_logger().info(f'{response.name} has been spawned')
        
        turtle_pose=NewTurtlePose()
        turtle_pose.x=x_
        turtle_pose.y=y_
        turtle_pose.theta=theta_
        turtle_pose.name=name_
        #publishing turtle pose
        self.pose_pub.publish(turtle_pose)
        
    
        

def main():
    rclpy.init()
    node=My_turtle()
    turtle_count_=2
    while True:
        x=random.uniform(2,10)
        y=random.uniform(2,10)
        theta=x=random.uniform(0,6)
        node.send_request(x,y,theta,f'turtle{turtle_count_}')
        turtle_count_+=1
        time.sleep(1)
    rclpy.spin(node)
    rclpy.shutdown()
if __name__=='__main__':
    main()
