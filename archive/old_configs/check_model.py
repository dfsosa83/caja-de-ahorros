import pickle

model_path = r'models/production/final_production_model_nested_cv.pkl'
print('Loading model file...')
try:
    with open(model_path, 'rb') as f:
        obj = pickle.load(f)
    print(f'Type: {type(obj)}')
    if isinstance(obj, dict):
        print(f'Dictionary keys: {list(obj.keys())}')
        for key, value in obj.items():
            print(f'  {key}: {type(value)} - has predict: {hasattr(value, "predict")}')
    else:
        print(f'Has predict method: {hasattr(obj, "predict")}')
        print(f'Object attributes: {dir(obj)[:10]}...')  # First 10 attributes
except Exception as e:
    print(f'Error: {e}')
