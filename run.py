# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import RSfusion
import RS_images_utils
import util


def main(argv):
    print('-------------start-------------')
    argc = len(argv)
    print(argv)
    if argc != 3:
        print('ERROR: 参数个数不对！')
        return
    data_path = argv[1]
    sensor_num = argv[2]
    result_folder = argv[3]
    print('影像路径：%s'%(data_path))
    print('结果文件夹：%s'%(result_folder))
    product_id = os.path.basename(data_path).split('_')[5][6:13]
    print('影像产品号：%s'%(product_id))



    print('-------------解压文件-------------')
    decompression_folder = '/storage/sample/raster'
    tar_step = "tar -zxvf {} -C {}".format(data_path,decompression_folder)
    if subprocess.call(tar_step, shell=True) != 0:
        err_message = '解压数据失败！'
        print(err_message)
        return
    MSS_path = decompression_folder + '/' + os.path.basename(data_path).replace('.tar.gz','-MSS{}.tiff'.format(sensor_num))
    PAN_path = decompression_folder + '/' +os.path.basename(data_path).replace('.tar.gz','-PAN{}.tiff'.format(sensor_num))
    MSS_path_w = decompression_folder + '/' + product_id + '-MSS{}.tiff'.format(sensor_num)
    PAN_path_w = decompression_folder + '/' + product_id + '-PAN{}.tiff'.format(sensor_num)
    print('-------------赋投影-------------')
    warp_step = "gdalwarp {} {} -s_srs EPSG:4326 -t_srs EPSG:4326".format(MSS_path, MSS_path_w)
    if subprocess.call(warp_step, shell=True) != 0:
        err_message = '多光谱数据赋投影失败！'
        print(err_message)
        return

    warp_step = "gdalwarp {} {} -s_srs EPSG:4326 -t_srs EPSG:4326".format(PAN_path, PAN_path_w)
    if subprocess.call(warp_step, shell=True) != 0:
        err_message = '全色数据赋投影失败！'
        print(err_message)
        return
    print('-------------数据融合-------------')
    fusion_result = decompression_folder + '/' + product_id + '.tiff'
    fusion_step = "python3 RSfusion.py {} {} {} {} {}".format(PAN_path_w, MSS_path_w + ',band=1', MSS_path_w + ',band=2', MSS_path_w + ',band=3',fusion_result)
    if subprocess.call(fusion_step, shell=True) != 0:
        err_message = '数据融合失败！'
        print(err_message)
        return
    print('-------------四分掩膜生成-------------')
    util.Create4VectorFileByRasterExtent(fusion_result)
    print('-------------裁剪影像（四分）-------------')
    shp1 = decompression_folder + '/' + product_id + '-1.shp'
    shp2 = decompression_folder + '/' + product_id + '-2.shp'
    shp3 = decompression_folder + '/' + product_id + '-3.shp'
    shp4 = decompression_folder + '/' + product_id + '-4.shp'

    tiff1 = decompression_folder + '/' + product_id + '-1.tiff'
    tiff2 = decompression_folder + '/' + product_id + '-2.tiff'
    tiff3 = decompression_folder + '/' + product_id + '-3.tiff'
    tiff4 = decompression_folder + '/' + product_id + '-4.tiff'
    mosic_step = "gdalwarp -ot Float32 -of GTiff  -tr 8.015972433164791e-06 -8.015972433164747e-06 -tap -cutline {} -crop_to_cutline {} {}".format(shp1,fusion_result,tiff1)
    if subprocess.call(mosic_step, shell=True) != 0:
        err_message = '四分-1裁剪失败！'
        print(err_message)
        return
    mosic_step = "gdalwarp -ot Float32 -of GTiff  -tr 8.015972433164791e-06 -8.015972433164747e-06 -tap -cutline {} -crop_to_cutline {} {}".format(shp2,fusion_result,tiff2)
    if subprocess.call(mosic_step, shell=True) != 0:
        err_message = '四分-2裁剪失败！'
        print(err_message)
        return
    mosic_step = "gdalwarp -ot Float32 -of GTiff  -tr 8.015972433164791e-06 -8.015972433164747e-06 -tap -cutline {} -crop_to_cutline {} {}".format(shp3,fusion_result,tiff3)
    if subprocess.call(mosic_step, shell=True) != 0:
        err_message = '四分-3裁剪失败！'
        print(err_message)
        return
    mosic_step = "gdalwarp -ot Float32 -of GTiff  -tr 8.015972433164791e-06 -8.015972433164747e-06 -tap -cutline {} -crop_to_cutline {} {}".format(shp4,fusion_result,tiff4)
    if subprocess.call(mosic_step, shell=True) != 0:
        err_message = '四分-4裁剪失败！'
        print(err_message)
        return
    print('-------------生成自然图像-------------')
    jpg_folder = result_folder
    jpg1 = jpg_folder + '/' + product_id + '-1.jpg'
    jpg2 = jpg_folder + '/' + product_id + '-2.jpg'
    jpg3 = jpg_folder + '/' + product_id + '-3.jpg'
    jpg4 = jpg_folder + '/' + product_id + '-4.jpg'

    RS_images_utils.save_tiff_png(tiff1,jpg1)
    RS_images_utils.save_tiff_png(tiff2,jpg2)
    RS_images_utils.save_tiff_png(tiff3,jpg3)
    RS_images_utils.save_tiff_png(tiff4,jpg4)
    print('------------NB--------------------')




if __name__ == "__main__":
    sys.exit(main(sys.argv))