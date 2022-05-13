def loadMutant(filename):
    file = open('../experiments/test_results/' + filename + '.txt');
    lines = file.readlines();
    data = {};
    for line in lines:
        line = line.strip().split(",");
        test = line[0].strip();
        output = line[1].strip();
        data[test] = output;
    return data;


minimal_set_subs =['m1', 'm7', 'm10', 'm11', 'm12', 'm13', 'm16']

minimal_set_equ = ['m1','m2', 'm3', 'm4', 'm6', 'm7', 'm8', 'm9', 'm10', 'm11', 'm12', 'm13', 'm14', 'm15', 'm16', 'm17', 'm19', 'm22', 'm25']
experiment = 'Equivalence';

minimal_set = [];
if experiment == 'Subsumption':
    minimal_set = minimal_set_subs;
else:
    minimal_set = minimal_set_equ

base_results = loadMutant('Base');  # load the results of the base program

results = {};
for m in minimal_set:
    results[m] = loadMutant(m);
    # load the results of each mutant (test number: test outcome)

dif_set = {};
for t in base_results:
    dif_set[t] = {};
    for m in minimal_set:
        dif_set[t][m] = '0';  # by default the t is not a dif for m
        if results[m][t]!=base_results[t]:

          # if t have different results for m and base program, add t to dif set of m
            dif_set[t][m] = '1';
        print(dif_set[t][m])
writer = open("difsets_" + experiment + ".csv", "w");
writer.write("," + ",".join(minimal_set) + "\n");
for t in dif_set:
    temp = [str(t)];
    for m in minimal_set:
        temp.append(dif_set[t][m]);
    writer.write(",".join(temp) + "\n");
writer.close();
