import cv2
import math
import matplotlib.pyplot as plt
from pyzbar.pyzbar import decode

class QRlocator:
    def __init__(self, image_path, focal_ratio, x_focal_angle_scalar, z_focal_angle_scalar):
        self.image_path = None
        self.image = None
        self.x_img_center = None
        self.y_img_center = None
        self.modify_image_path(image_path)
        
        self.focal_ratio = focal_ratio
        self.x_focal_angle_scalar = x_focal_angle_scalar
        self.z_focal_angle_scalar = z_focal_angle_scalar

        self.qr_codes = {}
        
    def scan_image(self):
        decoded_objects = decode(self.image)
        for qr_code in decoded_objects:
            points = qr_code.polygon
            if len(points) > 2:
                self.add_qr_code(qr_code.data.decode('utf-8'), points[0], points[1], points[2], points[3])
    
    def modify_image(self, image):
        if image is not None:
            self.image = image
            self.x_img_center = self.image.shape[1] / 2
            self.y_img_center = self.image.shape[0] / 2

    def modify_image_path(self, image_path):
        if image_path is not None:
            self.image_path = image_path
            image = cv2.imread(self.image_path)
            self.modify_image(image)

    def add_qr_code(self, data, tl, tr, br, bl):
        self.qr_codes[data] = [tl, tr, br, bl]

    def get_qr_codes(self):
        return self.qr_codes

    def get_qr_code(self, data):
        try:
            return self.qr_codes[data]
        except KeyError:
            return None
        
    def get_max_side_length(self, data):
        points = self.get_qr_code(data)
        #in this case norm\/ gets the distance between two points
        return max([cv2.norm(points[0], points[1]), 
                    cv2.norm(points[1], points[2]), 
                    cv2.norm(points[2], points[3]), 
                    cv2.norm(points[3], points[0])])
        
    def distance_from_camera_in_inches(self, data, qr_code_side_length_mm):
        distance_mm = (qr_code_side_length_mm * (self.focal_ratio * self.image.shape[1])) / self.get_max_side_length(data)
        return distance_mm / 25.4
    
    def get_y_position(self, data, qr_code_side_length_mm):
        return self.distance_from_camera_in_inches(data, qr_code_side_length_mm)
    
    def get_x_position(self, data, qr_code_side_length_mm):
        distance_inches = self.get_y_position(data, qr_code_side_length_mm)
        points = self.get_qr_code(data)
        delta_x = sum([point[0] for point in points]) / len(points) - self.x_img_center
        x_angle = math.degrees(math.atan(delta_x / self.image.shape[1]))
        return math.tan(math.radians(x_angle)) * distance_inches * self.x_focal_angle_scalar

    def get_z_position(self, data, qr_code_side_length_mm):
        distance_inches = self.get_y_position(data, qr_code_side_length_mm)
        points = self.get_qr_code(data)
        delta_z = sum([point[1] for point in points]) / len(points) - self.y_img_center
        z_angle = -math.degrees(math.atan(delta_z / self.image.shape[1]))
        return math.tan(math.radians(z_angle)) * distance_inches * self.z_focal_angle_scalar
    
    def show_visualization(self, qr_code_side_length_mm, qr_codes = None):
        if qr_codes is None:
            qr_codes = self.qr_codes

        fig, axs = plt.subplots(1, 2, figsize=(20, 10))

        axs[0].axhline(0, color='k')
        axs[0].scatter(0, 0, c='r', label='Camera')
        for data, qr_code in qr_codes.items():
            x = self.get_x_position(data, qr_code_side_length_mm) / 12
            y = self.get_y_position(data, qr_code_side_length_mm) / 12
            axs[0].scatter(x, y, label=f"QR Code: {data}")
            axs[0].annotate(data, (x, y), textcoords="offset points", xytext=(0, -10), ha='center')
        axs[0].set_xlabel('X (feet)')
        axs[0].set_ylabel('Y (feet)')
        axs[0].legend(loc='lower left')
        axs[0].axis('equal')
        axs[0].set_title('QR Code Location in XY Plane')

        for data, qr_code in qr_codes.items():
            x = self.get_x_position(data, qr_code_side_length_mm) / 12
            z = self.get_z_position(data, qr_code_side_length_mm) / 12
            axs[1].scatter(x, z, label=f"QR Code: {data}")
            axs[1].annotate(data, (x, z), textcoords="offset points", xytext=(0, -10), ha='center')
        axs[1].set_xlabel('X (feet)')
        axs[1].set_ylabel('Z (feet)')
        axs[1].legend(loc='lower left')
        axs[1].axis('equal')
        axs[1].set_title('QR Code Location in XZ Plane')

        plt.tight_layout()
        plt.show()












