import os
import pyzipper  # 使用 pyzipper 替代 zipfile

input_dir = os.path.join(os.path.dirname(__file__), 'input')
output_dir = os.path.join(os.path.dirname(__file__), 'output')

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    
    if os.path.isfile(file_path):
        zip_path = os.path.join(output_dir, f"{filename}.zip")
        
        # 使用 pyzipper 创建加密 ZIP 文件
        with pyzipper.AESZipFile(zip_path, 'w', 
                               compression=pyzipper.ZIP_DEFLATED,
                               encryption=pyzipper.WZ_AES) as zf:  # 启用 AES 加密
            zf.setpassword(b'1111')  # 设置密码
            zf.write(file_path, arcname=filename)
        print(f"处理中:  {filename}\t 压缩完成")
print(f"共 {len(os.listdir(input_dir))} 个文件全部压缩完成!!!")
