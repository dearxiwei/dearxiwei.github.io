import yaml
import os

def main():
    # 定义文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'config.yaml')
    new_config_path = os.path.join(current_dir, 'newconfig.yaml')
    
    # 读取原始配置文件
    with open(config_path, 'r', encoding='utf-8') as file:
        config_data = yaml.safe_load(file)
    
    if 'rules' not in config_data:
        print("配置文件中未找到rules规则")
        return
    
    # 原始规则数据
    original_rules = config_data['rules']
    original_count = len(original_rules)
    print(f"初始规则总数: {original_count}条")
    
    # 去重处理（保持顺序）
    unique_rules = []
    seen_rules = set()
    removed_count = 0
    
    print("\n去重处理过程:")
    for index, rule in enumerate(original_rules, 1):
        if rule in seen_rules:
            print(f"第{index}条规则已重复: {rule}")
            removed_count += 1
        else:
            unique_rules.append(rule)
            seen_rules.add(rule)
    
    # 更新配置数据
    config_data['rules'] = unique_rules
    
    # 保存新配置文件
    with open(new_config_path, 'w', encoding='utf-8') as file:
        yaml.dump(config_data, file, allow_unicode=True, sort_keys=False)
    
    # 输出统计信息
    print("\n处理结果:")
    print(f"━━ 原始规则总数: {original_count}条")
    print(f"━━ 重复规则数量: {removed_count}条")
    print(f"━━ 去重后剩余规则: {len(unique_rules)}条")
    print(f"新配置文件保存至: {os.path.abspath(new_config_path)}")

if __name__ == "__main__":
    main()
