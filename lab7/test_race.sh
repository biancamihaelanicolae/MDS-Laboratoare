cd /mnt/c/Users/"Bianca Mihaela"/Desktop/mds-lab1/lab7
gcc -pthread race.c -o race
gcc -std=c11 -pthread race_fixed.c -o race_fixed
echo "=== Race (expected 2000000) ==="
for i in 1 2 3; do
    echo -n "Run $i: "
    ./race
done
echo "=== Fixed (expected 2000000) ==="
for i in 1 2 3; do
    echo -n "Run $i: "
    ./race_fixed
done
