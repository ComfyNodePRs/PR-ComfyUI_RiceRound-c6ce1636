_E='file_name'
_D='options_value'
_C='choice_node'
_B='python_class_name'
_A=True
import hashlib,json
from pathlib import Path
from server import PromptServer
import re
from.utils import get_local_app_path
class RicePromptInfo:
	_instance=None;_initialized=False
	def __new__(A):
		if A._instance is None:A._instance=super(RicePromptInfo,A).__new__(A)
		return A._instance
	def __init__(A):
		if RicePromptInfo._initialized:return
		A.task_info_folder=get_local_app_path()/'tasks'
		if not A.task_info_folder.exists():A.task_info_folder.mkdir(parents=_A)
		A.choice_node_map={};A.new_choice_file_map={};A.choice_classname_map={};A.load_choice_node_map();RicePromptInfo._initialized=_A
	def clear(A):A.choice_node_map.clear();A.new_choice_file_map.clear()
	def get_choice_server_folder(B):
		A=B.task_info_folder/_C
		if not A.exists():A.mkdir(parents=_A)
		return A
	def load_choice_node_map(A):
		E=A.get_choice_server_folder()
		for B in E.glob('*.json'):
			try:
				with open(B,'r',encoding='utf-8')as F:
					C=json.load(F);D=C.get(_B)
					if D:A.choice_classname_map[D]=C
			except json.JSONDecodeError:print(f"Error parsing JSON from server file: {B}");continue
	def get_choice_node_options(A,node_class_name):return A.choice_classname_map.get(node_class_name,{}).get(_D,[])
	def get_choice_classname(A,node_id):return A.choice_node_map.get(node_id,{}).get(_B,'')
	def get_choice_value(A,node_id):return A.choice_node_map.get(node_id,{}).get(_D,[])
	def save_choice_classname(D,save_folder):
		A=Path(save_folder)/_C
		if not A.exists():A.mkdir(parents=_A)
		for(F,B)in D.new_choice_file_map.items():
			C=B.get(_E,'')
			if C:
				with open(A/f"{C}.json",'w',encoding='utf-8')as E:json.dump(B,E,ensure_ascii=False,indent=4)
	def set_node_additional_info(B,node_additional_info):
		H='template_id';C=node_additional_info
		if C and isinstance(C,dict):
			B.template_id=C.get(H,'');I=C.get('choice_node_map',{})
			for(D,A)in I.items():
				D=int(D);G=A.get('class_name','');A[H]=B.template_id;A['display_name']=G;J=A.get('node_type','')
				if J=='RiceRoundAdvancedChoiceNode':
					E=re.sub('[<>:"/\\\\|?*]','',G);F='RiceRoundAdvancedChoiceNode_'+hashlib.md5(E.lower().encode()).hexdigest()
					if F in B.choice_classname_map:print(f"Error RicePromptInfo set_node_additional_info python_class_name {F} already exists");PromptServer.instance.send_sync('rice_round_toast',{'content':'选择名称重复，如果本身是同一类型的节点，可以忽略提示','type':'info','duration':5000})
					A[_B]=F;A[_E]=E;B.new_choice_file_map[E]=A
				B.choice_node_map[D]=A