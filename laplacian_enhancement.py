from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import cv2

# 打开图像文件
dataset = gdal.Open(r'E:\HY-1C_NorthPole\W-E\research_area\second_try\sub_original_region\band2\123901_band2', gdal.GA_ReadOnly)

# 读取图像数据
band = dataset.GetRasterBand(1)
band_array = band.ReadAsArray()

# 定义拉普拉斯卷积核
laplacian_kernel = np.array([[1, 1, 1],
                            [1, -8, 1],
                            [1, 1, 1]])

# 使用卷积进行拉普拉斯滤波
laplacian_filtered = cv2.filter2D(band_array, -1, laplacian_kernel)

# 生成拉普拉斯增强图像
laplacian_sharpened = band_array - laplacian_filtered

# # 存储拉普拉斯滤波图像
driver = gdal.GetDriverByName('GTiff')
output_file1 = r'E:\HY-1C_NorthPole\W-E\research_area\second_try\sub_original_region\band2\laplacian\123901_filtered'  # 替换为第一个输出文件的路径和文件名
output_dataset1 = driver.Create(output_file1, band.XSize, band.YSize, 1, gdal.GDT_Float32)
output_dataset1.SetGeoTransform(dataset.GetGeoTransform())
output_dataset1.SetProjection(dataset.GetProjection())
output_dataset1.GetRasterBand(1).WriteArray(laplacian_filtered)
output_dataset1 = None
#
# # 存储拉普拉斯增强图像
output_file2 = r'E:\HY-1C_NorthPole\W-E\research_area\second_try\sub_original_region\band2\laplacian\123901_sharpened'  # 替换为第二个输出文件的路径和文件名
output_dataset2 = driver.Create(output_file2, band.XSize, band.YSize, 1, gdal.GDT_Float32)
output_dataset2.SetGeoTransform(dataset.GetGeoTransform())
output_dataset2.SetProjection(dataset.GetProjection())
output_dataset2.GetRasterBand(1).WriteArray(laplacian_sharpened)
output_dataset2 = None

plt.subplot(1, 3, 1)
plt.imshow(band_array, cmap='gray')
plt.title('Original Image')
plt.axis('off')

#显示拉普拉斯滤波图像
plt.subplot(1, 3, 2)
plt.imshow(laplacian_filtered, cmap='gray')
plt.title('Laplacian Filtered Image')
plt.axis('off')

#显示拉普拉斯增强图像
plt.subplot(1, 3, 3)
plt.imshow(laplacian_sharpened, cmap='gray')
plt.title('Laplacian Sharpened Image')
plt.axis('off')

#调整子图之间的间距
plt.tight_layout()

#显示图像
plt.show()
# 关闭数据集
dataset = None