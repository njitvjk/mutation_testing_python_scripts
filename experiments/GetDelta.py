



def loadMutant(filename):
	file=open('test_results/'+filename+'.txt');
	lines=file.readlines();
	data={};
	for line in lines:
		line=line.strip().split(",");
		test=line[0].strip();
		output=line[1].strip();
		data[test]=output;
	count=len(data);
	if count!=34:
		print(filename,count);
	return data;

def isSame(res_a,res_b):
	for t in res_a:
		if res_a[t]!=res_b[t]:
			return False;
	return True;

base_results=loadMutant('Base'); #load the results of the base program

mutants=['m1','m2', 'm3', 'm4', 'm6', 'm7', 'm8', 'm9', 'm10', 'm11', 'm12', 'm13', 'm14', 'm15', 'm16', 'm17', 'm19', 'm22', 'm25']
results={};
for m in mutants:
	results[m]=loadMutant(m); #load the results of each mutant (test number: test outcome)

d1={};
d2={};
d0={}
for m in mutants:
	d1[m]=[];
	d2[m]=[];
	d0[m]=[]
	for t in results[m]:
		if results[m][t]!=base_results[t]:
			d0[m].append(t);
	for t in results[m]:
		#if( ("IndexOutofBounds" in results[m][t]) or ("ClassCast" in results[m][t]) or ("OutOfMemoryError" in results[m][t]) or ("ComparisonFailure" in results[m][t]) ):
		if ("Exception" in results[m][t]):
				d2[m].append(t);
		elif results[m][t]!=base_results[t]:
				d1[m].append(t);
				d2[m].append(t);

writer=open("delta_analysis.csv",'w');
writer.write("Mutants,Delta 1,Delta 2,Delta 0\n");
for m in mutants:
	if len(d1[m])==0:
		d1[m]=["Empty"];
	if len(d2[m])==0:
		d2[m]=["Empty"];
	if len(d0[m])==0:
		d0[m]=["Empty"];
	tmp=[m,";".join(d1[m]),";".join(d2[m]),";".join(d0[m]),"\n"];
	writer.write(",".join(tmp));
writer.close();