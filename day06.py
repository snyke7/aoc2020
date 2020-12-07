# sed ':a;N;$!ba;s/\n\n/€/g' day06_input.txt | sed ':a;N;$!ba;s/\n//g' | sed 's/€/\n/g' > day06_output.txt

def get_solution():
    with open('day06_output.txt') as f:
        counts = [len(set(line.rstrip())) for line in f.readlines()]
        print(counts)
        print(sum(counts))
    with open('day06_output_pt2.txt') as f:
        counts = [
            len(slist[0].intersection(*slist[1:])) for slist in (
                list(map(frozenset, line.rstrip().split('|'))) for line in f.readlines()
            ) if slist
        ]
        print(counts)
        print(sum(counts))
