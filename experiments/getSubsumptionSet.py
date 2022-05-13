def loadBase():
    file = open('test_results/Base.txt');
    lines = file.readlines();
    data = {};
    for line in lines:
        line = line.strip().split(",");
        test = line[0].strip();
        output = line[1].strip();
        data[test] = output;
    # print(data)
    return data;


def loadmutantkills(base_results, filename):
    file = open('test_results/' + filename + '.txt');
    print(filename)
    lines = file.readlines();
    data = {};
    for line in lines:
        line = line.strip().split(",");
        test = line[0].strip();
        output = line[1].strip();
        if base_results[test] == output:
            data[test] = 0;
        # print(output)
        else:
            data[test] = 1;
    print(data);
    return data;


def loadMutant(filename):
    file = open('test_results/' + filename + '.txt');
    lines = file.readlines();
    data = {};
    for line in lines:
        line = line.rstrip('\n')
        line = line.rstrip('\t')
        line = line.strip().split(",");
        test = line[0].strip();
        output = line[1].strip();
        data[test] = output;
    # print(data)
    return data;


def isSame(res_a, res_b):
    for t in res_a:
        if res_a[t] != res_b[t]:
            return False;
    return True;


def MaSubsumesMb(res_a, res_b):
    subsumed = True;
    for t in res_a:
        if res_a[t] == 1:
            if res_b[t] != 1:
                subsumed = False;
                break;
    return subsumed;


base_results = loadBase();  # load the results of the base program

mutants = ['m' + str(i) for i in range(1, 27)];  # list of all mutants
#mutants = []
results = {};
real_output = {};
for m in mutants:
    results[m] = loadmutantkills(base_results,m);  # load the results (killed or survived) of each mutant (test number: 0 (survived), 1 (killed))
    real_output[m] = loadMutant(m);



indistig_mutants = {};
main_mutants = [];  # list of mutants that we are gonna test for subsumption.

for m_a in mutants:  # for each mutant m_a
    to_add_new_class = True;

    for m_b in indistig_mutants:  # for each main mutant in indisting classes
        if isSame(results[m_a], results[m_b]):
            print(True)

            # if m_a and m_b are indistiguishable, add m_a to class of m_b;
            indistig_mutants[m_b].append(m_a);print("indistingu",indistig_mutants[m_b])
            to_add_new_class = False;
            break;
    if to_add_new_class == True:  # if m_a is not indistiguishable with any mutants in indistig_mutants, create a new class for it.
        indistig_mutants[m_a] = [];


        # only work with killed mutants.
        if not isSame(real_output[m_a], base_results):
            main_mutants.append(m_a);
subsumed_mutants = {};
for m_a in main_mutants:  # for each mutant m_a (one per indisting classes)
    subsumed_mutants[m_a] = {};
    for m_b in main_mutants:  # for each other mutant m_b from different indistng classes
        if m_b == m_a:
            continue;
        subsumed_mutants[m_a][m_b] = MaSubsumesMb(results[m_a], results[
            m_b]);  # if m_a subsumes m_b then subsumed_mutants[m_a][m_b]=True, it is Flase otherwise.

minimal_set_subsumption = [];  # get roots (all mutants not subsumed by anything).

for m_a in main_mutants:  # for each mutant m_a
    m_a_isRoot = True;
    for m_b in main_mutants:  # for each oter mutant m_b
        if m_b == m_a:
            continue;
        if subsumed_mutants[m_b][m_a]:  # if m_a is subsumed by any mutant, it is not root
            m_a_isRoot = False;
            break;
    if m_a_isRoot:
        minimal_set_subsumption.append(m_a);

writer = open("analysis_subsumption.txt", "w");

writer.write("minimal set by subsumption:\n");
writer.write(", ".join(minimal_set_subsumption) + "\n\n\n");

writer.write("Indistinguishable Classes:\n");
count = 1;
for m in indistig_mutants:

    print("indistingm", indistig_mutants[m])

    writer.write("Class " + str(count) + ": " + m + ", " + ", ".join(indistig_mutants[m]) + "\n");
    count = count + 1;

writer.write("\n\n\n");
writer.write("Subsumption:\n");
for m_a in subsumed_mutants:
    for m_b in subsumed_mutants[m_a]:
        if subsumed_mutants[m_a][m_b]:
            writer.write(m_a + " --> " + m_b + "\n");

writer.close();
