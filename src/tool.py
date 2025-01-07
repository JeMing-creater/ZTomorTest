import os

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"目录 {directory} 已创建。")
    else:
        print(f"目录 {directory} 已存在。")

def get_directory_item(path):
    try:
        # 获取指定路径下的所有条目
        entries = os.listdir(path)
        return entries
    except FileNotFoundError:
        print(f"The provided path {path} does not exist.")
        return []

def write_result(path, result):
    directory = os.path.dirname(path)
    ensure_directory_exists(directory)
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w') as f:
        pass  
    
    cannot_open, loss_model, unalign_model, unResolution_model, use_model = result
    
    result_line = []
    with open(path, 'w') as f:
        # 1. 写入可用数据编号
        result = ''
        for item in use_model:
            result += item + ', '
        result_line.append('Useful data: ' + result.rstrip(', ') + '\n')
        result_line.append('\n')
        
        # 2. 无法打开的文件（文件损坏）
        result_line.append('Unable data: '+ '\n')
        for key in cannot_open.keys():
            result = ''
            data = cannot_open[key]
            for item in data:
                result += item + ', '
            result = result.rstrip(', ')
            result_line.append(f'{key}: {result} \n')
        result_line.append('\n')
        
        # 2. 写入缺失模态的编号
        result_line.append('Loss models data: '+ '\n')
        for key in loss_model.keys():
            result = ''
            data = loss_model[key]
            for item in data:
                result += item + ', '
            result = result.rstrip(', ')
            result_line.append(f'{key}: {result} \n')
        result_line.append('\n')  
        
        # 3. 写入不对齐模态的编号
        result_line.append('Unalign data: '+ '\n')
        for key in unalign_model.keys():
            result = ''
            data = unalign_model[key]
            for key2 in data.keys():
                result += f'{key2} : {data[key2]}' + ', '
            result = result.rstrip(', ')
            result_line.append(f'{key}: {result} \n')    
        result_line.append('\n') 
        
        # 4. 写入分辨率不足模态的编号
        result_line.append('unResolution data: '+ '\n')
        for key in unResolution_model.keys():
            result = ''
            data = unResolution_model[key]
            for key2 in data.keys():
                result += f'{key2} : {data[key2]}' + ', '
            result = result.rstrip(', ')
            result_line.append(f'{key}: {result} \n')    
        result_line.append('\n') 

        for line in result_line:
            f.write(line)