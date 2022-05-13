class TestData:
    def __init__(self, name):
        self.name = name;
        self.killedMutants = [];

    def addKilledMutants(self, m):
        if m not in self.killedMutants:
            self.killedMutants.append(m);

    def removeMutant(self, m):
        if m in self.killedMutants:
            self.killedMutants.remove(m);

    def getCoverage(self):
        return len(self.killedMutants);


import random;


def sortTestsByCoverage(dic_tests):
    tests_covs = [];
    print(dic_tests)
    for t in dic_tests:
        if not dic_tests:
            break;
        tests_covs.append([t, dic_tests[t].getCoverage()]);
    random.shuffle(tests_covs)
    tests_covs.sort(key=lambda x: x[1], reverse=True)

    return tests_covs;


def loadBase(MTS):
    file = open('test_results/Base.txt');
    lines = file.readlines();
    data = {};
    for line in lines:
        line = line.strip().split(",");
        test = line[0].strip();
        output = line[1].strip();
        if test in MTS:
            data[test] = output;
    return data;


def loadMutant(base_results, filename, MTS):
    file = open('test_results/' + filename + '.txt');
    lines = file.readlines();
    data = {};
    for line in lines:
        line = line.strip().split(",");
        test = line[0].strip();
        output = line[1].strip();
        if test in MTS:
            data[test] = output;
    return data;


def isSame(res_a, res_b):
    for t in res_a:
        if res_a[t] != res_b[t]:
            return False;
    return True;


def isError(test_output):
    #if (("IndexOutofBounds" in test_output) or ("ClassCast" in test_output) or (
            #"OutOfMemoryError" in test_output) or ("ComparisonFailure" in test_output)):
    if("Exception" in test_output):
        return True
    return False


def is_different(res1, res2):
    if type == '0':
        return res1 != res2
    if type == '1':
        if isError(res1) or isError(res2):
            return False
        return res1 != res2
    if type == '2':
        if isError(res1) and isError(res2):
            return False
        return res1 != res2


type = '1';
writer = open("MinimalTestSuite_Delta" + type + ".txt", 'w');
writer_killed = open("Killed_MinimalTestSuite_Delta" + type + ".txt", 'w');
writer.write("Minimal Test Suite by Delta" + type + ":\n");
writer_killed.write("Killed Mutants by Minimal Test Suites by Delta" + type + ":\n");
trial = 0;
ALL_SETS = [];
set_number = 0;
while trial < 5000:
    trial = trial + 1;
    tests = {}
    mutants = [];
    #print(trial);
    filename = 'difsets_' + type + '.csv';
    file = open(filename);
    lines = file.readlines();
    mutants = lines[0].strip().split(",")[1:];
    #print("mutants",mutants);
    for i in range(1, len(lines)):
        line = lines[i].strip().split(",");
        test_name = line[0];

        test_obj = TestData(test_name);
        for j in range(1, len(line)):
            if line[j] == '1':
                test_obj.addKilledMutants(mutants[j - 1]);
        tests[test_name] = test_obj;


    minimal_test_suits = [];



    while len(mutants) > 1:
        sorted = sortTestsByCoverage(tests);
        print(sorted)

        biggest_test = sorted[0][0];
        if bool(biggest_test):

            killed_mutants = tests[biggest_test].killedMutants;
            minimal_test_suits.append(biggest_test);
            del tests[biggest_test]
            for t in tests:
                for m in killed_mutants:
                    tests[t].removeMutant(m);
            for m in killed_mutants:
                mutants.remove(m);

    minimal_test_suits = [str(i) for i in minimal_test_suits];
    print("minimal",minimal_test_suits);
    minimal_test_suits.sort();
    minimal_test_suits = [str(i) for i in minimal_test_suits];
    str_test_suits = ",".join(minimal_test_suits);
    if str_test_suits in ALL_SETS:
        continue;
    set_number = set_number + 1;
    ALL_SETS.append(str_test_suits);
    writer.write("Set " + str(set_number) + "(size=" + str(len(minimal_test_suits)) + "):" + ",".join(
        minimal_test_suits) + "\n");

    base_results = loadBase(minimal_test_suits);  # load the results of the base program
    mutants_all = ['m' + str(i) for i in range(1, 21)];  # list of all mutants
    results_all = {};
    for m in mutants_all:
        results_all[m] = loadMutant(base_results, m, minimal_test_suits);
    killed_mutants_using_MTS = [];
    for m in mutants_all:
        for t in results_all[m]:
            if is_different(results_all[m][t], base_results[t]):
                killed_mutants_using_MTS.append(m);
                break
    writer_killed.write("\nKilled Mutants using set " + str(set_number) + "(killed mutants=" + str(
        len(killed_mutants_using_MTS)) + "):\n" + ",".join(killed_mutants_using_MTS) + "\n");
writer.close();
writer_killed.close();
