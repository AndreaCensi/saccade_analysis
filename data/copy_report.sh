dir=copy-of-report

mkdir -p $dir

for a in D*; do

	cp -R $a/report  $dir/$a
done
