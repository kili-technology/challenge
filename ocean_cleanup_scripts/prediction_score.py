"""
For the Ocean Cleanup Challenge
"""

import os
from kili.client import Kili
from datetime import datetime

team_project_id_array = []
main_project_id=''

def get_json_response(category):
    return {'JOB_0': {'categories': [{'confidence': 100,
       'name': category}]}}

def get_response_category(json_response):
    return json_response['JOB_0']['categories'][0]['name']


def get_ground_truth_dict(kili, main_project_id):
    assets_with_high_consensus = kili.assets(
        project_id = main_project_id,
        consensus_mark_gt=0.66,
        status_in=['LABELED'],
        fields=['labels.jsonResponse', 'labels.isLatestLabelForUser', 'consensusMark', 'id', 'externalId'])
    ground_truths = {}
    for asset in assets_with_high_consensus:
        latest_labels = [label for label in asset['labels'] if label.get('isLatestLabelForUser')]
        all_labels_categories = [get_response_category(label['jsonResponse']) for label in latest_labels]
        ground_truths[[asset['externalId']]] = max(set(all_labels_categories), key = all_labels_categories.count)
    return ground_truths


def calculate_predictions_accuracy(kili, project_id, ground_truths):
    assets_with_predictions = kili.assets(
        project_id = project_id,
        status_in=['PREDICTION'],
        fields=['labels.jsonResponse', 'labels.isLatestLabelForUser','labels.createdAt', 'id', 'externalId'])
    score = 0
    for asset in assets_with_predictions:
        predictions = asset['labels']
        latest_prediction= max(predictions, key=lambda label: datetime.strptime(label['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        prediction_category = get_response_category(latest_prediction['jsonResponse'])
        if ground_truths.get(asset['externalId']) and ground_truths.get(asset['externalId']) == prediction_category:
            score+=1
    return score/len(ground_truths)

def main():
    api_key = os.getenv('KILI_API_KEY')
    kili = Kili(api_key=api_key)
    ground_truth = get_ground_truth_dict(kili, main_project_id)
    final_scores={}
    for project_id in team_project_id_array:
        final_scores[project_id] = calculate_predictions_accuracy(kili, project_id, ground_truth)
    print(final_scores)
    return final_scores





if __name__ == '__main__':
    main()
