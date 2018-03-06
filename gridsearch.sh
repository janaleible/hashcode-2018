#!/usr/bin/env bash

if [ -f "output/meta.txt" ] ; then
    rm "output/meta.txt"
fi

python3 script.py "a_example" 1 1 1 &
python3 script.py "a_example" 10 1 1 &
python3 script.py "a_example" 1 10 1 &
python3 script.py "a_example" 1 1 10 &
wait

python3 script.py "b_should_be_easy" 1 1 1 &
python3 script.py "b_should_be_easy" 10 1 1 &
python3 script.py "b_should_be_easy" 1 10 1 &
python3 script.py "b_should_be_easy" 1 1 10 &
wait

python3 script.py "c_no_hurry" 1 1 1 &
python3 script.py "c_no_hurry" 10 1 1 &
python3 script.py "c_no_hurry" 1 10 1 &
python3 script.py "c_no_hurry" 1 1 10 &
wait

python3 script.py "d_metropolis" 1 1 1 &
python3 script.py "d_metropolis" 10 1 1 &
python3 script.py "d_metropolis" 1 10 1 &
python3 script.py "d_metropolis" 1 1 10 &
wait

python3 script.py "e_high_bonus" 1 1 1 &
python3 script.py "e_high_bonus" 10 1 1 &
python3 script.py "e_high_bonus" 1 10 1 &
python3 script.py "e_high_bonus" 1 1 10 &
wait
