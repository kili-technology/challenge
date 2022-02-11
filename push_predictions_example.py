import os
import uuid

from kili.client import Kili


def push_predictions_example():
    kili = Kili(api_key=os.getenv('KILI_API_KEY'))
    kili.create_predictions(
        project_id='',
        external_id_array=['56a211f916a347a4bb52bb6a5547d23a'],
        model_name_array=['v1'],
        json_response_array=[{
            'JOB': {
                'annotations': [{
                    'boundingPoly': [{
                        'normalizedVertices': [
                            { 'x': 0.09, 'y': 0.84 },
                            { 'x': 0.09, 'y': 0.36 },
                            { 'x': 0.92, 'y': 0.36 },
                            { 'x': 0.92, 'y': 0.84 }
                        ]
                    }],
                    'categories': [{ 'name': 'PLASTIC_BAG' }],
                    'mid': str(uuid.uuid4()),
                    'type': 'rectangle',
                }]
            }
        }
    ])

if __name__ == '__main__':
    push_predictions_example()