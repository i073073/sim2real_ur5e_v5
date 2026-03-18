# ur5e_sim2real/src/tcp_trail_renderer.py
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
import tf2_ros

class TcpTrailRenderer(Node):
    def __init__(self):
        super().__init__('tcp_trail_renderer')
        self.marker_publisher = self.create_publisher(MarkerArray, '/tcp_trail_markers', 10)
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(0.1, self.publish_trail) # 10Hz update rate
        self.trail_points = []
        self.max_trail_length = 100 # 최대 100개 포인트 저장

    def publish_trail(self):
        try:
            # tcp_link의 현재 위치를 world 프레임 기준으로 얻어옴
            transform = self.tf_buffer.lookup_transform('world', 'tcp_link', rclpy.time.Time())
            current_point = Point()
            current_point.x = transform.transform.translation.x
            current_point.y = transform.transform.translation.y
            current_point.z = transform.transform.translation.z

            # 트레일 목록에 추가 (최대 길이 유지)
            self.trail_points.append(current_point)
            if len(self.trail_points) > self.max_trail_length:
                self.trail_points.pop(0)

            # MarkerArray 메시지 생성
            marker_array = MarkerArray()
            marker = Marker()
            marker.header.frame_id = 'world'
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = 'tcp_trail'
            marker.id = 0
            marker.type = Marker.POINTS # 포인트 타입 마커
            marker.action = Marker.ADD
            marker.scale.x = 0.01 # 포인트 크기 (1cm)
            marker.scale.y = 0.01
            marker.color.a = 1.0 # 투명도
            marker.color.r = 0.0
            marker.color.g = 1.0
            marker.color.b = 0.0
            marker.points = self.trail_points

            marker_array.markers.append(marker)
            self.marker_publisher.publish(marker_array)

        except tf2_ros.TransformException as ex:
            self.get_logger().warn(f'Could not transform from world to tcp_link: {ex}')

def main(args=None):
    rclpy.init(args=args)
    tcp_trail_renderer = TcpTrailRenderer()
    rclpy.spin(tcp_trail_renderer)
    tcp_trail_renderer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()