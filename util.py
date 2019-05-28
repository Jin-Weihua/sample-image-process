#-*- coding: utf-8 -*-
try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
    import rasterio
    import os
except ImportError:
    import gdal
    import ogr
    import osr


def WriteVectorFile(filename, wkt):
         # 为了支持中文路径，请添加下面这句代码
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
         # 为了使属性表字段支持中文，请添加下面这句
        gdal.SetConfigOption("SHAPE_ENCODING","")
 
        strVectorFile = filename
 
         # 注册所有的驱动
        ogr.RegisterAll()
 
         # 创建数据，这里以创建ESRI的shp文件为例
        strDriverName = "ESRI Shapefile"
        oDriver =ogr.GetDriverByName(strDriverName)
        if oDriver == None:
            print("%s 驱动不可用！\n", strDriverName)
            return
        
         # 创建数据源
        oDS =oDriver.CreateDataSource(strVectorFile)
        if oDS == None:
            print("创建文件【%s】失败！", strVectorFile)
            return
 
         # 创建图层，创建一个多边形图层，这里没有指定空间参考，如果需要的话，需要在这里进行指定
        papszLCO = []
        spatialref = osr.SpatialReference()
        spatialref.ImportFromEPSG(4326)
        oLayer =oDS.CreateLayer("TestPolygon", spatialref, ogr.wkbPolygon, papszLCO)
        if oLayer == None:
            print("图层创建失败！\n")
            return
 
         # 下面创建属性表
         # 先创建一个叫FieldID的整型属性
        oFieldID =ogr.FieldDefn("FieldID", ogr.OFTInteger)
        oLayer.CreateField(oFieldID, 1)
 
         # 再创建一个叫FeatureName的字符型属性，字符长度为50
        #  oFieldName =ogr.FieldDefn("FieldName", ogr.OFTString)
        #  oFieldName.SetWidth(100)
        #  oLayer.CreateField(oFieldName, 1)
 
        oDefn = oLayer.GetLayerDefn()
 
        #  # 创建三角形要素
        #  oFeatureTriangle = ogr.Feature(oDefn)
        #  oFeatureTriangle.SetField(0, 0)
        #  oFeatureTriangle.SetField(1, "三角形")
        #  geomTriangle =ogr.CreateGeometryFromWkt("POLYGON ((0 0,20 0,10 15,0 0))")
        #  oFeatureTriangle.SetGeometry(geomTriangle)
        #  oLayer.CreateFeature(oFeatureTriangle)
 
         # 创建矩形要素
        oFeatureRectangle = ogr.Feature(oDefn)
        oFeatureRectangle.SetField(0, 1)
        #  oFeatureRectangle.SetField(1, "矩形")
        geomRectangle =ogr.CreateGeometryFromWkt(wkt)
        oFeatureRectangle.SetGeometry(geomRectangle)
        oLayer.CreateFeature(oFeatureRectangle)
 
        oDS.Destroy()
        print("数据集创建完成！\n")


def Create4VectorFileByRasterExtent(rasterfilename):
        # 为了支持中文路径，请添加下面这句代码
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
        # 为了使属性表字段支持中文，请添加下面这句
        gdal.SetConfigOption("SHAPE_ENCODING","")

        filename = os.path.basename(rasterfilename).split('.')[0]
        folder = os.path.dirname(rasterfilename)

        dataset = rasterio.open(rasterfilename)
        dx = dataset.bounds[2]-dataset.bounds[0]
        dy = dataset.bounds[3]-dataset.bounds[1]
        ractangle_ld = "POLYGON ((%f %f,%f %f,%f %f,%f %f,%f %f))"%(dataset.bounds[0],dataset.bounds[1],dataset.bounds[0]+dx/2.0+0.01,dataset.bounds[1],
                      dataset.bounds[0]+dx/2.0+0.01,dataset.bounds[1]+dy/2.0+0.01,dataset.bounds[0],dataset.bounds[1]+dy/2.0+0.01,dataset.bounds[0],dataset.bounds[1])
        WriteVectorFile(folder+'/'+filename+'-1.shp',ractangle_ld)

        ractangle_rd = "POLYGON ((%f %f,%f %f,%f %f,%f %f,%f %f))"%(dataset.bounds[0]+dx/2.0-0.01,dataset.bounds[1],dataset.bounds[2],dataset.bounds[1],
                      dataset.bounds[2],dataset.bounds[1]+dy/2.0+0.01,dataset.bounds[0]+dx/2.0-0.01,dataset.bounds[1]+dy/2.0+0.01,dataset.bounds[0]+dx/2.0-0.01,dataset.bounds[1])
        WriteVectorFile(folder+'/'+filename+'-2.shp',ractangle_rd)

        ractangle_ru = "POLYGON ((%f %f,%f %f,%f %f,%f %f,%f %f))"%(dataset.bounds[0]+dx/2.0-0.01,dataset.bounds[1]+dy/2.0-0.01,dataset.bounds[2],dataset.bounds[1]+dy/2.0-0.01,
                      dataset.bounds[2],dataset.bounds[3],dataset.bounds[0]+dx/2.0-0.01,dataset.bounds[3],dataset.bounds[0]+dx/2.0-0.01,dataset.bounds[1]+dy/2.0-0.01)
        WriteVectorFile(folder+'/'+filename+'-3.shp',ractangle_ru)

        ractangle_lu = "POLYGON ((%f %f,%f %f,%f %f,%f %f,%f %f))"%(dataset.bounds[0],dataset.bounds[1]+dy/2.0-0.01,dataset.bounds[0]+dx/2.0+0.01,dataset.bounds[1]+dy/2.0-0.01,
                      dataset.bounds[0]+dx/2.0+0.01,dataset.bounds[3],dataset.bounds[0],dataset.bounds[3],dataset.bounds[0],dataset.bounds[1]+dy/2.0-0.01)
        WriteVectorFile(folder+'/'+filename+'-4.shp',ractangle_lu)
       



if __name__ == '__main__':
    Create4VectorFileByRasterExtent('/Users/jinweihua/Downloads/GF2_PMS1_E121.1_N31.7_20180310_L1A0003052510/3052510-PAN1.tiff')