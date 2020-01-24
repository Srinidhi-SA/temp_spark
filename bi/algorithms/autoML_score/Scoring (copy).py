def score_model_autoML(spark,linear_df,tree_df,dataframe_context,df_helper_linear_df,df_helper_tree_df,metaParserInstance_linear_df,metaParserInstance_tree_df):
    dataframe_context.set_anova_on_scored_data(True)
    LOGGER = dataframe_context.get_logger()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    jobName = dataframe_context.get_job_name()
    ignoreMsg = dataframe_context.get_message_ignore()
    targetLevel = dataframe_context.get_target_level_for_model()
    dataCleansingDict = dataframe_context.get_dataCleansing_info()
    featureEngineeringDict = dataframe_context.get_featureEngginerring_info()
    print("Prediction Started")
    dataframe_context.initialize_ml_model_prediction_weight()

    st = time.time()
    story_narrative = NarrativesTree()
    story_narrative.set_name("scores")
    result_setter = ResultSetter(dataframe_context)
    model_path = dataframe_context.get_model_path()
    print("model path",model_path)
    result_column = dataframe_context.get_result_column()



    # Linear
    if result_column in linear_df.columns:
        df_helper_linear_df.remove_null_rows(result_column)
    linear_df = df_helper_linear_df.get_data_frame()
    linear_df = df_helper_linear_df.fill_missing_values(linear_df)

    # Tree
    if result_column in tree_df.columns:
        df_helper_tree_df.remove_null_rows(result_column)
    tree_df = df_helper_tree_df.get_data_frame()
    tree_df = df_helper_tree_df.fill_missing_values(tree_df)





    model_slug = model_path
    score_slug = dataframe_context.get_score_path()
    print("score_slug",score_slug)
    basefoldername = GLOBALSETTINGS.BASEFOLDERNAME_SCORES
    score_file_path = MLUtils.create_scored_data_folder(score_slug,basefoldername)
    appid = str(dataframe_context.get_app_id())
    app_type = dataframe_context.get_app_type()
    algorithm_name = dataframe_context.get_algorithm_slug()[0]
    print("algorithm_name",algorithm_name)
    print("score_file_path",score_file_path)
    print("model_slug",model_slug)

    scriptWeightDict = dataframe_context.get_ml_model_prediction_weight()
    scriptStages = {
        "preprocessing":{
            "summary":"Dataset Loading Completed",
            "weight":4
            }
        }
    print(scriptWeightDict)
    CommonUtils.create_update_and_save_progress_message(dataframe_context,scriptWeightDict,scriptStages,"initialization","preprocessing","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

    if app_type == "CLASSIFICATION":
        model_path = score_file_path.split(basefoldername)[0]+"/"+GLOBALSETTINGS.BASEFOLDERNAME_MODELS+"/"+model_slug+"/"+algorithm_name
        dataframe_context.set_model_path(model_path)
        dataframe_context.set_score_path(score_file_path)
        selected_model_for_prediction = [GLOBALSETTINGS.SLUG_MODEL_MAPPING[algorithm_name]]
        print("selected_model_for_prediction", selected_model_for_prediction)
        if "randomforest" in selected_model_for_prediction:
            trainedModel = RFClassificationModelScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "xgboost" in selected_model_for_prediction:
            trainedModel = XgboostScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"xgboost",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "Neural Network" in selected_model_for_prediction:
            trainedModel = NeuralNetworkScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"xgboost",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "logisticregression" in selected_model_for_prediction:
            trainedModel = LogisticRegressionScript(linear_df, df_helper_linear_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_linear_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"logisticRegression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "TensorFlow" in selected_model_for_prediction:
            trainedModel = TensorFlowScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"TensorFlow",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "Neural Networks(pyTorch)" in selected_model_for_prediction:
            trainedModel = NNPTClassificationScript(tree_df, df_helper_tree_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_tree_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"Neural Networks(pyTorch)",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        elif "naive bayes" in selected_model_for_prediction:
            trainedModel = NBMClassificationModelScript(linear_df, df_helper_linear_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_linear_df)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"naive bayes",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
                try:
                    trainedModel = NBGClassificationModelScript(linear_df, df_helper_linear_df, dataframe_context, spark, story_narrative,result_setter,metaParserInstance_linear_df)
                    trainedModel.Predict()
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"naive bayes",e)
                    CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            print("Scoring Done in ", time.time() - st,  " seconds.")
        else:
            print("Could Not Load the Model for Scoring")

        # scoreSummary = CommonUtils.convert_python_object_to_json(story_narrative)
        storycards = result_setter.get_score_cards()
        storyNode = NarrativesTree()
        storyNode.add_cards(storycards)
        # storyNode = {"listOfCards":[storycards],"listOfNodes":[],"name":None,"slug":None}
        scoreSummary = CommonUtils.convert_python_object_to_json(storyNode)
        print(scoreSummary)
        jobUrl = dataframe_context.get_job_url()
        response = CommonUtils.save_result_json(jobUrl,scoreSummary)
        progressMessage = CommonUtils.create_progress_message_object("final","final","info","mAdvisor Has Successfully Completed Building Machine Learning Models",100,100,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        print("Model Scoring Completed in ", time.time() - st, " seconds.")

    elif app_type == "REGRESSION":
        pass
        '''
        To be done later when regression scoring is wired
        '''
        headNodeJson = CommonUtils.convert_python_object_to_json(headNode)
        print(headNodeJson)
        response = CommonUtils.save_result_json(jobUrl,headNodeJson)
        # print "Dimension Analysis Completed in", time.time()-st," Seconds"
        print("Model Scoring Completed in ", time.time() - st, " seconds.")
