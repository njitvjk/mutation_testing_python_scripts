class TestData:
	def __init__(self,name):
		self.name=name;
		self.killedMutants=[];
	
	def addKilledMutants(self,m):
		if m not in self.killedMutants:
			self.killedMutants.append(m);
	
	def removeMutant(self,m):
		if m in self.killedMutants:
			self.killedMutants.remove(m);
	
	def getCoverage(self):
		return len(self.killedMutants);
import random;
def sortTestsByCoverage(dic_tests):
	tests_covs=[];
	for t in dic_tests:
		tests_covs.append([t,dic_tests[t].getCoverage()]);
	random.shuffle(tests_covs)
	tests_covs.sort(key = lambda x:x[1],reverse =True)
	print(tests_covs)
	return tests_covs;
type='Subsumption';
writer=open("MinimalTestSuite_"+type+".txt",'w');
writer.write("Minimal Test Suite by "+type+":\n");
trial=0;
while trial<10:
	trial=trial+1;
	tests={}
	mutants=[];

	filename='difsets_'+type+'.csv';
	file=open(filename);
	lines=file.readlines();
	mutants=lines[0].strip().split(",")[1:];
	for i in range(1,len(lines)):
		line=lines[i].strip().split(",");
		test_name=line[0];
		test_obj= TestData(test_name);
		for j in range(1,len(line)):
			if line[j]=='1':
				test_obj.addKilledMutants(mutants[j-1]);
		tests[test_name]=test_obj;

	minimal_test_suits=[];
	print("len",len(mutants))
	while len(mutants)>1:
		#print(len(mutants))
		sorted=sortTestsByCoverage(tests);
		biggest_test=sorted[0][0]
		print(biggest_test)
		if biggest_test==-1: break
		killed_mutants=tests[biggest_test].killedMutants;
		minimal_test_suits.append(biggest_test);
		del tests[biggest_test]
		for t in tests:
			for m in killed_mutants:
				tests[t].removeMutant(m);
		for m in killed_mutants:
			mutants.remove(m);
	writer.write("Set "+str(trial)+"(size="+str(len(minimal_test_suits))+"):"+",".join(minimal_test_suits)+"\n");

writer.close();
