import json
import sys

if __name__ == "__main__":
	src=""
	with open(sys.argv[1],'r') as f:
		src = f.read()
	d = json.loads(src)
	path = [d]
	keys  = ["root"]
	types = ["dict"]
	indices = [0]
	while True:
		keytypes = [[],[],[],[]]  #0 STR, 1 INT, 2 DICT, 3 LIST
		for key in sorted(d.keys()):
			if type(d[key]) == type(""):
				keytypes[0].append(key)
			elif type(d[key]) == type(1):
				keytypes[1].append(key)
			elif type(d[key]) == type({}):
				keytypes[2].append(key)
			elif type(d[key]) == type([]):
				keytypes[3].append(key)

		for key in keytypes[0]+keytypes[1]:
			if d[key]=="":
				print("    ",key,": <empty>")
			else:
				print("    ",key,":",d[key])
		for key in keytypes[2]:
			print("    ",key)
		for key in keytypes[3]:
			print("    ",key," (list)",len(d[key]))
		printer = "root"
		for i,part in enumerate(keys):
			if i==0:
				pass
			elif types[i]=="array":
				printer+="["+part+"]["+str(indices[i])+"]"
			else:
				printer+="["+part+"]"
		print(printer)
		response = input("Which would you like to explore?")
		if response=="quit":
			break
		elif response==":print":
			print(d)
		elif response==">" and types[-1]=="array":
			path.pop()
			l = path[-1][keys[-1]]
			indices[-1]=min(indices[-1]+1,len(l)-1)
			d=l[indices[-1]]
			path.append(d)
		elif response=="<" and types[-1]=="array":
			path.pop()
			l = path[-1][keys[-1]]
			indices[-1]=max(indices[-1]-1,0)
			d=l[indices[-1]]
			path.append(d)
		elif response=="<<" and types[-1]=="array":
			path.pop()
			l = path[-1][keys[-1]]
			indices[-1]=0
			d=l[indices[-1]]
			path.append(d)
		elif response==">>" and types[-1]=="array":
			path.pop()
			l = path[-1][keys[-1]]
			indices[-1]=len(l)-1
			d=l[indices[-1]]
			path.append(d)
		elif response==".." and len(path)>1:
			path.pop()
			keys.pop()
			types.pop()
			indices.pop()
			d = path[len(path)-1]
		elif response in d.keys():
			n = d[response]
			if type(n)==type([]):
				print(type(n[0]))
				if len(n)==0:
					print("ZERO LENGTH")
				elif type(n[0])==type({}):
					d=n[0]
					path.append(d)
					types.append("array")
					keys.append(response)
					indices.append(0)
				elif type(n[0]) in (type(""),type(1)):
					print("Values: ",n)
			if type(n)==type({}):
				d=n
				path.append(d)
				types.append("dict")
				keys.append(response)
				indices.append(0)
			elif type(n) in (type(""),type(1)):
				print("Value:",n)
