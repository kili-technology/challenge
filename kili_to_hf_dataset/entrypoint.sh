# to run in a Python3.7 environment with the requirements installed
case $1 in

    kili2hfds)
    PYTHONPATH=$(pwd) python cmd/kili_to_local.py --local-path $2 && \
    bumpversion --current-version $(cat VERSION) minor VERSION plastic_in_river/plastic_in_river.py && \
    bash cmd/upload_to_gcs.sh $2 && \
    datasets-cli test plastic_in_river/ --save_infos --all_configs && \
    cd plastic_in_river/ && git submodule update --remote && git add dataset_infos.json && git commit -m "Updated from Kili: v$(cat VERSION)" && git push HEAD:main && cd .. && \
    git add VERSION && git commit -m "Dataset updated from Kili: v$(cat VERSION)"
    ;;

    *)
    echo "Command not found!"
    ;;

esac
