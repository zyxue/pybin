# for seq in sq1 sq2 sq3 sq4 sq5 sq6; do
#     for cdt in m300 w300; do
# 	python dihedral_ange_analysis.py \
# 	    -f "/home/zyxue/labwork/mono_meo/ogd/g_rama/${seq}${cdt}*dihedral*xvg" \
# 	    -o ${seq}${cdt}.png
#     done
# done

for seq in sq1 sq2 sq3 sq4 sq5 sq6; do
    for cdt in m300 w300; do
	for inf in /home/zyxue/labwork/mono_meo/ogd/g_rama/${seq}${cdt}s[0-3]0_rama.xvg; do 
	    python dihedral_ange_analysis.py -f ${inf} -o ${inf:0:55}.png
	done
    done
done