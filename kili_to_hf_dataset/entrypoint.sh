# to run in a Python3.7 environment with the requirements installed
case $1 in 

    kili2hfds)
    PYTHONPATH=$(pwd) python cmd/kili_to_local.py --local-path $2
    bash cmd/upload_to_gcs.sh $2
    datasets-cli test litter-challenge-test/ --save_infos --all_configs
    cd litter-challenge-test/ && git add dataset_infos.json && git commit -m "Updated from Kili" && git push
    ;;

    *)
    echo "Command not found!"
    ;;

esac
