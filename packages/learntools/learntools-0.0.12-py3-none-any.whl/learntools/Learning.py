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

    return pertubations #make the inside arrays?


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

def p_add(p1,p2):
    '''
    adds p2 to the p1 pertubation
    '''
    for i in range(len(p1)):
        for j in range(len(p1[i])):
            p1[i][j] += p2[i][j]

    return p1

def p_multiply(p,n):
    '''
    multiplies pertubation by n
    '''
    for i in range(len(p)):
        for j in range(len(p[i])):
            p[i][j] = p[i][j] * n

    return p



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

    

    for i in range(max_its):
        if info:
            print("Iter", i, "Loss", losses[-1])

        if losses[-1] < threshold:
            if info:
                print("Stopped Due to Threshold Reached")
            break

        if i!= 0:
            velocity = p_multiply(old_pertubation,momentum)
            make_mutate(net, velocity)

        for k in range(max_mutations):  # mutate so many times before giving up
            pertubations = random_mutate(net, step)

            loss = loss_fun(net)

            if loss < losses[-1]:
                losses.append(loss)
                
                if i!=0:
                    old_pertubation = p_add(pertubations,velocity)
                else:
                    old_pertubation = pertubations

                break
            else:
                # pertubate in the opposite direction to save generating another pertubation
                undo_mutate(net, pertubations)
                undo_mutate(net, pertubations)

            loss = loss_fun(net)
            if loss < losses[-1]:
                losses.append(loss)
                if i!=0:
                    old_pertubation = p_add(p_multiply(pertubations,-1),velocity)
                else:
                    old_pertubation = p_multiply(pertubations,-1)

                
                break
            else:
                make_mutate(net, pertubations)

        total_k += k
        if k == max_mutations - 1:
            if info:
                print("Stopped Due to Max Mutations Reached")
            break

    return losses, (i, total_k)
