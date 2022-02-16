
DATA_DIR=$1
CURR_DIR=$(pwd)
VERSION=$(cat VERSION)

for SPLIT in train test validation
do
    cd $DATA_DIR/$SPLIT
    rm -f annotations.tar.gz
    rm -f images.tar.gz
	tar -czvf annotations.tar.gz *.txt
    tar -czvf images.tar.gz *.jpg
    rm *.txt
    rm *.jpg
    gsutil cp -r "*.tar.gz" gs://kili-datasets-public/plastic-in-river/v$VERSION/$SPLIT/
done
cd $CURR_DIR