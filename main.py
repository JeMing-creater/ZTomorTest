from easydict import EasyDict
import SimpleITK as sitk
from src.tool import *
from src.check import *
import os, cv2, yaml


# TODO: 确定分辨率是否合理，合理返回True, 不合理返回False

def main(config):
  # 检查的模态
  checkModels = config.checkModels
  
  # 非手术勾画
  dataPath = config.dataPath1
  directory_item = get_directory_item(dataPath)
  
  # TODO: 确定哪个编号空缺模态，如皆不空缺，返回True, 否则返回空缺模态列表
  loss_model = {}
  # TODO: 确定同编号下，不同模态切片数量是否对齐，如皆对齐返回True, 如不对齐返回各个模态切片数量的字典
  unalign_model = {}
  # TODO: 确定分辨率是否合理，合理返回True, 不合理返回False
  
  if directory_item != []:
    for item in directory_item:
      this_data_path = dataPath + '/' + item + '/'
      all_models = get_directory_item(this_data_path)
      # TODO: 确定哪个编号空缺模态，如皆不空缺，返回True, 否则返回空缺模态列表
      check_flag, loss_item = check_subdirectories_contain_files(this_data_path, all_models, checkModels)
      if check_flag == False:
        loss_model[item] = loss_item
      else:
        # 如果模态缺失，则无所谓对齐，如果不缺失，则考虑对齐
        # TODO: 确定同编号下，不同模态切片数量是否对齐，如皆对齐返回True, 如不对齐返回各个模态切片数量的字典
        check_flag, unalign_item = check_slices_consistency(this_data_path, checkModels)
        if check_flag == False:
          unalign_model[item] = unalign_item
  else:
    print('dataPath has not data!')
  
  print(loss_model)
  print(unalign_model)
  # 手术勾画

if __name__ == '__main__':
  config = EasyDict(yaml.load(open('config.yml', 'r', encoding="utf-8"), Loader=yaml.FullLoader))
  main(config)
    