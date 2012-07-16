for i in $(qstat | grep "$1" | awk '{print $1}'); do
    canceljob ${i}
done