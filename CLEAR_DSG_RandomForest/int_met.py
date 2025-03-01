import numpy as np
import sklearn
import sklearn.cluster

# def calc_identity(exp1, exp2):
#     dis = np.linalg.norm(exp1-exp2, axis = 1)
#     total = dis.shape[0]
#     true = np.where(abs(dis)<1e-8)[0].shape[0]
#     score = (total-true)/total
#     return score*100

def calc_identity(exp1, exp2):
    # dis = np.array(exp1)==np.array(exp2)
    # dis = dis.all(axis = 1)
    dis = np.array([np.array_equal(exp1[i],exp2[i]) for i in range(len(exp1))])
    total = dis.shape[0]
    true = np.sum(dis)
    score = (total-true)/total
    return score*100, true, total


def calc_separability(x_test, exp):
    dissimilar_instances=len(x_test.drop_duplicates())
    similar_exps = 0
    for i in range(exp.shape[0]):
        for j in range(exp.shape[0]):
            if i == j:
                continue
            eq = np.array_equal(exp[i],exp[j])
            if eq:
                similar_exps += 1
    total = exp.shape[0]
    score = (dissimilar_instances-similar_exps)/dissimilar_instances
    return dissimilar_instances,similar_exps,score*100


def calc_stability(exp, labels):
    total = labels.shape[0]
    label_values = np.unique(labels)
    n_clusters = label_values.shape[0]
    init = np.array([[np.average(exp[np.where(labels == i)], axis = 0)] for i in label_values]).squeeze()
    ct = sklearn.cluster.KMeans(n_clusters = n_clusters, n_jobs=5, random_state=1, n_init=10, init = init)
    ct.fit(exp)
    error = np.sum(np.abs(labels-ct.labels_))
    if error/total > 0.5:
        error = total-error
    return error, total




# def calc_separability(x_test, exp):
#     #x_test = np.unique(x_test)
#     dissimilar_instances=len(np.unique(x_test))
#     print("dissimilar_instances ",dissimilar_instances)
#     similar_exps = 0
#     for i in range(exp.shape[0]):
#         for j in range(exp.shape[0]):
#             if i == j:
#                 continue
#             eq = np.array_equal(exp[i],exp[j])
#             if eq:
#                 similar_exps += 1
#     total = exp.shape[0]
#     #score = 100*abs(wrong)/total**2
#     return dissimilar_instances,similar_exps,total**2
