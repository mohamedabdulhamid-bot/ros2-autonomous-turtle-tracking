#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Kill
from geometry_msgs.msg import Twist
from my_interfaces.msg import NewTurtlePose
import math

class My_turtle(Node):
    def __init__(self):
        super().__init__('controller')
        
        self.turtle1_pose = None
        self.new_turtle_pose = None
        
        self.get_logger().info('controller node has been started')
        self.pose_turtle_sub_=self.create_subscription(
            Pose,'/turtle1/pose',self.turtle1_pose_callback,10)
        self.cmd_vel_pub=self.create_publisher(
            Twist,'/turtle1/cmd_vel',10)
        self.new_turtle_pose_sub=self.create_subscription(
            NewTurtlePose,'NewTurtlePose',self.new_turtle_pose_callback,10)
        
        self.timer = self.create_timer(0.1, self.cmd_vel_publisher)
        
        #killer client
        self.killer_client=self.create_client(
            Kill,'/kill')
    def turtle1_pose_callback(self,pose=Pose()):
       self.turtle1_pose=pose
       #print (f'turtle1_pose.x:{pose.x}')
       #print (f'turtle1_pose.y:{pose.y}')
       #print (f'turtle1_pose.theta:{pose.theta}')
       
    
    def new_turtle_pose_callback(self,new_pose=NewTurtlePose()):
       self.new_turtle_pose=new_pose
       #print (f'new_turtle_pose.x:{new_pose.x}')
       #print (f'new_turtle_pose.y:{new_pose.y}')
       #print (f'new_turtle_pose.theta:{new_pose.theta}')
    
    def cmd_vel_publisher(self):
        
        if self.turtle1_pose is None or self.new_turtle_pose is None:
            self.get_logger().warn('no pose')
            return  
        #linear
        dist_x=self.new_turtle_pose.x - self.turtle1_pose.x
        dist_y=self.new_turtle_pose.y - self.turtle1_pose.y
        dist=math.sqrt(pow(dist_x,2)+pow(dist_y,2))
        #angular
        target_angel=math.atan2(dist_y,dist_x)
        diff=target_angel - self.turtle1_pose.theta
        
        cmd_vel=Twist()
        #linear
        if(dist>0.1):
            cmd_vel.linear.x= dist*6#0.9
        #angular
            cmd_vel.angular.z=self.normalization_angle(diff)*10
        #killing the turtle
            if(dist<0.5):
                self.killer(self.new_turtle_pose.name)
        #publishing cmd_vel
        self.cmd_vel_pub.publish(cmd_vel)
        
        
            
    def normalization_angle(self,theta):
        #Normalize angle to be between 180 &-180
        normalized_theta = theta % (2 * math.pi)
        if normalized_theta > math.pi:
            normalized_theta -= 2 * math.pi
        return normalized_theta
    
    def killer(self,turtle_name):
        while not self.killer_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Waiting for /kill service...')
        request=Kill.Request()
        request.name=turtle_name
        future=self.killer_client.call_async(request)
        response=future.result()
        self.get_logger().info(f'{turtle_name} has been killed')
        
        

def main():
    rclpy.init()
    node=My_turtle()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=='__main__':
    main()