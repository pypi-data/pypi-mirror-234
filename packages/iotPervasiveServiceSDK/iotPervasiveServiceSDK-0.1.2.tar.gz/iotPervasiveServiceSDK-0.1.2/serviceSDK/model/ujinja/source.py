import re
class TemplateEngine:
  FOR = "for"
  ENDFOR = "endfor"
  IF = "if"
  ENDIF = "endif"
  delimiterList=["==", ">=", "<=","!=",">","<","or", "and", "!"]
  delimiters = "("+"|".join(delimiterList)+")"

  def __init__(self):
      pass

  # 定义一个加载模板的方法，从文件中读取模板内容，并存入字典
  def load_template(self, strTemplates):
      self.template = strTemplates;

  # 渲染模板的方法
  # 输入 变量字典
  # 返回 渲染后的字符串
  def render_template(self, data: dict)->str:
    result = self.template
    # 获取标签位置
    start_index = self.findStartTag(result)
    print(start_index)

    while start_index != -1:
      # 获取tag类型
      start_last_tag = result[start_index:start_index+2]
      if(start_last_tag == "{{"):
        # 变量替换
        end_index = result.find('}}', start_index)
        key = result[start_index + 2:end_index].strip()
        #根据key获取value
        value = self.get_value(key,data)
        #拼接
        result = result[:start_index] + str(value) + result[end_index + 2:]
      # 对if或者for进行处理
      elif(start_last_tag == "{%"):
        end_index = result.find('%}', start_index)
        tagbody = result[start_index+2:end_index]
        tagFragment = tagbody.split(" ")
        while '' in tagFragment:
          tagFragment.remove('')
        type = tagFragment[0]
        # 处理if
        if(type==self.IF):
          # endTag = "{% endif %}"
          # try:
          #   endTag=re.compile(r"{%\s*endif\s*%}").search(result).group(0)
          # except:
          #   raise Exception('Missing end tag in '+ tagbody)
          # endTagIndex=result.find(endTag)
          endTagIndex,endTag = self.findEndTag(result[start_index:],self.IF)
          endTagIndex = endTagIndex+start_index
          #得到条件
          tagFragment[0]=""
          condition = "".join(tagFragment)
          print(condition)
          exeConditionRes=self.conditionalExecution(data,condition)
          print(exeConditionRes)
          #判断结果
          if(exeConditionRes):
            # 先删除end标签保证start标签起始坐标不变
            result = result[:endTagIndex] + result[endTagIndex + len(endTag):]
            result = result[:start_index] + result[end_index + 2:]
          else:
            result = result[:start_index] + result[endTagIndex + len(endTag):]
        # 处理for
        elif(type==self.FOR):
          # 定位end标签的位置
          # endTag = "{% endfor %}"
          # try:
          #   endTag=re.compile(r"{%\s*endfor\s*%}").search(result).group(0)
          # except:
          #   raise Exception('Missing end tag in '+ tagbody)
          # endTagIndex=result.find(endTag)
          endTagIndex,endTag = self.findEndTag(result[start_index:],self.FOR)
          endTagIndex = endTagIndex+start_index
          tagFragment[0]=""
          # 获取被循环的字典值
          value = self.get_value(tagFragment[-1],data)
          print(value)
          resBody = ""
          for item in value:
            t = TemplateEngine()
            forBody = result[end_index+2:endTagIndex]
            t.load_template(forBody)
            data[tagFragment[1]] = item
            res = t.render_template(data)
            resBody = resBody + res
            data.pop(tagFragment[1])
          result = result[:start_index] + resBody + result[endTagIndex + len(endTag):]

      start_index = self.findStartTag(result)
      print("====")
    return result

# 找到开始标签的位置
  def findStartTag(self,msg:str):
    valueTagIndex = msg.find('{{')
    logicTagIndex = msg.find('{%')
    if(valueTagIndex == -1 and logicTagIndex == -1):
      return -1
    elif(valueTagIndex == -1):
      return logicTagIndex
    elif(logicTagIndex == -1):
      return valueTagIndex
    else:
      return  valueTagIndex < logicTagIndex and valueTagIndex or logicTagIndex

# 找到结束标签的位置
  def findEndTag(self,body:str,type):
    level = 1
    position = -1
    tag = ""
    startTagRe = ""
    endTagRe = ""
    if(type == self.IF):
      startTagRe = "{%\s*if.*%}"
      endTagRe = "{%\s*endif\s*%}"
    elif(type == self.FOR):
      startTagRe = "{%\s*for.*%}"
      endTagRe = "{%\s*endfor\s*%}"
    # 初始化开始标签
    startTag = re.compile(startTagRe).search(body).group(0)
    startTagIndex = body.find(startTag)
    body = body[startTagIndex+len(startTag):]
    position = startTagIndex+len(startTag)
    while(level>0):
      # 判断最近的Tag是开始标签还是结束标签
      try:
        startTag = re.compile(startTagRe).search(body).group(0)
        startTagIndex = body.find(startTag)
      except:
        startTagIndex = -1
      try:
        endTag = re.compile(endTagRe).search(body).group(0)
        endTagIndex = body.find(endTag)
      except:
        endTagIndex = -1
      if(endTagIndex ==-1):
        # 错误，没有结束标签
        return -1,-1
      # 如果开始标签不存在，结束标签存在或结束标签在开始标签之前  leve-1 并记录结束标签的位置和tag 
      elif(startTagIndex==-1 or endTagIndex < startTagIndex):
        level = level-1
        tag = endTag
        catPosition = endTagIndex+len(endTag)
        position = position + catPosition
        body = body[catPosition:]
        if(level==0):
          position = position - len(endTag)
          break
      elif(startTagIndex<endTagIndex):
        level = level+1
        catPosition = startTagIndex+len(startTag)
        position = position + catPosition
        body = body[startTagIndex+len(startTag):]
    
    return position,tag
      
        
      

  # 判断条件表达式
  def conditionalExecution(self,data: dict,condition:str):
    #替换变量
    ## 截取字符串
    conditionList = re.split(self.delimiters, condition)
    ## 替换变量值
    for i in range(len(conditionList)):
      if(conditionList[i].find("'")==-1 and conditionList[i].find('"')):
        try:
          value=self.get_str_value(conditionList[i],data)
          conditionList[i] = value
        except:
          pass
    exeCondition=" ".join(conditionList)
    print(exeCondition)
    return eval(exeCondition)


# 获取字符串结果
  def get_str_value(self,key: str,data: dict):
    value = self.getRealValue(key,data)
    if isinstance (value,str):
      value = "'"+value+"'" 
    elif(not isinstance(value,dict)):
      value = str(value)
    
    return value 

# 获取字典中的值
  def get_value(self,key: str,data: dict):
    value = self.getRealValue(key,data)
    if isinstance (value,bool):
        value = str(value).lower()
    return value

# 获取真实值
  def getRealValue(self,key: str,data: dict):
    keys = key.split('.')
    value = data
    for k in keys:
      start = k.find("[")
      # 如果是数组
      if(start!=-1):
        end = k.find("]")
        try:
          sp =k[start+1:end]
        except:
          raise Exception('ERROR Array indices have no end flags')
        try:
          index=int(sp)
        except:
          raise Exception('ERROR Array indices are not numbers')
        try:
          value = value[k[:start]][index]
        except:
          raise Exception('ERROR Array index out of bounds')
      # 不是数组
      else:
        try:
          value = value[k]
        except:
          raise Exception('ERROR Variable does not exist')
    return value
      
      

