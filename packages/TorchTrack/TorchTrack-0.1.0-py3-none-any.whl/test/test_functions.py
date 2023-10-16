from track_ml import track_functions

def test_track_functions():
    track_null_params = track_functions.JsonModelData("None", None, None, None) 

    assert track_null_params.print_saved_model_data() == True 
    #assert track_null_params._model_training_data == None
    #assert track_null_params._model_architecture == None
    #assert track_null_params._model_optimizer == None
    #assert track_null_params.save_model_data() == None
