from multiprocessing import cpu_count
from XME.XMElib.ArrayOperator import ArrayOperator
from XME.XMElib.Executor import Executor
from XME.XMElib.Logputter import Logputter
from XME.XMElib.version_info import XME_Version_info
from copy import deepcopy
def get_par(args,name,default=None):
	try:
		return args[name]
	except:
		return default
class XME:
	aoobj_array=[]
	exobj_array=[]
	class Array:
		def __init__(self,array):
			self.array=array
			self.length=len(array)
	def __init__(self,*fun,**args):
		self.pnum=get_par(args,"pnum",cpu_count())
		self.funs=[]
		if get_par(args,"do_with_log",True):
			self.logobj=Logputter(get_par(args,"logfile"),XME_Version_info,get_par(args,"show_version_info",True))
			self.logobj.print_in_screen=get_par(args,"print_in_screen",True)
		else:
			self.logobj=None
		def func(funum,*targ,**args):
			args.update({"logobj":self.logobj})
			if self.logobj!=None:
				args.update({"print":self.logobj.write_log})
			calnum=get_par(args,"calnum",0)
			if calnum==0:
				for i in targ:
					if type(i)==self.Array:
						calnum=max(calnum,i.length)
				for i in args.keys():
					if type(args[i])==self.Array:
						calnum=max(calnum,args[i].length)
			if calnum==0:
				calnum+=1 #at least run once
			ao=self.ao(calnum,self.pnum)
			for i in targ: #first set
				if type(i)!=self.Array:
					ao.add_common_args(i)
				else:
					ao.add_argscut(i.array)
			for i in fun[funum].__code__.co_varnames: #follow sequence
				if i in args.keys():
					if type(args[i])!=self.Array:
						ao.add_common_args(args[i])
					else:
						ao.add_agrscut(args[i].array)
			return ao
			#ex=self.ex(fun[funum],pnum=self.pnum)
			#ex.build_from_ao(ao)
			#ao.result_combine()
			#return ao.results
		if len(fun)>0:
			def single_fun(*targ,**args):
				ao=func(-1,*targ,**args)
				ex=self.ex(fun[-1],pnum=self.pnum)
				ex.build_from_ao(ao)
				ao.result_combine()
				return ao.results
			self.fun=single_fun
			def multi_funs(funum_array=range(len(fun)),targ_array=[[]]*len(fun),args_array=[{}]*len(fun)):
				if len(funum_array)!=len(targ_array) or len(funum_array)!=len(args_array):
					print("Error parameters number")
					return ()
				ao=[]
				results=[]
				tfuns=[]
				for i in range(len(funum_array)):
					tfuns.append(fun[funum_array[i]])
					ao.append(func(funum_array[i],*(targ_array[i]),**(args_array[i])))
				ex=self.ex(*tfuns,pnum=self.pnum)
				ex.build_from_ao(ao)
				results=[]
				for i in range(len(funum_array)):
					ao[i].result_combine()
					results.append(ao[i].results)
				return tuple(results)
			self.funs=multi_funs
	def ao(self,calnum,pnum=None):
		if pnum==None:
			pnum=self.pnum
		self.aoobj_array.append(ArrayOperator(cal_num=calnum,pnum=pnum))
		return self.aoobj_array[-1]
	def ex(self,*fun,**args):
		self.exobj_array.append(Executor(*fun,**args))
		return self.exobj_array[-1]
	def clean(self):
		self.aoobj_array=[]
		self.exobj_array=[]
def build(*fun,**args):
	return XME(*fun,**args)
