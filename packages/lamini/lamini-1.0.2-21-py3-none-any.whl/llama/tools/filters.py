from random import Random
from llama.program.util.run_ai import query_run_embedding
from llama.program.util.run_ai import fuzzy_is_duplicate, get_closest_embedding
from collections import defaultdict
from random import sample
from copy import deepcopy
from tqdm import tqdm
from math import log


def get_attributes(value):
    return [
        attribute
        for attribute, _ in value.__fields__.items()
    ]


def type_to_string(type):
    attributes = get_attributes(type)
    return ' '.join([type[attribute] for attribute in attributes])


# TODO: add flag for deduping input and output, rather than just input
def dedupe(dataset, mode='exact', config={}):
    if mode == 'exact':
        threshold = 1.0
    elif mode == 'minimal':
        threshold = 0.99
    else: # mode == 'aggressive'
        threshold = 0.9
    deduper = DedupeFilter(dataset, config=config)
    return deduper.full_dedupe_dataset(threshold)


# TODO: add flag for deduping input and output, rather than just input
def dedupe_with_indices(dataset, mode='exact', config={}):
    if mode == 'exact':
        threshold = 1.0
    elif mode == 'minimal':
        threshold = 0.99
    else: # mode == 'aggressive'
        threshold = 0.9
    deduper = DedupeFilter(dataset, config=config)
    deduper.full_dedupe_dataset(threshold)
    return deduper.kept_indices


class DedupeFilter:
    """Dedupe your dataset with embeddings"""

    def __init__(self, dataset, config={}):
        self.dataset = dataset
        self.kept_dataset = []
        self.kept_indices = []
        self.removed_dataset = []
        self.removed_indices = []
        self.index = []
        self.deduped_index = []
        self.config = config

    def get_inputs(self):
        if type(self.dataset[0]) is list:
            return [datum[0] for datum in self.dataset]
        return self.dataset

    def get_all_embeddings(self):
        dataset = [type_to_string(datum) for datum in self.get_inputs()]
        self.index = []
        for i in tqdm(range(0, len(dataset), 32), desc='Filtering with dedupe...'):
            # Get embeddings
            # print("Processing Embeddings: " + str(i) + " of " + str(len(dataset)))
            embeddings = query_run_embedding(dataset[i : i + 32], self.config)
            self.index.extend(embeddings)

        return self.index

    def stochastic_dedupe_dataset(self, sample_size=None, threshold=0.99):
        if not sample_size:
            sample_size = int(log(len(self.dataset)))
        self.deduped_index = []
        self.kept_indices = []
        self.kept_dataset = []
        index = self.get_all_embeddings()
        rand = Random()
        for i in range(len(self.dataset)):
            # print("Comparing: " + str(i) + " of " + str(len(self.dataset)))
            # print("Deduped Index: " + str(len(deduped_index)))
            # Get embeddings
            embedding = index[i]
            random_sample = rand.sample(
                self.deduped_index, min(sample_size, len(self.deduped_index))
            )
            if not fuzzy_is_duplicate(embedding, random_sample, threshold):
                # print("Adding: " + str(i) + " of " + str(len(self.dataset)))
                self.deduped_index.append(embedding)
                self.kept_indices.append(i)
                self.kept_dataset.append(self.dataset[i])
            else:
                self.removed_indices.append(i)
                self.removed_dataset.append(self.dataset[i])

        return self.kept_dataset

    def full_dedupe_dataset(self, threshold=0.99):
        self.deduped_index = []
        self.kept_indices = []
        self.kept_dataset = []
        index = self.get_all_embeddings()
        for i in range(len(self.dataset)):
            # print("Processing: " + str(i) + " of " + str(len(self.dataset)))
            # print("Deduped Index: " + str(len(deduped_index)))
            # Get embeddings
            embedding = index[i]
            if not fuzzy_is_duplicate(embedding, self.deduped_index, threshold):
                # print("Adding: " + str(i) + " of " + str(len(self.dataset)))
                self.deduped_index.append(embedding)
                self.kept_indices.append(i)
                self.kept_dataset.append(self.dataset[i])
            else:
                self.removed_indices.append(i)
                self.removed_dataset.append(self.dataset[i])

        return self.kept_dataset


def balance(dataset, field=None, mode='exact', n=None, config={}):
    if mode == 'exact':
        threshold = 1.0
    elif mode == 'minimal':
        threshold = 0.99
    else: # mode == 'aggressive'
        threshold = 0.9
    balancer = BalanceFilter(dataset, config=config)
    if not field:
        field = get_attributes(balancer.get_outputs()[0])[0]
    if not n:
        n = len(dataset)
    kept_dataset = balancer.balance_dataset(field, n, threshold)
    return kept_dataset


class BalanceFilter:
    """Balance your dataset with embeddings"""

    def __init__(self, dataset, config={}):
        self.dataset = dataset
        self.kept_dataset = []
        self.kept_indices = []
        self.removed_dataset = []
        self.removed_indices = []
        self.index = []
        self.deduped_index = []
        self.clusters = {}
        self.config = config

    def get_all_embeddings(self, attribute):
        dataset = [datum[attribute] for datum in self.get_outputs()]
        self.index = []
        for i in tqdm(range(0, len(dataset), 32), desc='Filtering with balance...'):
            # Get embeddings
            # print("Processing Embeddings: " + str(i) + " of " + str(len(dataset)))
            embeddings = query_run_embedding(dataset[i : i + 32], self.config)
            self.index.extend(embeddings)

        return self.index

    def get_outputs(self):
        if type(self.dataset[0]) is list:
            return [datum[-1] for datum in self.dataset]
        return self.dataset
    
    def update_clusters(self, i, threshold):
        embedding = self.index[i]
        if not fuzzy_is_duplicate(embedding, self.deduped_index, threshold):
            self.clusters[str(embedding)] = [i]
            self.deduped_index.append(embedding)
        else:
            cluster_embedding = get_closest_embedding(embedding, self.deduped_index)
            self.clusters[str(cluster_embedding)].append(i)

    def list_classes(self, data, attribute, threshold):
        # classes = defaultdict(list)
        # for i, datum in enumerate(data):
        #     classes[datum[attribute]].append(i)
        # return classes
        self.get_all_embeddings(attribute)
        for i in range(len(data)):
            self.update_clusters(i, threshold)
        return self.clusters
    
    # TODO: perturb data rather than duplicate exactly
    def augment_data(self, data_indices, num_copies):
        augmented_indices = data_indices
        while len(augmented_indices) < num_copies:
            augmented_indices.extend([deepcopy(datum) for datum in sample(data_indices, min(len(data_indices), num_copies - len(augmented_indices)))])
        return augmented_indices
    
    # TODO: allow for balancing on multiple attributes
    def balance_dataset(self, attribute, max_num_samples, threshold):
        classes = self.list_classes(self.get_outputs(), attribute, threshold)
        num_classes = len(classes)
        num_samples_per_class = max(max_num_samples // num_classes, 1)
        for class_name in classes:
            sampled_indices = sample(self.augment_data(classes[class_name], num_samples_per_class), len(classes[class_name]))
            self.kept_dataset.extend([self.dataset[i] for i in sampled_indices[:num_samples_per_class]])
            self.kept_indices.extend(sampled_indices[:num_samples_per_class])
            self.removed_dataset.extend([self.dataset[i] for i in sampled_indices[num_samples_per_class:]])
            self.removed_indices.extend(sampled_indices[num_samples_per_class:])
        return self.kept_dataset
