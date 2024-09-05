import os
import open3d as o3d
import numpy as np
from PIL import Image
import argparse

# 加载图像目录中的图片，并限制最大图片数量
def load_images_from_folder(folder, max_images=5):
    images = []
    filenames = sorted(os.listdir(folder))  # 按文件名排序

    for filename in filenames:
        if len(images) >= max_images:
            break
        img_path = os.path.join(folder, filename)
        img = Image.open(img_path).convert('RGB')  # 强制转换为RGB格式
        images.append(np.array(img))
    return images


def main(args):
    # 设置图像目录和图片数量限制
    image_folder = args.img_dir_path # 替换为你的图像目录路径
    max_images = args.max_images  # 限制显示的图片数量

    # 加载图像
    images = load_images_from_folder(image_folder, max_images)

    # 将加载的图片顺序倒过来
    images.reverse()  # 或者使用 images = images[::-1]

    # 设置图像数量和间距
    spacing = args.spacing  # 调整这个值来控制图片之间的间距
    point_clouds = []

    for i, image_array in enumerate(images):
        h, w, _ = image_array.shape

        # 创建点云对象
        pcd = o3d.geometry.PointCloud()

        # 生成网格上的点，并翻转Y轴
        x, y = np.meshgrid(np.arange(w), np.arange(h))
        y = h - y  # 通过减去h，将Y轴翻转

        points = np.stack((x, y, np.zeros_like(x)), axis=-1).reshape(-1, 3)

        # 设置点云的点
        pcd.points = o3d.utility.Vector3dVector(points)

        # 设置点云的颜色
        colors = image_array.reshape(-1, 3) / 255.0
        pcd.colors = o3d.utility.Vector3dVector(colors)

        # 将点云移动到Z轴上的指定位置，X轴和Y轴不变
        pcd.translate((0, 0, i * spacing))

        # 添加点云到集合中
        point_clouds.append(pcd)

    # 可视化
    o3d.visualization.draw_geometries(point_clouds, window_name="3D Image Planes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize images to 3D")
    parser.add_argument("--img_dir_path", type=str, required=True,
                        help="Path to the folder containing images.")
    parser.add_argument("--max_images", type=int, default=15,
                        help="Maximum number of images to load.")
    parser.add_argument("--spacing", type=float, default=80.0,
                        help="Spacing between the image planes in the Z-axis.")

    args = parser.parse_args()
    main(args)
