
import pathlib,shutil,os

def set_env_configs():
    snowpark_configs = '''[
    {
        "field_id": "snow_role",
        "field_label": "Snowpark role",
        "field_mandatory": "yes",
        "field_placeholder": "Snow Role",
        "field_type": "hidden",
        "field_value": "FOSFOR_REFRACT",
        "grid_value": 4,
        "referenceId": "0b45f5a2-3cbd-45a0-90a7-4488d2f5ff2b",
        "secured": "false"
    },
    {
        "field_id": "snow_database",
        "field_label": "Snow database",
        "field_mandatory": "yes",
        "field_placeholder": "Snow Database",
        "field_type": "hidden",
        "field_value": "FOSFOR_REFRACT",
        "grid_value": 4,
        "secured": "false"
    },
    {
        "field_id": "snow_warehouse",
        "field_label": "Snow warehouse",
        "field_mandatory": "yes",
        "field_placeholder": "Snow Warehouse",
        "field_type": "hidden",
        "field_value": "FOSFOR_REFRACT",
        "grid_value": 4,
        "secured": "false"
    },
    {
        "field_id": "snow_table",
        "field_label": "Snow table",
        "field_mandatory": "yes",
        "field_placeholder": "snow table",
        "field_type": "hidden",
        "field_value": "SCB_DRIFT_CUR",
        "grid_value": 4,
        "secured": "false"
    },
    {
        "field_id": "snow_schema",
        "field_label": "Snow schema",
        "field_mandatory": "yes",
        "field_placeholder": "Snow Schema",
        "field_type": "hidden",
        "field_value": "SALES",
        "grid_value": 4,
        "secured": "false"
    },
    {
        "field_id": "snow_user",
        "field_label": "Snow user",
        "field_mandatory": "yes",
        "field_placeholder": "Snow User",
        "field_type": "hidden",
        "field_value": "REFRACT.FOSFOR@LNTINFOTECH.COM",
        "grid_value": 4,
        "secured": "false"
    },
    {
        "field_id": "snow_account",
        "field_label": "Snow account",
        "field_mandatory": "yes",
        "field_placeholder": "Snow Account",
        "field_type": "hidden",
        "field_value": "fya62509.us-east-1",
        "grid_value": 4,
        "secured": "false"
    },
    {
        "field_id": "snow_password",
        "field_label": "Snow password",
        "field_mandatory": "yes",
        "field_placeholder": "Snow Password",
        "field_type": "hidden",
        "field_value": "Password321",
        "grid_value": 4,
        "secured": "true"
    },
    {
        "field_id": "current_table_name",
        "field_label": "Current table name",
        "field_mandatory": "yes",
        "field_placeholder": "Table",
        "field_type": "hidden",
        "field_value": "SCB_DRIFT_CUR",
        "grid_value": 4,
        "secured": "false"
    },
    {
        "field_id": "reference_table_name",
        "field_label": "Reference table name",
        "field_mandatory": "yes",
        "field_placeholder": "Table",
        "field_type": "hidden",
        "field_value": "SCB_DRIFT_REF",
        "grid_value": 4,
        "secured": "false"
    }
]'''
    basic_details = '''[
    {
        "field_id": "drift_type",
        "field_label": "Drift type",
        "field_mandatory": "yes",
        "field_type": "hidden",
    "field_value": "prediction_drift",
        "refract_source": ""
    },
    {
        "field_id": "data_type",
        "field_label": "Data type",
        "field_mandatory": "yes",
        "field_options": [
            "tabular"
        ],
        "field_type": "select",
        "field_value": "tabular",
        "grid_value": 12,
        "refract_source": ""
    },
    {
        "field_id": "problem_type",
        "field_label": "Problem type",
        "field_mandatory": "yes",
        "field_options": [
            "regression",
            "binary_classification",
            "multiclass_classification"
        ],
        "field_type": "select",
        "field_value": "binary_classification",
        "grid_value": 12,
        "refract_source": ""
    },
    {
        "field_id": "default_container_size",
        "field_label": "Default container size",
        "field_mandatory": "yes",
        "field_name": "Medium ( CPU: 2, Mem: 4Gi )",
        "field_options": "",
        "field_placeholder": "container size",
        "field_type": "selectapi",
        "field_value": "cb1a459e-502a-45a6-b42f-ff5da2d9d1e7",
        "grid_value": 12,
        "refract_source": ""
    },
    {
        "field_id": "data_source",
        "field_label": "Data source",
        "field_mandatory": "yes",
        "field_options": [
            "Refract",
            "Snowflake"
        ],
        "field_type": "select",
        "field_value": "Refract",
        "grid_value": 12,
        "refract_source": ""
    }
]'''
    data_configs = '''[
    {
        "field_id": "prediction_col_name",
        "field_label": "Prediction column name",
        "field_mandatory": "yes",
        "field_placeholder": "prediction column name",
        "field_type": "text",
        "field_value": "PREDICTION",
        "grid_value": 6,
        "secured": "false"
    },
    {
        "field_id": "target_col_name",
        "field_label": "Target column name",
        "field_mandatory": "yes",
        "field_placeholder": "target column name",
        "field_type": "text",
        "field_value": "LOAN_STATUS",
        "grid_value": 6,
        "secured": "false"
    }
]'''
    reference_data_info = '''[
    {
        "field_id": "reference_data_path",
        "field_info": "Select file from data section",
        "field_label": "Reference data path",
        "field_mandatory": "yes",
        "field_name": "",
        "field_options": "",
        "field_placeholder": "reference path...",
        "field_type": "selectapi",
        "field_value": "reference.csv",
        "grid_value": 6,
        "refract_source": "",
        "secured": "false"
    }
]'''
    current_data_info = '''[
    {
        "field_id": "current_data_path",
        "field_info": "Select file from data section",
        "field_label": "Current data path",
        "field_mandatory": "yes",
        "field_name": "",
        "field_options": "",
        "field_placeholder": "current path...",
        "field_type": "selectapi",
        "field_value": "current.csv",
        "grid_value": 6,
        "refract_source": "",
        "secured": "false"
    }
]'''
    alert_configs = '''[
                    
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_options": [
                                "Drift Score"
                            ],
                            "field_type": "select",
                            "field_value": "Drift Score"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "1"
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_options": [
                                {
                                    "icon": "red",
                                    "label": "Red"
                                },
                                {
                                    "icon": "amber",
                                    "label": "Amber"
                                },
                                {
                                    "icon": "green",
                                    "label": "Green"
                                }
                            ],
                            "field_type": "select",
                            "field_value": "Green"
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_options": [
                                "Drift Score"
                            ],
                            "field_type": "select",
                            "field_value": "Drift Score"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "1"
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_options": [
                                {
                                    "icon": "red",
                                    "label": "Red"
                                },
                                {
                                    "icon": "amber",
                                    "label": "Amber"
                                },
                                {
                                    "icon": "green",
                                    "label": "Green"
                                }
                            ],
                            "field_type": "select",
                            "field_value": "Amber"
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_options": [
                                "Drift Score"
                            ],
                            "field_type": "select",
                            "field_value": "Drift Score"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "1"
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_options": [
                                {
                                    "icon": "red",
                                    "label": "Red"
                                },
                                {
                                    "icon": "amber",
                                    "label": "Amber"
                                },
                                {
                                    "icon": "green",
                                    "label": "Green"
                                }
                            ],
                            "field_type": "select",
                            "field_value": "Green"
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "F1 Score",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ]
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.3"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Green",
                            "field_options": [
                                {
                                    "label": "Red",
                                    "icon": "red"
                                },
                                {
                                    "label": "Amber",
                                    "icon": "amber"
                                },
                                {
                                    "label": "Green",
                                    "icon": "green"
                                }
                            ]
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Recall",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ]
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.3"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Green",
                            "field_options": [
                                {
                                    "label": "Red",
                                    "icon": "red"
                                },
                                {
                                    "label": "Amber",
                                    "icon": "amber"
                                },
                                {
                                    "label": "Green",
                                    "icon": "green"
                                }
                            ]
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Precision",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ]
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.3"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Green",
                            "field_options": [
                                {
                                    "label": "Red",
                                    "icon": "red"
                                },
                                {
                                    "label": "Amber",
                                    "icon": "amber"
                                },
                                {
                                    "label": "Green",
                                    "icon": "green"
                                }
                            ]
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Accuracy",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ]
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.3"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Green",
                            "field_options": [
                                {
                                    "label": "Red",
                                    "icon": "red"
                                },
                                {
                                    "label": "Amber",
                                    "icon": "amber"
                                },
                                {
                                    "label": "Green",
                                    "icon": "green"
                                }
                            ]
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "F1 Score",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ]
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.1"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Amber",
                            "field_options": [
                                {
                                    "label": "Red",
                                    "icon": "red"
                                },
                                {
                                    "label": "Amber",
                                    "icon": "amber"
                                },
                                {
                                    "label": "Green",
                                    "icon": "green"
                                }
                            ]
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Recall",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ]
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.1"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Amber",
                            "field_options": [
                                {
                                    "label": "Red",
                                    "icon": "red"
                                },
                                {
                                    "label": "Amber",
                                    "icon": "amber"
                                },
                                {
                                    "label": "Green",
                                    "icon": "green"
                                }
                            ]
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Precision",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ]
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.1"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Amber",
                            "field_options": [
                                {
                                    "label": "Red",
                                    "icon": "red"
                                },
                                {
                                    "label": "Amber",
                                    "icon": "amber"
                                },
                                {
                                    "label": "Green",
                                    "icon": "green"
                                }
                            ]
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Accuracy",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ]
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.1"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_type": "select",
                            "field_value": "Amber",
                            "field_options": [
                                {
                                    "label": "Red",
                                    "icon": "red"
                                },
                                {
                                    "label": "Amber",
                                    "icon": "amber"
                                },
                                {
                                    "label": "Green",
                                    "icon": "green"
                                }
                            ]
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ],
                            "field_type": "select",
                            "field_value": "F1 Score"
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.2"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_options": [
                                {
                                    "icon": "red",
                                    "label": "Red"
                                },
                                {
                                    "icon": "amber",
                                    "label": "Amber"
                                },
                                {
                                    "icon": "green",
                                    "label": "Green"
                                }
                            ],
                            "field_type": "select",
                            "field_value": "Red"
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ],
                            "field_type": "select",
                            "field_value": "Recall"
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.2"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_options": [
                                {
                                    "icon": "red",
                                    "label": "Red"
                                },
                                {
                                    "icon": "amber",
                                    "label": "Amber"
                                },
                                {
                                    "icon": "green",
                                    "label": "Green"
                                }
                            ],
                            "field_type": "select",
                            "field_value": "Red"
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ],
                            "field_type": "select",
                            "field_value": "Precision"
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.2"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_options": [
                                {
                                    "icon": "red",
                                    "label": "Red"
                                },
                                {
                                    "icon": "amber",
                                    "label": "Amber"
                                },
                                {
                                    "icon": "green",
                                    "label": "Green"
                                }
                            ],
                            "field_type": "select",
                            "field_value": "Red"
                        }
                    ],
                    [
                        {
                            "field_id": "parameter",
                            "field_label": "Parameter",
                            "field_mandatory": "yes",
                            "field_options": [
                                "Accuracy",
                                "Precision",
                                "Recall",
                                "F1 Score"
                            ],
                            "field_type": "select",
                            "field_value": "Accuracy"
                        },
                        {
                            "field_id": "min_threshold",
                            "field_label": "Min. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0"
                        },
                        {
                            "field_id": "max_threshold",
                            "field_label": "Max. threshold",
                            "field_mandatory": "yes",
                            "field_type": "number",
                            "field_value": "0.2"
                        },
                        {
                            "field_id": "severity",
                            "field_label": "Severity",
                            "field_mandatory": "yes",
                            "field_options": [
                                {
                                    "icon": "red",
                                    "label": "Red"
                                },
                                {
                                    "icon": "amber",
                                    "label": "Amber"
                                },
                                {
                                    "icon": "green",
                                    "label": "Green"
                                }
                            ],
                            "field_type": "select",
                            "field_value": "Red"
                        }
                    ]
                ]'''
    advanced_settings = '''{
                    "categorical_features": [
                        {
                            "field_id": "categorical_features",
                            "field_label": "Feature list",
                            "field_mandatory": "yes",
                            "field_placeholder": "Feature List",
                            "field_type": "text",
                            "field_value": "auto",
                            "grid_value": 4,
                            "secured": "false"
                        },
                        {
                            "field_id": "categorical_features_stattest",
                            "field_label": "Test",
                            "field_mandatory": "yes",
                            "field_options": [
                                "auto",
                                "chisquare",
                                "fisher_exact",
                                "g_test",
                                "hellinger_distance",
                                "jensenshannon",
                                "kl_divergence",
                                "psi"
                            ],
                            "field_type": "select",
                            "field_value": "auto",
                            "grid_value": 4
                        },
                        {
                            "field_id": "categorical_features_threshold",
                            "field_label": "Threshold",
                            "field_mandatory": "yes",
                            "field_placeholder": "Threshold",
                            "field_type": "text",
                            "field_value": "auto",
                            "grid_value": 4,
                            "secured": "false"
                        }
                    ],
                    "numerical_features": [
                        {
                            "field_id": "numerical_features",
                            "field_label": "Feature list",
                            "field_mandatory": "yes",
                            "field_placeholder": "List",
                            "field_type": "text",
                            "field_value": "auto",
                            "grid_value": 4,
                            "secured": "false"
                        },
                        {
                            "field_id": "numerical_features_stattest",
                            "field_label": "Test",
                            "field_mandatory": "yes",
                            "field_options": [
                                "auto",
                                "anderson",
                                "cramer_von_mises",
                                "energy_distance",
                                "epps_singleton",
                                "hellinger_distance",
                                "jensenshannon",
                                "kl_divergence",
                                "ks",
                                "mann_whitney_urank",
                                "psi",
                                "t_test",
                                "total_variation_distance",
                                "wasserstein_distance_norm",
                                "z_stattest"
                            ],
                            "field_type": "select",
                            "field_value": "auto",
                            "grid_value": 4
                        },
                        {
                            "field_id": "numerical_features_threshold",
                            "field_label": "Threshold",
                            "field_mandatory": "yes",
                            "field_placeholder": "Threshold",
                            "field_type": "text",
                            "field_value": "auto",
                            "grid_value": 4,
                            "secured": "false"
                        }
                    ]
                }'''
    os.environ["advanced_settings"]=advanced_settings
    os.environ["alert_configuration"] = alert_configs
    os.environ["reference_dataset"]=reference_data_info
    os.environ["current_dataset"] = current_data_info
    os.environ["data_configuration"] = data_configs
    os.environ['basic_details'] = basic_details
    os.environ['snowflake_configuration']=snowpark_configs
    os.environ["output_path"]=os.path.join(os.getcwd(),"Report_Dir")
    plugin = '''[
    {
        "field_id": "plugin_type",
        "field_label": "Plgin type",
        "field_mandatory": "yes",
        "field_type": "hidden",
    "field_value": "prediction_drift",
        "refract_source": ""
    }]'''
    os.environ["plugin"]  = plugin
    os.environ["prediction_col_name"]='["NOT_DEFAULT", "DEFAULT"]'


def remove_cache_files():
    for i in pathlib.Path(".").rglob("__pycache__"):
        print(i)
        shutil.rmtree(i)


if __name__ == "__main__" :
    remove_cache_files()
