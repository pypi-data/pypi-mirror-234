'''
* 模板转换
* input: template:模板的字符串   data:替换内容的字典
* output：拼接好的模板
* 
'''
def templateConversion(template: str, data: dict) -> str:
    # 获取字典中的值
    def get_value(key: str):
        keys = key.split('.')
        value = data
        for k in keys:
            value = value[k]
        if isinstance (value,bool):
            value = str(value).lower()
        return value

    result = template
    # 获取标签位置
    start_index = result.find('{{')
    while start_index != -1:
        end_index = result.find('}}', start_index)
        #获取到key
        key = result[start_index + 2:end_index].strip()
        #根据key获取value
        value = get_value(key)
        #拼接
        result = result[:start_index] + str(value) + result[end_index + 2:]
        #获取下一个标签位置
        start_index = result.find('{{')
    return result