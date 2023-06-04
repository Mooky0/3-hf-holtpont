echo "Running the moodle tests"

out=$(cat input1.txt | python3 main.py)

if [[ "$out" == "T1,4,R2
T3,5,R3" ]]
then
    echo "Test1: Passed"
    let "count += 1"
else
    echo "Test1: Failed:\n"
    echo $out 
fi
    
out=$(cat input2.txt | python3 main.py)

if [[ "$out" == "T1,2,R1" ]]
then
    echo "Test2: Passed"
    let "count += 1"
else
    echo "Test2: Failed:\n"
    echo $out
fi

out=$(cat input3.txt | python3 main.py)

if [[ "$out" == "T2,2,R1" ]]
then
    echo "Test3: Passed"
    let "count += 1"
else
    echo "Test3: Failed:\n"
    echo $out
fi

out=$(cat input4.txt | python3 main.py)

if [[ "$out" == "T2,4,R1" ]]
then
    echo "Test4: Passed"
    let "count += 1"
else
    echo "Test4: Failed:\n"
    echo $out
fi

echo -n $count
echo "/4"