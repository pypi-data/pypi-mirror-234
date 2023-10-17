# This is a sample Python script.
import os
import re
import json
import requests

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

''''
以下是服务提供者，也就是实现方
'''
# oc 格式下匹配类实现的正则表达式
# 只获取匹配到的类名 考虑@implementation 和类名中间可能存在多个空格，考虑@end前可能有空格或者换行符
oc_implementation_regular = r'@implementation\s+(Target_\w+)[\s\S]*?@end'
# 获取匹配到的完整文件， 过滤同理上，只是输出的内容不一样，这个输出匹配到的类的完整实现
oc_full_implementation_regular = r'(@implementation\s+Target_\w+[\s\S]*?@end)'
# oc 格式下匹配方法名称的正则表达式，匹配实现的方法，1. Action前可能有多个空格 2. 只考虑只有一个参数的场景
oc_action_regular = r'\s*[\+-]\s*\([^)]*\)\s*(Action_.*?:)[\s\S]*?{'

''''
以下是调用者
'''
oc_target_action_foldername = 'YHMediator'
# 获取target-action方式的调用者， 这个可以去固定目录下进行文件查找，默认是放在YHMediator组件中
# target-action调用的地方，正则
oc_replace_target_action_regular = r'\*\s*(.*?)\s*=\s*@\"(.*?)\";'
# 考虑特殊的场景，以下场景不计入调用考虑： 前面有//， 方法的声明及实现
oc_target_action_regular = r"^(?!//).*performActionWithTarget:\s*(\S+)\s+action:\s*(\S+)"

# 获取调用方
class FileTool:

    @classmethod
    def findAllFilesWithPath(cls, path: str, prefix: str = 'Target_', suffix: list = ['.m']) -> list:
        """
        查找path目录下，以prefix开头, 以suffix结尾的文件
        :param path:   文件目录
        :param prefix: 文件前缀
        :param suffix: 文件结尾
        :return:
        """
        # print("查找到文件  \n")
        path_list = []

        # 判断某个文件名是否已suffix中某一个元素结尾，满足一个就代表 成功
        def fileEndWith(fileinner: str, suffixinner: list) -> bool:
            """
            :param fileinner:
            :param suffixinner:
            :return:
            """
            if len(fileinner) <= 0 or len(suffixinner) <= 0:
                return False
            for su in suffixinner:
                return fileinner.endswith(su)
            return False

        for root, dirs, files in os.walk(path):
            for file in files:
                # 先以文件名称来匹配，这样效率比较高
                if ((len(prefix) > 0 and file.startswith(prefix)) or len(prefix) <= 0) and (
                        len(suffix) > 0 and fileEndWith(file, suffix) or len(suffix) <= 0):
                    file_path = os.path.join(root, file)
                    path_list.append(file_path)
                    print(file_path + "\n")
        return path_list

    @classmethod
    def findAllClassAndMethodNameWithPathOC(cls, path: str) -> dict:
        """
        在oc格式下
        查找这个文件中所有的action
        :param path:
        :return:
        """
        if not os.path.exists(path):
            return {}
        # print("查找到文件  \n")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            # print("完整.m实现文件 \n" + content)
            # 获取到完整的匹配文件
            class_matchs = []
            try:
                class_full_pattern = re.compile(oc_full_implementation_regular)
                class_matchs = class_full_pattern.findall(content)
            except Exception as exc:
                print(exc)
            finally:
                if len(class_matchs) <= 0:
                    return {}
            # print("匹配到的完整类的实现 \n")
            # print(class_matchs)
            match_dict = {}
            for full_class_text in class_matchs:
                # print("完整类实现文件 \n" + full_class_text)
                class_name_pattern = re.compile(oc_implementation_regular)
                class_name_match = class_name_pattern.findall(full_class_text)
                class_name = class_name_match[0]
                # print("匹配到的类的名称 \n")
                # print(class_name_match)
                method_name_pattern = re.compile(oc_action_regular)
                method_name_matchs = []
                try:
                    method_name_matchs = method_name_pattern.findall(full_class_text)
                except Exception as exc:
                    print(exc)
                # print("匹配到的方法的实现 \n")
                # print(method_name_matchs)
                path_list = []
                for method_name in method_name_matchs:
                    path_list.append(method_name)
                match_dict[class_name] = path_list
        return match_dict

    @staticmethod
    def findPathWithFileName(path: str, foldname: str = oc_target_action_foldername):
        '''

        :param foldname:
        :param path:
        :return:
        '''
        # print("77777" + path)
        for root, dirs, files in os.walk(path):
            # print("Files")
            # print(dirs)
            for file in dirs:
                if file == foldname:
                    fullpath = os.path.join(root, file)
                    # print(fullpath)
                    if os.listdir(fullpath):
                        return fullpath
        return None

    @staticmethod
    def findCallerClassAndMethod(path: str):
        caller_dict: [str, list] = {}
        filepath = FileTool.findPathWithFileName(path)
        # print("文件目录" + filepath)
        if filepath is None:
            return {}
        for root, dirs, files in os.walk(filepath):
            for file in files:
                filepath = os.path.join(root, file)
                # print(filepath)
                if not file.endswith('.m') or file == 'YHMediator.m':
                    continue
                with open(filepath, 'r', encoding='utf-8') as filed:
                    file_content = filed.read()
                    caller_pattern = re.compile(oc_target_action_regular)
                    caller_matchs = caller_pattern.findall(file_content)
                    # print("方法替换文本内容 \n")
                    # print(file_content)
                    # print("匹配文本内容 \n")
                    # print(caller_matchs)
                    if len(caller_matchs) <= 0:
                        continue

                    map_dict = FileTool.replaceMethodnameWithRealCall(file_content)
                    # print(map_dict)
                    for target_action in caller_matchs:
                        target, action = target_action
                        if target in map_dict.keys() and map_dict[target] is not None:
                            target = map_dict[target]
                        if action in map_dict.keys() and map_dict[action] is not None:
                            action = map_dict[action]

                        action_list = []
                        if target in caller_dict.keys():
                            action_list = caller_dict[target]
                        if action_list is None:
                            caller_dict[target] = [action]
                        else:
                            action_list.append(action)
                            caller_dict[target] = action_list

        return caller_dict

    @staticmethod
    def replaceMethodnameWithRealCall(content: str) -> dict:
        replace_pattern = re.compile(oc_replace_target_action_regular)
        replace_matchs = replace_pattern.findall(content)
        map_dict = {}
        for replace in replace_matchs:
            replace_left, relace_right = replace
            map_dict[replace_left] = relace_right
        return map_dict


class MethodDetect:

    def __init__(self, path: str, prefix: str = 'Target_'):
        """
        :param path: 项目路径
        """
        self.path = path

    def detect_class(self) -> dict:
        class_paths = FileTool.findAllFilesWithPath(self.path)
        path_list = {}
        for path in class_paths:
            match_class_dict = FileTool.findAllClassAndMethodNameWithPathOC(path)
            path_list.update(match_class_dict)
        return path_list

    # 获取所有的调用地方
    def detect_caller(self) -> dict:
        return FileTool.findCallerClassAndMethod(self.path)


# 定义解析markdown数据的模型
class MarkDownModel:
    project = ""
    detail_content = ""

    def mark_down_info(self):
        wechat_dict = {"msgtype": "markdown"}
        content = """移动端项目<font color=\"warning\">{0}</font>告警！\n
            >存在没有实现的类及方法: <font color=\"warning\">{1}</font>
 	        \n请关注:<@81095534><@81075463><@81137040><@81122647><@80727655>
        """.format("YHDOS YHMediator服务提供者检测",
                   self.detail_content)
        mark_down_dict = {"content": content}
        wechat_dict["markdown"] = mark_down_dict
        return wechat_dict


class SendWeChatAlert:
    # 企业微信webhook地址
    url = ''
    # 企业微信发送内容
    content = {}

    def __init__(self, url, content):
        self.url = url
        self.content = content

    def sendWechatRequest(self):
        requests.post(
            url=self.url,
            data=json.dumps(self.content, ensure_ascii=False).encode("utf-8"),
            auth=('Content-Type', 'application/json'),
            verify=False
        )


def detect_method(debug: bool = True):
    # Use a breakpoint in the code line below to debug your script.
    cur_path = os.getcwd()
    cur_path = "/Users/fanguohuijack/Desktop/operation-cp-hcwms/yhdos-jianxuanmian/ios/Pods"
    methoddetect = MethodDetect(path=cur_path)
    resut_define = methoddetect.detect_class()
    # print(resut_define)
    resut_caller = methoddetect.detect_caller()
    # print(resut_caller)
    resut = {}
    for target in resut_caller.keys():
        actions = resut_caller[target]
        # 底层逻辑， 兼容实现的时候添加的前缀
        target = "Target_" + target
        actions = ["Action_" + element for element in actions]
        define_actions = []
        if target in resut_define.keys():
            define_actions = resut_define[target]
        actions_set = set(actions)
        define_action_set = set(define_actions)
        res = actions_set - define_action_set
        if len(res) > 0:
            resut[target] = list(res)
    # print("没有定义的方法")
    # print(resut)
    # print("成功了")
    # print("++++++method_detect++++++\n")
    full_info = "++++++method_detect++++++\n"
    if len(resut.keys()) <= 0:
        # print("😊😊😊😊😊所有硬编码的Target和Action都存在\n")
        full_info += "\n😊😊😊😊😊所有硬编码的Target和Action都存在\n"
        print(full_info)
        return
    else:
        # print("😭😭😭😭😭😭以下硬编码的Target和Action不存存在\n")
        full_info += "😭😭😭😭😭😭以下硬编码的Target和Action不存在\n"
        for element in resut.keys():
            # print("Target: \n \t" + element)
            full_info += ("\nTarget: \n \t" + element)
            actions = resut[element]
            # print("Action: ")
            full_info += "\nAction: "
            for action in actions:
                # print("\t"+action )
                full_info += "\n\t"+action
            # print("\n")
            full_info += "\n"
            # print(detail_content)
        # print("eeeee")
        print(full_info)
        markdownModel = MarkDownModel()
        # detail_content = json.dumps(resut, ensure_ascii=False).encode("utf-8")
        markdownModel.detail_content = full_info
        wechatInfoDict = markdownModel.mark_down_info()
        # 测试
        urltest = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cf8fceb4-349b-44eb-a734-36fd3cc840bb"
        # urltest = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b0cfdb22-5b44-427e-9552-8c1dd6ff1692"
        # 正式
        # urltest = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8796776b-58f4-4bc1-b30a-8af0f59e165a"
        chatAlert = SendWeChatAlert(urltest, wechatInfoDict)
        chatAlert.sendWechatRequest()


def main(argvs=None):
    test = True
    if argvs is not None and len(argvs) > 1:
        test = argvs[1] == 'DEBUG'
    detect_method()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    detect_method()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
