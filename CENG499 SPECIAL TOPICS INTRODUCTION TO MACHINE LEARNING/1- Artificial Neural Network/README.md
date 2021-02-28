Model Training
python3 train.py

With that code, system will start to train model with hyperparameters that given in report. After each train, script is printing hyperparameters that tried and success result. At the end, script will do last training with selected best hyperparamaters and save an module state dictionary to file.

Model test with test data
python3 work.py

With that code, script loads model state dictionary that saved by train.py and use it to classify data at test file.

