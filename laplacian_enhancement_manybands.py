from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import cv2

# 打开图像文件
dataset = gdal.Open(r'E:\HY-1C_NorthPole\W-E\resize_250\histogram_equalization\band2\123901_equalization.tif', gdal.GA_ReadOnly)

# 定义拉普拉斯卷积核
laplacian_kernel = np.array([[1, 1, 1],
                             [1, -8, 1],
                             [1, 1, 1]])

# 初始化滤波和锐化后的波段列表
filtered_bands = []
sharpened_bands = []

# 遍历每个波段
for b in range(dataset.RasterCount):
    band = dataset.GetRasterBand(b + 1)
    band_array = band.ReadAsArray()

    # 使用卷积进行拉普拉斯滤波
    laplacian_filtered = cv2.filter2D(band_array, -1, laplacian_kernel)

    # 生成拉普拉斯增强图像
    laplacian_sharpened = band_array - laplacian_filtered

    # 将滤波和锐化后的波段添加到列表
    filtered_bands.append(laplacian_filtered)
    sharpened_bands.append(laplacian_sharpened)

# 将滤波和锐化后的波段堆叠起来以创建新的4波段图像
filtered_image = np.dstack(filtered_bands)
sharpened_image = np.dstack(sharpened_bands)

# 存储滤波和锐化后的图像
driver = gdal.GetDriverByName('GTiff')
output_file1 = r'E:\HY-1C_NorthPole\W-E\resize_250\histogram_equalization\band2\laplacian\123901_band2_filtered'  # 替换为第一个输出文件的路径和文件名
output_file2 = r'E:\HY-1C_NorthPole\W-E\resize_250\histogram_equalization\band2\laplacian\123901_band2_sharpened'  # 替换为第二个输出文件的路径和文件名

# 创建滤波后的图像文件
output_dataset1 = driver.Create(output_file1, band.XSize, band.YSize, dataset.RasterCount, gdal.GDT_Float32)
output_dataset1.SetGeoTransform(dataset.GetGeoTransform())
output_dataset1.SetProjection(dataset.GetProjection())
for b in range(dataset.RasterCount):
    output_dataset1.GetRasterBand(b + 1).WriteArray(filtered_bands[b])
output_dataset1 = None

# 创建锐化后的图像文件
output_dataset2 = driver.Create(output_file2, band.XSize, band.YSize, dataset.RasterCount, gdal.GDT_Float32)
output_dataset2.SetGeoTransform(dataset.GetGeoTransform())
output_dataset2.SetProjection(dataset.GetProjection())
for b in range(dataset.RasterCount):
    output_dataset2.GetRasterBand(b + 1).WriteArray(sharpened_bands[b])
output_dataset2 = None

# 关闭数据集
dataset = None