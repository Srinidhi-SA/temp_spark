import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


def get_layers_for_network_module(nnpt_params, task_type):
    layers = []
    layers_list = sorted(tuple(nnpt_params["hidden_layer_info"]))

    print "n_layers - ", len(layers_list)
    print "task_type - ", task_type
    print "layers_tuple - ", layers_list

    if task_type == "CLASSIFICATION":
        for val in layers_list:
            layer_dict = nnpt_params["hidden_layer_info"][val]
            layer_name = layer_dict["layer"]
            layer_units_ip = layer_dict["units_ip"]
            layer_units_op = layer_dict["units_op"]
            layer_bias = layer_dict["bias"]
            layer_activation = layer_dict["activation"]
            layer_batchnormalization = layer_dict["batchnormalization"]
            layer_dropout = layer_dict["dropout"]

            print "~"*50
            print "Layer ID - ", val
            print "Layer Name - ", layer_name
            print "~"*50

            if layer_name == "Linear":
                main_layer = nn.Linear(in_features = layer_units_ip, out_features = layer_units_op, bias = layer_bias)
                layers.append(main_layer)
                if layer_activation != None:
                    if layer_activation["name"] == "ELU":
                        activation = nn.ELU(alpha = layer_activation["alpha"], inplace = False)
                    if layer_activation["name"] == "Hardshrink":
                        activation = nn.Hardshrink(lambd = layer_activation["lambd"])
                    if layer_activation["name"] == "Hardtanh":
                        activation = nn.Hardtanh(min_val = layer_activation["min_val"], max_val = layer_activation["max_val"], inplace = False)
                    if layer_activation["name"] == "LeakyReLU":
                        activation = nn.LeakyReLU(negative_slope = layer_activation["negative_slope"], inplace = False)
                    if layer_activation["name"] == "LogSigmoid":
                        activation = nn.LogSigmoid()
                    if layer_activation["name"] == "MultiheadAttention":
                        activation = nn.MultiheadAttention(
                        embed_dim = layer_activation["embed_dim"],
                        num_heads = layer_activation["num_heads"],
                        dropout = layer_activation["dropout"],
                        bias = layer_activation["bias"],
                        add_bias_kv = layer_activation["add_bias_kv"],
                        add_zero_attn = layer_activation["add_zero_attn"],
                        kdim = layer_activation["kdim"],
                        vdim = layer_activation["vdim"]
                        )
                    if layer_activation["name"] == "PreLU":
                        activation = nn.PreLU(num_parameters = layer_activation["num_parameters"], init = layer_activation["init"])
                    if layer_activation["name"] == "ReLU":
                        activation = nn.ReLU()
                    if layer_activation["name"] == "ReLU6":
                        activation = nn.ReLU6()
                    if layer_activation["name"] == "RreLU":
                        activation = nn.RreLU(lower = layer_activation["lower"], upper = layer_activation["upper"], inplace = False)
                    if layer_activation["name"] == "SELU":
                        activation = nn.SELU()
                    if layer_activation["name"] == "CELU":
                        activation = nn.CELU(alpha = layer_activation["alpha"], inplace = False)
                    if layer_activation["name"] == "GELU":
                        activation = nn.GELU()
                    if layer_activation["name"] == "Sigmoid":
                        activation = nn.Sigmoid()
                    if layer_activation["name"] == "Softplus":
                        activation = nn.Softplus(beta = layer_activation["beta"], threshold = layer_activation["threshold"])
                    if layer_activation["name"] == "Softshrink":
                        activation = nn.Softshrink(lambd = layer_activation["lambd"])
                    if layer_activation["name"] == "Softsign":
                        activation = nn.Softsign()
                    if layer_activation["name"] == "Tanh":
                        activation = nn.Tanh()
                    if layer_activation["name"] == "Tanhshrink":
                        activation = nn.Tanhshrink()
                    if layer_activation["name"] == "Threshold":
                        activation = nn.Threshold(threshold = layer_activation["threshold"], value = layer_activation["value"])
                    if layer_activation["name"] == "Softmin":
                        activation = nn.Softmin(dim = layer_activation["dim"])
                    if layer_activation["name"] == "Softmax":
                        activation = nn.Softmax(dim = layer_activation["dim"])
                    if layer_activation["name"] == "Softmax2d":
                        activation = nn.Softmax2d()
                    if layer_activation["name"] == "LogSoftmax":
                        activation = nn.LogSoftmax(dim = layer_activation["dim"])
                    if layer_activation["name"] == "AdaptiveLogSoftmaxWithLoss":
                        activation = nn.AdaptiveLogSoftmaxWithLoss(n_classes = layer_activation["n_classes"], cutoffs = layer_activation["cutoffs"], div_value = layer_activation["div_value"], head_bias = layer_activation["head_bias"])

                    layers.append(activation)
                else:
                    pass

                if layer_batchnormalization != None:
                    if layer_batchnormalization["name"] == "BatchNorm1d":
                        batch_normalization = nn.BatchNorm1d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "BatchNorm2d":
                        batch_normalization = nn.BatchNorm2d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "BatchNorm3d":
                        batch_normalization = nn.BatchNorm3d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "SyncBatchNorm":
                        batch_normalization = nn.SyncBatchNorm(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"], process_group = layer_batchnormalization["process_group"])
                    if layer_batchnormalization["name"] == "InstanceNorm1d":
                        batch_normalization = nn.InstanceNorm1d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "InstanceNorm2d":
                        batch_normalization = nn.InstanceNorm2d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "InstanceNorm3d":
                        batch_normalization = nn.InstanceNorm3d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "GroupNorm":
                        batch_normalization = nn.GroupNorm(num_groups = layer_batchnormalization["num_groups"], num_channels = layer_batchnormalization["num_channels"], eps = layer_batchnormalization["eps"], affine = layer_batchnormalization["affine"])
                    if layer_batchnormalization["name"] == "LayerNorm":
                        batch_normalization = nn.LayerNorm(normalized_shape = layer_batchnormalization["normalized_shape"], eps = layer_batchnormalization["eps"], elementwise_affine = layer_batchnormalization["elementwise_affine"])
                    if layer_batchnormalization["name"] == "LocalResponseNorm":
                        batch_normalization = nn.LocalResponseNorm(size = layer_batchnormalization["size"], alpha = layer_batchnormalization["alpha"], beta = layer_batchnormalization["beta"], k = layer_batchnormalization["k"])

                    layers.append(batch_normalization)
                else:
                    pass

                if layer_dropout != None:
                    if layer_dropout["name"] == "Dropout":
                        dropout = nn.Dropout(p = layer_dropout["p"], inplace = False)
                    if layer_dropout["name"] == "Dropout2d":
                        dropout = nn.Dropout2d(p = layer_dropout["p"], inplace = False)
                    if layer_dropout["name"] == "Dropout3d":
                        dropout = nn.Dropout3d(p = layer_dropout["p"], inplace = False)
                    if layer_dropout["name"] == "AlphaDropout":
                        dropout = nn.AlphaDropout(p = layer_dropout["p"], inplace = False)

                    layers.append(dropout)
                else:
                    pass

        print "~"*50
        print "FINAL LAYERS FOR NETWORK - ", layers
        print "~"*50

    if task_type == "REGRESSION":
        for val in layers_list:
            layer_dict = nnpt_params["hidden_layer_info"][val]
            layer_name = layer_dict["layer"]
            layer_units_ip = layer_dict["units_ip"]
            layer_units_op = layer_dict["units_op"]
            layer_bias = layer_dict["bias"]
            layer_activation = layer_dict["activation"]
            layer_batchnormalization = layer_dict["batchnormalization"]
            layer_dropout = layer_dict["dropout"]

            print "~"*50
            print "Layer ID - ", val
            print "Layer Name - ", layer_name
            print "~"*50

            if layer_name == "Linear":
                main_layer = nn.Linear(in_features = layer_units_ip, out_features = layer_units_op, bias = layer_bias)
                layers.append(main_layer)
                if layer_activation != None:
                    if layer_activation["name"] == "ELU":
                        activation = nn.ELU(alpha = layer_activation["alpha"], inplace = False)
                    if layer_activation["name"] == "Hardshrink":
                        activation = nn.Hardshrink(lambd = layer_activation["lambd"])
                    if layer_activation["name"] == "Hardtanh":
                        activation = nn.Hardtanh(min_val = layer_activation["min_val"], max_val = layer_activation["max_val"], inplace = False)
                    if layer_activation["name"] == "LeakyReLU":
                        activation = nn.LeakyReLU(negative_slope = layer_activation["negative_slope"], inplace = False)
                    if layer_activation["name"] == "LogSigmoid":
                        activation = nn.LogSigmoid()
                    if layer_activation["name"] == "MultiheadAttention":
                        activation = nn.MultiheadAttention(
                        embed_dim = layer_activation["embed_dim"],
                        num_heads = layer_activation["num_heads"],
                        dropout = layer_activation["dropout"],
                        bias = layer_activation["bias"],
                        add_bias_kv = layer_activation["add_bias_kv"],
                        add_zero_attn = layer_activation["add_zero_attn"],
                        kdim = layer_activation["kdim"],
                        vdim = layer_activation["vdim"]
                        )
                    if layer_activation["name"] == "PreLU":
                        activation = nn.PreLU(num_parameters = layer_activation["num_parameters"], init = layer_activation["init"])
                    if layer_activation["name"] == "ReLU":
                        activation = nn.ReLU()
                    if layer_activation["name"] == "ReLU6":
                        activation = nn.ReLU6()
                    if layer_activation["name"] == "RreLU":
                        activation = nn.RreLU(lower = layer_activation["lower"], upper = layer_activation["upper"], inplace = False)
                    if layer_activation["name"] == "SELU":
                        activation = nn.SELU()
                    if layer_activation["name"] == "CELU":
                        activation = nn.CELU(alpha = layer_activation["alpha"], inplace = False)
                    if layer_activation["name"] == "GELU":
                        activation = nn.GELU()
                    if layer_activation["name"] == "Sigmoid":
                        activation = nn.Sigmoid()
                    if layer_activation["name"] == "Softplus":
                        activation = nn.Softplus(beta = layer_activation["beta"], threshold = layer_activation["threshold"])
                    if layer_activation["name"] == "Softshrink":
                        activation = nn.Softshrink(lambd = layer_activation["lambd"])
                    if layer_activation["name"] == "Softsign":
                        activation = nn.Softsign()
                    if layer_activation["name"] == "Tanh":
                        activation = nn.Tanh()
                    if layer_activation["name"] == "Tanhshrink":
                        activation = nn.Tanhshrink()
                    if layer_activation["name"] == "Threshold":
                        activation = nn.Threshold(threshold = layer_activation["threshold"], value = layer_activation["value"])
                    if layer_activation["name"] == "Softmin":
                        activation = nn.Softmin(dim = layer_activation["dim"])
                    if layer_activation["name"] == "Softmax":
                        activation = nn.Softmax(dim = layer_activation["dim"])
                    if layer_activation["name"] == "Softmax2d":
                        activation = nn.Softmax2d()
                    if layer_activation["name"] == "LogSoftmax":
                        activation = nn.LogSoftmax(dim = layer_activation["dim"])
                    if layer_activation["name"] == "AdaptiveLogSoftmaxWithLoss":
                        activation = nn.AdaptiveLogSoftmaxWithLoss(n_classes = layer_activation["n_classes"], cutoffs = layer_activation["cutoffs"], div_value = layer_activation["div_value"], head_bias = layer_activation["head_bias"])

                    layers.append(activation)
                else:
                    pass

                if layer_batchnormalization != None:
                    if layer_batchnormalization["name"] == "BatchNorm1d":
                        batch_normalization = nn.BatchNorm1d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "BatchNorm2d":
                        batch_normalization = nn.BatchNorm2d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "BatchNorm3d":
                        batch_normalization = nn.BatchNorm3d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "SyncBatchNorm":
                        batch_normalization = nn.SyncBatchNorm(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"], process_group = layer_batchnormalization["process_group"])
                    if layer_batchnormalization["name"] == "InstanceNorm1d":
                        batch_normalization = nn.InstanceNorm1d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "InstanceNorm2d":
                        batch_normalization = nn.InstanceNorm2d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "InstanceNorm3d":
                        batch_normalization = nn.InstanceNorm3d(num_features = layer_batchnormalization["num_features"], eps = layer_batchnormalization["eps"], momentum = layer_batchnormalization["momentum"], affine = layer_batchnormalization["affine"], track_running_stats = layer_batchnormalization["track_running_stats"])
                    if layer_batchnormalization["name"] == "GroupNorm":
                        batch_normalization = nn.GroupNorm(num_groups = layer_batchnormalization["num_groups"], num_channels = layer_batchnormalization["num_channels"], eps = layer_batchnormalization["eps"], affine = layer_batchnormalization["affine"])
                    if layer_batchnormalization["name"] == "LayerNorm":
                        batch_normalization = nn.LayerNorm(normalized_shape = layer_batchnormalization["normalized_shape"], eps = layer_batchnormalization["eps"], elementwise_affine = layer_batchnormalization["elementwise_affine"])
                    if layer_batchnormalization["name"] == "LocalResponseNorm":
                        batch_normalization = nn.LocalResponseNorm(size = layer_batchnormalization["size"], alpha = layer_batchnormalization["alpha"], beta = layer_batchnormalization["beta"], k = layer_batchnormalization["k"])

                    layers.append(batch_normalization)
                else:
                    pass

                if layer_dropout != None:
                    if layer_dropout["name"] == "Dropout":
                        dropout = nn.Dropout(p = layer_dropout["p"], inplace = False)
                    if layer_dropout["name"] == "Dropout2d":
                        dropout = nn.Dropout2d(p = layer_dropout["p"], inplace = False)
                    if layer_dropout["name"] == "Dropout3d":
                        dropout = nn.Dropout3d(p = layer_dropout["p"], inplace = False)
                    if layer_dropout["name"] == "AlphaDropout":
                        dropout = nn.AlphaDropout(p = layer_dropout["p"], inplace = False)

                    layers.append(dropout)
                else:
                    pass

    return layers


def get_other_pytorch_params(nnpt_params, task_type):
    loss_criterion_dict = nnpt_params["loss"]
    loss_name = loss_criterion_dict["loss"]

    optimizer_dict = nnpt_params["optimizer"]
    optimizer_name = optimizer_dict["optimizer"]

    batch_size = nnpt_params["batch_size"]
    number_of_epochs = nnpt_params["number_of_epochs"]

    if loss_name == "CrossEntropyLoss":
        loss_criterion = nn.CrossEntropyLoss(reduction = loss_criterion_dict["reduction"])
    if loss_name == "MSELoss":
        loss_criterion = nn.MSELoss(reduction = loss_criterion_dict["reduction"])


    # if optimizer_name == "Adam":
    #     optimizer_params = []
    #     for k,v in optimizer_dict:
    #         if optimizer_dict[k] == "optimizer":
    #             pass
    #         else:
    #             optimizer_params.append(k = v)


    other_params_dict = {}
    other_params_dict["number_of_epochs"] = number_of_epochs
    other_params_dict["batch_size"] = batch_size
    other_params_dict["loss_criterion"] = loss_criterion
    # other_params_dict["optimizer"] = optimizer_params



    return other_params_dict



def get_tensored_data(x_train, y_train, x_test, y_test):
    x_train = np.stack([x_train[col].values for col in x_train.columns], 1)
    x_train_tensored = torch.tensor(x_train, dtype=torch.float)

    # y_train = np.stack([y_train[col].values for col in y_train.columns], 1)
    y_train_tensored = torch.tensor(y_train, dtype=torch.float)

    x_test = np.stack([x_test[col].values for col in x_test.columns], 1)
    x_test_tensored = torch.tensor(x_test, dtype=torch.float)

    # y_test = np.stack([y_test[col].values for col in y_test.columns], 1)
    try:
        y_test_tensored = torch.tensor(y_test, dtype=torch.float)
    except:
        y_test_tensored = torch.tensor(y_test.values, dtype=torch.float)

    return x_train_tensored, y_train_tensored, x_test_tensored, y_test_tensored
