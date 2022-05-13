

def loadData():
	file=open('delta_analysis.csv');
	lines=file.readlines();
	mutants={};
	for i in range(1,len(lines)):
		line=lines[i].strip().split(",");
		m=line[0].strip();
		tests_0=line[1].split(";");
		tests_1=line[2].split(";");
		tests_2=line[3].split(";");
		tests_0 = [i for i in tests_0 if i != 'Empty'];
		tests_1 = [i for i in tests_1 if i != 'Empty'];
		tests_2 = [i for i in tests_2 if i != 'Empty'];
		mutants[m]=[tests_0,tests_1,tests_2];
	return mutants;

def AllTestsIncluded(t1,t2):
	if (len(t1)==0) or (len(t2)==0):
		return False;
	for i in t1:
		if i not in t2:
			return False
	return True;

mutants=loadData();
all_mutants=list(mutants.keys());
Subsumption_D0={};
Subsumption_D1={};
Subsumption_D2={};

for m1 in mutants:
	Subsumption_D0[m1]=[];
	Subsumption_D1[m1]=[];
	Subsumption_D2[m1]=[];
	for m2 in mutants:
		if m1==m2:
			continue;
		if AllTestsIncluded(mutants[m1][0],mutants[m2][0]):
			Subsumption_D0[m1].append(m2);
		if AllTestsIncluded(mutants[m1][1],mutants[m2][1]):
			Subsumption_D1[m1].append(m2);
		if AllTestsIncluded(mutants[m1][2],mutants[m2][2]):
			Subsumption_D2[m1].append(m2);


writer_D0_matrix=open("subsumption/D0_matrix.csv",'w');
writer_D1_matrix=open("subsumption/D1_matrix.csv",'w');
writer_D2_matrix=open("subsumption/D2_matrix.csv",'w');
writer_D0_list=open("subsumption/D0_list.txt",'w');
writer_D1_list=open("subsumption/D1_list.txt",'w');
writer_D2_list=open("subsumption/D2_list.txt",'w');
writer_D0_matrix.write(","+",".join(all_mutants)+"\n");
writer_D1_matrix.write(","+",".join(all_mutants)+"\n");
writer_D2_matrix.write(","+",".join(all_mutants)+"\n");

for mi in all_mutants:
	temp_0=[mi];
	temp_1=[mi];
	temp_2=[mi];
	for mj in all_mutants:
		if mj in Subsumption_D0[mi]:
			temp_0.append("x");
			writer_D0_list.write(mi+" --> "+mj+"\n")
		else:
			temp_1.append("");
		if mj in Subsumption_D1[mi]:
			temp_1.append("x");
			writer_D1_list.write(mi+" --> "+mj+"\n")
		else:
			temp_1.append("");
		if mj in Subsumption_D2[mi]:
			temp_2.append("x");
			writer_D2_list.write(mi+" --> "+mj+"\n")
		else:
			temp_2.append("");
	writer_D0_matrix.write(",".join(temp_0)+"\n")
	writer_D1_matrix.write(",".join(temp_1)+"\n")
	writer_D2_matrix.write(",".join(temp_2)+"\n")

writer_D0_matrix.close();
writer_D1_matrix.close();
writer_D2_matrix.close();
writer_D0_list.close();
writer_D1_list.close();
writer_D2_list.close();



