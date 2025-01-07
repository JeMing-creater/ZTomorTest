import os
import cv2
import nibabel as nib

def check_subdirectories_contain_files(main_directory, subdirectory_names, checkModels):
    
    empty_dirs = []
    entries = os.listdir(main_directory)
    # 判断要检查的模态是否全部包含在目录中
    for model in checkModels:
        if model not in entries:
            empty_dirs.append(model)
            
    for subdir_name in subdirectory_names:
        if subdir_name not in checkModels:
            continue
        else:
            subdir_path = os.path.join(main_directory, subdir_name)
            if not os.path.isdir(subdir_path):
                # 如果不是有效的目录，则添加到空目录列表并继续下一个
                empty_dirs.append(subdir_name)
                continue
            
            # 获取子目录中的所有条目，并过滤出文件
            files_in_subdir = [f for f in os.listdir(subdir_path) 
                            if os.path.isfile(os.path.join(subdir_path, f))]
            
            if not files_in_subdir:
                empty_dirs.append(subdir_name)
    
    
    # 如果empty_dirs为空，说明所有子目录都包含文件
    return (not empty_dirs, empty_dirs)

def check_slices_consistency(main_directory, checkModels):
    slice_counts = {}
    inconsistent_modalities = {}

    # 遍历所有模态子目录
    for modality in checkModels:
        modality_dir = os.path.join(main_directory, modality)
        if not os.path.isdir(modality_dir):
            print(f"警告：未找到 {modality} 模态的子目录")
            continue
        
        nii_files = [f for f in os.listdir(modality_dir) if f.endswith('.nii.gz')]
        if not nii_files:
            print(f"警告：{modality} 模态子目录下没有 .nii.gz 文件")
            continue
        
        # 假设每个模态只有一个 .nii.gz 文件，如果有多个，请根据需要调整逻辑
        nii_file_path = os.path.join(modality_dir, nii_files[0])
        
        # 加载.nii.gz文件并获取2D切片数量
        img = nib.load(nii_file_path)
        slices = img.shape[2] if len(img.shape) >= 3 else None  # 假设第三维为切片维度
        
        if slices is None:
            print(f"警告：无法确定 {modality} 模态文件的2D切片数量")
            continue
        
        slice_counts[modality] = slices
    
    # 检查所有模态的2D切片数量是否一致
    reference_slices = next(iter(slice_counts.values()), None) if slice_counts else None
    for modality, slices in slice_counts.items():
        if slices != reference_slices:
            inconsistent_modalities[modality] = slices
    
    return (not bool(inconsistent_modalities), inconsistent_modalities)