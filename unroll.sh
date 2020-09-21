INPUT_FILE=$1
UNROLLING_DEPTH=$2
OUTPUT_FILE=$3

./unroll_isc $INPUT_FILE ${INPUT_FILE}_temp.delete $UNROLLING_DEPTH

./iscas2symcnf ${INPUT_FILE}_temp.delete $OUTPUT_FILE

rm *_temp.delete
