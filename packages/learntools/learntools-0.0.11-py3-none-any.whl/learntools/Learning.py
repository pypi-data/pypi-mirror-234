import numpy as np
from copy import deepcopy


def random_learning(
    net,
    loss_fun,
    max_its=1000,
    max_mutations=1000,
    step=1 / 2**5,
    threshold=1e-3,
    info=False,
):
    """
    returns loss over iterations,
    (iterations reached,total mutation attempts)
    """
    losses = [loss_fun(net)]
    total_k = 0

    for i in range(max_its):
        if info:
            print("Iter", i, "Loss", losses[-1])

        if losses[-1] < threshold:
            if info:
                print("Stopped Due to Threshold Reached")
            break

        for k in range(max_mutations):  # mutate so many times before giving up
            pertubations = random_mutate(net, step)
            loss = loss_fun(net)

            if loss < losses[-1]:
                losses.append(loss)
                break
            else:
                # pertubate in the opposite direction to save generating another pertubation
                undo_mutate(net, pertubations)
                undo_mutate(net, pertubations)

            loss = loss_fun(net)
            if loss < losses[-1]:
                losses.append(loss)
                break
            else:
                make_mutate(net, pertubations)

        total_k += k
        if k == max_mutations - 1:
            if info:
                print("Stopped Due to Max Mutations Reached")
            break

    return losses, (i, total_k)


def random_mutate(net, step: float):  # randomly mutate the network
    pertubations = []
    for index in net.mutateable_layers:
        w_shape = np.shape(net.layers[index].weights)
        b_shape = np.shape(net.layers[index].biases)

        w_pertubation = step * np.random.normal(size=w_shape)
        b_pertubation = step * np.random.normal(size=b_shape)

        pertubations.append([w_pertubation, b_pertubation])

        net.layers[index].weights += w_pertubation
        net.layers[index].biases += b_pertubation

    return pertubations


def undo_mutate(net, pertubations):
    i = 0
    for index in net.mutateable_layers:
        w_pertubation = pertubations[i][0]
        b_pertubation = pertubations[i][1]

        net.layers[index].weights -= w_pertubation
        net.layers[index].biases -= b_pertubation

        i += 1


def make_mutate(net, pertubations):
    i = 0
    for index in net.mutateable_layers:
        w_pertubation = pertubations[i][0]
        b_pertubation = pertubations[i][1]

        net.layers[index].weights += w_pertubation
        net.layers[index].biases += b_pertubation

        i += 1


def random_learning_momentum(
    net,
    loss_fun,
    max_its=1000,
    max_mutations=1000,
    step=1 / 2**5,
    threshold=1e-3,
    momentum=0,
    info=False,
):
    """
    returns loss over iterations,
    (iterations reached,total mutation attempts)
    """
    losses = [loss_fun(net)]
    total_k = 0

    velocity = None

    for i in range(max_its):
        if info:
            print("Iter", i, "Loss", losses[-1])

        if losses[-1] < threshold:
            if info:
                print("Stopped Due to Threshold Reached")
            break

        if i != 0:  # if not first run we have momentum from last pertubation
            make_mutate(net, [[momentum * w, momentum * b] for w, b in velocity])

        for k in range(max_mutations):  # mutate so many times before giving up
            pertubations = random_mutate(net, step)
            loss = loss_fun(net)

            if loss < losses[-1]:
                losses.append(loss)
                velocity = pertubations

                break
            else:
                # pertubate in the opposite direction to save generating another pertubation
                undo_mutate(net, pertubations)
                undo_mutate(net, pertubations)

            loss = loss_fun(net)
            if loss < losses[-1]:
                losses.append(loss)
                velocity = -pertubations
                break
            else:
                make_mutate(net, pertubations)

        total_k += k
        if k == max_mutations - 1:
            if info:
                print("Stopped Due to Max Mutations Reached")
            break

    return losses, (i, total_k)
