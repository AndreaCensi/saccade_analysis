for species in D*; do
	pushd $species/processed
	tar cvhfz use_for_report.tgz use_for_report/
	popd
done

