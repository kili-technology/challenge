# to run in a Python3.7 environment with the requirements installed
case $1 in

    kili2hfds)
    LOCAL_PATH=/tmp/kili2hfds/plastic_in_river
    mkdir -p $LOCAL_PATH && \
    PYTHONPATH=$(pwd) python cmd/kili_to_local.py --local-path $LOCAL_PATH && \
    bumpversion --current-version $(cat VERSION) minor VERSION plastic_in_river/plastic_in_river.py && \
    bash cmd/upload_to_gcs.sh $LOCAL_PATH && \
    datasets-cli test plastic_in_river/ --save_infos --all_configs && \
    cd plastic_in_river/ && git submodule update --remote && git add dataset_infos.json plastic_in_river.py && git commit -m "Updated from Kili: v$(cat ../VERSION)" && git push origin HEAD:main && cd .. && \
    git add VERSION && git commit -m "Dataset updated from Kili: v$(cat VERSION)"
    rm -r $LOCAL_PATH
    ;;

    *)
    echo "Command not found!"
    ;;

esac
