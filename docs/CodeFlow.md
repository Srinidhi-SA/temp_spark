## Updated on 9/July/2018


## Updated on 9/July/2018


1. ** Job Types** :

    jobType:
    + *--metaData*: Metadata Generation for a dataset.
    + *--story*: Run Measure or Dimension analysis on the supplied dataset.
    + *--training*: ML Model training.
    + *--prediction*: ML Model Predictions for the trained models.
    + *--stockAdvisor*: Custom application for stock Analysis
    + *--testCase*: Evaluating test cases.

2. ** Analysis Types**:

    analysistype:
    + *--measure*: Measure Analysis when the target Variable is Measure type.
    + *--dimension* Dimension Analysis when the target Variable is Dimension type.

3. ** Directory Structure**:

    mAdvisor-MLScripts:
    + **_bi_**
        + **_algorithms_**:
            * Contains Scripts for ML algorithms and utils__
        + **_common_**:
            * Generic Classes for card structures,charts,models etc.
        + **_narratives_**:
            * Narrative Generation classes for different analysis.
        + **_parser_**:
            * Parser class for the config file used.
        + **_scripts_**:
            * Scripts to Trigger the Job submitted through Config.
        + **_settings_**:
            * Global Settings and configs.
        + **_sparkjobs_**:
            * Wrapper for calling the master script.
        + **_stats_**:
            * Scripts for various statistical analysis.
        + **_templates_**:
            * Jinja2 templates for generating narratives.
        + **_transformations_**:
            * DataFrame transformations like binning,subsetting scripts.
        + **_tests_**:
            * Test cases for different analysis.
