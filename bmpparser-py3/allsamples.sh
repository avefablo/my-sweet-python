for x in samples/*.bmp; do
echo $x
python3 launcher.py $x 
echo
done

