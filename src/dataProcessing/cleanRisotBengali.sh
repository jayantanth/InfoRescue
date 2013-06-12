cd ../../data/RISOT-DATA/
pwd

for z in *
do
	if [ -d "$z" ]; then
		echo $z
		mkdir -p ../RISOT-DATA_cleaned/$z/
		cd $z
		for x in *
		do
			mkdir ../../RISOT-DATA_cleaned/$z/$x/
			echo $x
			cd $x
			for i in *
			do
				mkdir ../../../RISOT-DATA_cleaned/$z/$x/$i
				echo $i
				cd $i
				for j in *
				do
					echo $j
					head -n -2 $j | tail -n +4 > ../../../../RISOT-DATA_cleaned/$z/$x/$i/$j
				done
				cd ..
			done
			cd ..
		done
		cd ..
	fi
done