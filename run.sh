
source="demo2"
#generate the first unrolling
./unroll $source.isc ${source}_1.isc 1

#generate the second unrolling
./unroll $source.isc ${source}_2.isc 2

#generate the third unrolling
./unroll $source.isc ${source}_3.isc 3


# convert to symbolic CNF
./iscas2symcnf ${source}_1.isc ${source}_1.scnf

./iscas2symcnf ${source}_2.isc ${source}_2.scnf

./iscas2symcnf ${source}_3.isc ${source}_3.scnf

python $source.py
