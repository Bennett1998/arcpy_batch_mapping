# coding:utf-8
# Arcpy batch mapping library, version 1.0.0 beta
# python 2.7.3
# arcgis 10.2
# Author: Li Qiang
# email: liqiang@cug.edu.cn
# Last edited: 13:40 24th Dec, 2020
# copyright @Li Qiang

import os
import arcpy
import csv


class ArcpyPlot():
    def __init__(self, env_path, mxd_path, shape_path, data_path, rewrite_field_name, id_field_name):
        self.rewrite_field_name = rewrite_field_name
        self.id_field_name = id_field_name
        self.data_path = data_path
        self.mxd_path = mxd_path
        self.env_path = env_path
        self.shape_path = shape_path

        # 设置工作空间
        arcpy.env.workspace = self.env_path
        # 读取mxd
        self.mxd = arcpy.mapping.MapDocument(self.mxd_path)
        # 读取数据框
        self.df = arcpy.mapping.ListDataFrames(self.mxd, r"Layers")[0]
        # 读取每一个图层
        self.layers = arcpy.mapping.ListLayers(self.mxd, "", self.df)
        # 读取地图文字要素
        self.ELM = arcpy.mapping.ListLayoutElements(self.mxd, "TEXT_ELEMENT")

    def data_load(self):
        data_dict = {}
        with open(self.data_path, 'r') as f:
            reader = csv.reader(f)
            head = next(reader)
            for i in reader:
                data_dict[str(int(i[0]))] = i[1]
        self.data = data_dict

    def rewrite_attribute_table(self):
        self.data_load()
        cusor = arcpy.UpdateCursor(self.shape_path)
        for my_row in cusor:
            id = my_row.getValue(self.id_field_name)
            id = str(int(id))
            if id in self.data.keys():
                new_value = self.data[id]
            else:
                new_value = 0
            my_row.setValue(self.rewrite_field_name, new_value)
            cusor.updateRow(my_row)

    def rewrite_map_text(self, text_dict={}, is_test=False):
        # 可使用本方法对地图中的文字部分进行测试
        if is_test:
            # 测试地图文件中各个文字部分的名字和内容
            print("Test the order of text in this mxd file....")
            for i in range(len(self.ELM)):
                print(self.ELM[i].name, self.ELM[i].text)
        else:
            # 修改地图文件中特定文字部分的名字和内容
            for elm in self.ELM:
                if elm.name in text_dict.keys():
                    elm.text = text_dict[elm.name]

    def rewrite_layers(self, rewrite_layer_name, new_layer_path):
        for layer in self.layers:
            if layer.name == rewrite_layer_name:
                source_layer = layer

                # 可以删去这个图层或者将其不可视
                # layer.visible=False
                arcpy.mapping.RemoveLayer(self.df, layer)

        # 插入图层
        new_layer = arcpy.mapping.Layer(new_layer_path)
        arcpy.mapping.AddLayer(self.df, new_layer, "TOP")

        # 使用原图层将新图层符号化
        new_layer = arcpy.mapping.ListLayers(self.mxd, "", self.df)[0][0]
        arcpy.mapping.UpdateLayer(self.df, new_layer, source_layer, True)

        # 刷新视图
        arcpy.RefreshActiveView()

    def drawing_map(self, save_path, resolution=100):
        try:
            arcpy.mapping.ExportToJPEG(self.mxd, save_path, resolution=resolution)

            print(save_path + "  Successfully!**********")
        except Exception as e:
            print(save_path + "  failed!!!!!!!!!!!!!!!!!")
            print(e)

    def pipeline(self, text_dict, save_path):
        # 修改属性表的绘图字段内容
        self.rewrite_attribute_table()
        # 修改地图的文本
        self.rewrite_map_text(text_dict)
        # 绘图
        self.drawing_map(save_path)


def main():
    
    # # 将要修改的shape文件的属性表的字段名
    # rewrite_field_name =

    # # 将要修改的shape文件的与新数据进行匹配的字段名：id字段名
    # id_field_name =

    # # 新数据文件的路径：为csv格式，第一列为匹配的id字段，第二列为数据
    # data_path =

    # # .mxd文件的路径
    # mxd_path =

    # # shape等mxd工程文件的源文件路径
    # env_path =

    # # 所要修改的shape文件的路径
    # shape_path =

    # # 输出地图的保存路径
    # save_path =

    # # 地图模板中进行替换的文字，为字典
    # text_dict =

    # arcpy_plot = ArcpyPlot(env_path, mxd_path, shape_path, data_path, rewrite_field_name, id_field_name)
    # arcpy_plot.pipeline()
    pass


if __name__ == '__main__':
    main()
