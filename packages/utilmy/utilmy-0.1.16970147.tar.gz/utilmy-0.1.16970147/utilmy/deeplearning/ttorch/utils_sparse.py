
"""

The use of sparse Linear layer does reduce the number of parameters, but it will occupy more memory to maintain sparse matrices unless there is a more efficient way to store sparse matrices.

SparesModelForTorch
SparseLinear and other purning method using torch_sparse

Features
SparseLinear.py:
Torch_sparse library is used to implement the Linear Layer of sparse matrix, which can save memory cost and speed up the calculation in theory.




sparse layer and sparse gradient

https://medium.com/nvidia-merlin/training-larger-and-faster-recommender-systems-with-pytorch-sparse-embeddings-53348a2cde3f






"""


import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm
### SPARSE TENSOR

class Net(nn.Module):
    def __init__(self, input_dim=150):
        super(Net, self).__init__()


        # Sparse weight initialization with zeros
        Xempty = torch.sparse_coo_tensor(torch.tensor([[0,], [input_dim-1]]),
                                         torch.tensor([0.0]),
                                         torch.Size([53, input_dim]))
        self.fc1_weight = nn.Parameter(Xempty)


        self.fc2 = nn.Linear(53, 17)
        self.fc3 = nn.Linear(17, 2)
        nn.init.xavier_uniform_(self.fc2.weight)
        nn.init.xavier_uniform_(self.fc3.weight)


    def forward(self, x):
        iref, jref = self.fc1_weight.data.coalesce().indices()  # Existing weights
        imax, jmax = self.fc1_weight.data.size()
        print(iref, jref)

        new_indices = []
        new_values = []
        xind = x.coalesce().indices()

        for i, j in zip(xind[0], xind[1]):
            if (i, j) not in zip(iref, jref):
                # New input (i,j) values: Randomized the weight for (i,j)
                random_value_2d = torch.rand(1, device=x.device)  # Ensure the random tensor is on the same device as x
                new_values.append(random_value_2d.item())
                new_indices.append([i, j])

                if i > imax:
                    imax = i  # input batch size
                if j > jmax:
                    jmax = j  # should not be changed: physical input wide size

        if new_indices:  # If there are any new indices
            new_indices_tensor = torch.tensor(new_indices, device=x.device).t()  # Ensure new_indices is on the same device as x
            self.fc1_weight.data += torch.sparse_coo_tensor(new_indices_tensor,
                                                            torch.tensor(new_values, device=x.device),
                                                            (imax, jmax))

        x = F.relu(torch.sparse.mm(x.float(), self.fc1_weight.float().t()))

        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        return F.log_softmax(x, dim=1)


# Testing the Net
def test():
    n_dim = 15* 10**7

    net = Net(input_dim= n_dim)
    print(net.fc1_weight)



    X1 = torch.sparse_coo_tensor(torch.tensor([[0, 1, 2, 3], [10, 20, 30, 40]]),
                                torch.tensor([1, 2, 3, 4]), torch.Size([4, n_dim]))
    out1 = net(X1)
    print(out1)

    X2 = torch.sparse_coo_tensor(torch.tensor([[0, 1, 2, 3], [50, 60, 70, 80]]),
                                torch.tensor([1, 2, 3, 4]), torch.Size([4, n_dim]))
    out2 = net(X2)


    X3 = torch.sparse_coo_tensor(torch.tensor([[0, 1, 2, 3], [10, 20, 700, 800]]),
                                torch.tensor([1, 2, 3, 4]), torch.Size([4, n_dim]))
    out3 = net(X3)
    print(out3)

test()



import torch.nn as nn
import torch
import torch_sparse


class SparseLinearFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, sparse_weight_indices, sparse_weight_values, bias, m, n):
        y = torch_sparse.spmm(sparse_weight_indices, sparse_weight_values, m, n, x).T
        if len(bias) > 0:
            y += bias.unsqueeze(0).expand_as(y)

        ctx.save_for_backward(x, sparse_weight_indices, sparse_weight_values, torch.tensor(m), torch.tensor(n), bias)
        return y

    @staticmethod
    def backward(ctx, grad_output):
        x, sparse_weight_indices, sparse_weight_values, m, n, bias = ctx.saved_tensors
        grad_weight = grad_bias = None

        if ctx.needs_input_grad[2]:
            grad_weight = grad_output.t().mm(x.t())
            grad_weight = grad_weight[sparse_weight_indices[0], sparse_weight_indices[1]]

        if len(bias) > 0 and ctx.needs_input_grad[3]:
            grad_bias = grad_output.sum(0).squeeze(0)

        return None, None, grad_weight, grad_bias, None, None


class SparseLinear(nn.Module):
    def __init__(self, weight, bias, device=None, dtype=None):
        super(SparseLinear, self).__init__()
        self.in_features = weight.size(1)
        self.out_features = weight.size(0)

        self.sparse_weight_indices = torch.nn.Parameter(weight.to_sparse().indices(), requires_grad=False)
        self.register_parameter("sparse_weight_indices", self.sparse_weight_indices)

        self.sparse_weight_values = torch.nn.Parameter(weight.to_sparse().values())
        self.register_parameter("sparse_weight_values", self.sparse_weight_values)

        if bias is not False:
            self.bias = torch.nn.Parameter(bias)
            self.register_parameter('bias', self.bias)
        else:
            self.bias = None

    def forward(self, x):
        if len(x.shape) is 3:
            result = None
            for single_batch in x:
                if result is not None:
                    result = result.cat(SparseLinearFunction.apply(single_batch.T, self.sparse_weight_indices,
                                                                   self.sparse_weight_values, self.bias,
                                                                   self.out_features, self.in_features), dim=0)
                else:
                    result = SparseLinearFunction.apply(single_batch.T, self.sparse_weight_indices,
                                                        self.sparse_weight_values, self.bias,
                                                        self.out_features, self.in_features).unsqueeze(0)
            return result
        else:
            return SparseLinearFunction.apply(x.T, self.sparse_weight_indices, self.sparse_weight_values, self.bias,
                                              self.out_features, self.in_features)

    def extra_repr(self):
        return 'input_features={}, output_features={}, bias={}, sparsity={}'.format(
            self.in_features, self.out_features,
            len(self.bias) > 0, round(len(self.sparse_weight_values)/(self.in_features * self.out_features), 2))













"""
Toools for Sparse torch

https://github.com/yoongi0428/RecSys_PyTorch/blob/master/models/LightGCN.py


LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation, 
Xiangnan He et al.,
SIGIR 2020.
"""
import os
import math
import time

import numpy as np
import scipy.sparse as sp
import torch
import torch.nn as nn
import torch.nn.functional as F

from .BaseModel import BaseModel
from data.generators import PairwiseGenerator

class LightGCN(BaseModel):
    def __init__(self, dataset, hparams, device):
        super(LightGCN, self).__init__()
        self.data_name = dataset.dataname
        self.num_users = dataset.num_users
        self.num_items = dataset.num_items

        self.emb_dim = hparams['emb_dim']
        self.num_layers = hparams['num_layers']
        self.node_dropout = hparams['node_dropout']

        self.split = hparams['split']
        self.num_folds = hparams['num_folds']

        self.reg = hparams['reg']
        
        self.Graph = None
        self.data_loader = None
        self.path = hparams['graph_dir']
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.device = device

        self.build_graph()

        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001)

    def build_graph(self):
        self.user_embedding = nn.Embedding(self.num_users, self.emb_dim)
        self.item_embedding = nn.Embedding(self.num_items, self.emb_dim)
        nn.init.normal_(self.user_embedding.weight, 0, 0.01)
        nn.init.normal_(self.item_embedding.weight, 0, 0.01)

        self.user_embedding_pred = None
        self.item_embedding_pred = None

        self.to(self.device)

    def update_lightgcn_embedding(self):
        self.user_embeddings, self.item_embeddings = self._lightgcn_embedding(self.Graph)
    
    def forward(self, user_ids, item_ids):
        user_emb = F.embedding(user_ids, self.user_embeddings)
        item_emb = F.embedding(item_ids, self.item_embeddings)
        
        pred_rating = torch.sum(torch.mul(user_emb, item_emb), 1)
        return pred_rating
    
    def fit(self, dataset, exp_config, evaluator=None, early_stop=None, loggers=None):
        train_matrix = dataset.train_data
        self.Graph = self.getSparseGraph(train_matrix)
        
        batch_generator = PairwiseGenerator(
                train_matrix, num_negatives=1, num_positives_per_user=1,
                batch_size=exp_config.batch_size, shuffle=True, device=self.device)

        num_batches = len(batch_generator)
        for epoch in range(1, exp_config.num_epochs + 1):
            self.train()
            epoch_loss = 0.0
            
            for b, (batch_users, batch_pos, batch_neg) in enumerate(batch_generator):
                self.optimizer.zero_grad()

                batch_loss = self.process_one_batch(batch_users, batch_pos, batch_neg)
                batch_loss.backward()
                self.optimizer.step()

                epoch_loss += batch_loss

                if exp_config.verbose and b % 50 == 0:
                    print('(%3d / %3d) loss = %.4f' % (b, num_batches, batch_loss))
            
            epoch_summary = {'loss': epoch_loss}
            
            # Evaluate if necessary
            if evaluator is not None and epoch >= exp_config.test_from and epoch % exp_config.test_step == 0:
                scores = evaluator.evaluate(self)
                epoch_summary.update(scores)
                
                if loggers is not None:
                    for logger in loggers:
                        logger.log_metrics(epoch_summary, epoch=epoch)

                ## Check early stop
                if early_stop is not None:
                    is_update, should_stop = early_stop.step(scores, epoch)
                    if should_stop:
                        break
            else:
                if loggers is not None:
                    for logger in loggers:
                        logger.log_metrics(epoch_summary, epoch=epoch)

        best_score = early_stop.best_score if early_stop is not None else scores
        return {'scores': best_score}
    
    def process_one_batch(self, users, pos_items, neg_items):
        self.update_lightgcn_embedding()

        pos_scores = self.forward(users, pos_items)
        neg_scores = self.forward(users, neg_items)
        loss = -F.sigmoid(pos_scores - neg_scores).log().mean()
        return loss

    def predict_batch_users(self, user_ids):
        user_embeddings = F.embedding(user_ids, self.user_embeddings)
        item_embeddings = self.item_embeddings
        return user_embeddings @ item_embeddings.T

    def predict(self, eval_users, eval_pos, test_batch_size):
        self.update_lightgcn_embedding()

        num_eval_users = len(eval_users)
        num_batches = int(np.ceil(num_eval_users / test_batch_size))
        pred_matrix = np.zeros(eval_pos.shape)
        perm = list(range(num_eval_users))
        with torch.no_grad():
            for b in range(num_batches):
                if (b + 1) * test_batch_size >= num_eval_users:
                    batch_idx = perm[b * test_batch_size:]
                else:
                    batch_idx = perm[b * test_batch_size: (b + 1) * test_batch_size]
                
                batch_users = eval_users[batch_idx]
                batch_users_torch = torch.LongTensor(batch_users).to(self.device)
                pred_matrix[batch_users] = self.predict_batch_users(batch_users_torch).detach().cpu().numpy()

        pred_matrix[eval_pos.nonzero()] = float('-inf')

        return pred_matrix
    

    ##################################### LightGCN Code
    def __dropout_x(self, x, keep_prob):
        size = x.size()
        index = x.indices().t()
        values = x.values()
        random_index = torch.rand(len(values)) + keep_prob
        random_index = random_index.int().bool()
        index = index[random_index]
        values = values[random_index]/keep_prob
        g = torch.sparse.FloatTensor(index.t(), values, size)
        return g
    
    def __dropout(self, keep_prob):
        if self.split:
            graph = []
            for g in self.Graph:
                graph.append(self.__dropout_x(g, keep_prob))
        else:
            graph = self.__dropout_x(self.Graph, keep_prob)
        return graph

    def _lightgcn_embedding(self, graph):
        users_emb = self.user_embedding.weight
        items_emb = self.item_embedding.weight
        all_emb = torch.cat([users_emb, items_emb])

        embs = [all_emb]
        if self.node_dropout > 0:
            if self.training:
                g_droped = self.__dropout(graph, self.node_dropout)
            else:
                g_droped = graph        
        else:
            g_droped = graph    
        
        for layer in range(self.num_layers):
            if self.split:
                temp_emb = []
                for f in range(len(g_droped)):
                    temp_emb.append(torch.sparse.mm(g_droped[f], all_emb))
                side_emb = torch.cat(temp_emb, dim=0)
                all_emb = side_emb
            else:
                all_emb = torch.sparse.mm(g_droped, all_emb)
            embs.append(all_emb)
        embs = torch.stack(embs, dim=1)
        
        light_out = torch.mean(embs, dim=1)
        users, items = torch.split(light_out, [self.num_users, self.num_items])
        return users, items

    def make_train_matrix(self):
        train_matrix_arr = self.dataset.train_matrix.toarray()
        self.train_matrix = sp.csr_matrix(train_matrix_arr)
    
    def _split_A_hat(self, A):
        A_fold = []
        fold_len = (self.num_users + self.num_items) // self.num_folds
        for i_fold in range(self.num_folds):
            start = i_fold*fold_len
            if i_fold == self.num_folds - 1:
                end = self.num_users + self.num_items
            else:
                end = (i_fold + 1) * fold_len
            A_fold.append(self._convert_sp_mat_to_sp_tensor(A[start:end]).coalesce().to(self.device))
        return A_fold

    def _convert_sp_mat_to_sp_tensor(self, X):
        coo = X.tocoo().astype(np.float32)
        row = torch.Tensor(coo.row).long()
        col = torch.Tensor(coo.col).long()
        index = torch.stack([row, col])
        data = torch.FloatTensor(coo.data)
        return torch.sparse.FloatTensor(index, data, torch.Size(coo.shape))
        
    def getSparseGraph(self, rating_matrix):
        n_users, n_items = rating_matrix.shape
        print("loading adjacency matrix")
        
        filename = f'{self.data_name}_s_pre_adj_mat.npz'
        try:
            pre_adj_mat = sp.load_npz(os.path.join(self.path, filename))
            print("successfully loaded...")
            norm_adj = pre_adj_mat
        except :
            print("generating adjacency matrix")
            s = time.time()
            adj_mat = sp.dok_matrix((n_users + n_items, n_users + n_items), dtype=np.float32)
            adj_mat = adj_mat.tolil()
            R = rating_matrix.tolil()
            adj_mat[:n_users, n_users:] = R
            adj_mat[n_users:, :n_users] = R.T
            adj_mat = adj_mat.todok()
            # adj_mat = adj_mat + sp.eye(adj_mat.shape[0])
            
            rowsum = np.array(adj_mat.sum(axis=1))
            d_inv = np.power(rowsum, -0.5).flatten()
            d_inv[np.isinf(d_inv)] = 0.
            d_mat = sp.diags(d_inv)
            
            norm_adj = d_mat.dot(adj_mat)
            norm_adj = norm_adj.dot(d_mat)
            norm_adj = norm_adj.tocsr()
            end = time.time()
            print(f"costing {end-s}s, saved norm_mat...")
            sp.save_npz(os.path.join(self.path, filename), norm_adj)

        if self.split == True:
            Graph = self._split_A_hat(norm_adj)
            print("done split matrix")
        else:
            Graph = self._convert_sp_mat_to_sp_tensor(norm_adj)
            Graph = Graph.coalesce().to(self.device)
            print("don't split the matrix")
        return Graph




"""
Neural Graph Collaborative Filtering,
Xiang Wang et al.,
SIGIR 2019.
[Official tensorflow]: https://github.com/xiangwang1223/neural_graph_collaborative_filtering
[PyTorch reference]: https://github.com/huangtinglin/NGCF-PyTorch
"""
import os
import math
import time

import numpy as np
import scipy.sparse as sp
import torch
import torch.nn as nn
import torch.nn.functional as F

from .BaseModel import BaseModel
from data.generators import PairwiseGenerator

class NGCF(BaseModel):
    def __init__(self, dataset, hparams, device):
        super(NGCF, self).__init__()
        self.data_name = dataset.dataname
        self.num_users = dataset.num_users
        self.num_items = dataset.num_items

        self.emb_dim = hparams['emb_dim']
        self.num_layers = hparams['num_layers']
        self.node_dropout = hparams['node_dropout']
        self.mess_dropout = hparams['mess_dropout']

        self.split = hparams['split']
        self.num_folds = hparams['num_folds']

        self.reg = hparams['reg']
        
        self.Graph = None
        self.data_loader = None
        self.path = hparams['graph_dir']
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.device = device

        self.build_graph()

        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001)

    def build_graph(self):
        self.user_embedding = nn.Embedding(self.num_users, self.emb_dim)
        self.item_embedding = nn.Embedding(self.num_items, self.emb_dim)
        nn.init.normal_(self.user_embedding.weight, 0, 0.01)
        nn.init.normal_(self.item_embedding.weight, 0, 0.01)

        self.weight_dict = nn.ParameterDict()
        layers = [self.emb_dim] * (self.num_layers + 1)
        for k in range(len(layers)-1):
            self.weight_dict.update({'W_gc_%d'%k: nn.Parameter(nn.init.normal_(torch.empty(layers[k], layers[k+1])))})
            self.weight_dict.update({'b_gc_%d'%k: nn.Parameter(nn.init.normal_(torch.empty(1, layers[k+1])))})

            self.weight_dict.update({'W_bi_%d'%k: nn.Parameter(nn.init.normal_(torch.empty(layers[k], layers[k+1])))})
            self.weight_dict.update({'b_bi_%d'%k: nn.Parameter(nn.init.normal_(torch.empty(1, layers[k+1])))})

        self.to(self.device)

    def update_ngcf_embedding(self):
        self.user_embeddings, self.item_embeddings = self._ngcf_embedding(self.Graph)
    
    def forward(self, user_ids, item_ids):
        user_emb = F.embedding(user_ids, self.user_embeddings)
        item_emb = F.embedding(item_ids, self.item_embeddings)
        
        pred_rating = torch.sum(torch.mul(user_emb, item_emb), 1)
        return pred_rating
    
    def fit(self, dataset, exp_config, evaluator=None, early_stop=None, loggers=None):
        train_matrix = dataset.train_data
        self.Graph = self.getSparseGraph(train_matrix)
        
        batch_generator = PairwiseGenerator(
                train_matrix, num_negatives=1, num_positives_per_user=1,
                batch_size=exp_config.batch_size, shuffle=True, device=self.device)

        num_batches = len(batch_generator)
        for epoch in range(1, exp_config.num_epochs + 1):
            self.train()
            epoch_loss = 0.0

            for b, (batch_users, batch_pos, batch_neg) in enumerate(batch_generator):
                self.optimizer.zero_grad()

                batch_loss = self.process_one_batch(batch_users, batch_pos, batch_neg)
                batch_loss.backward()
                self.optimizer.step()

                epoch_loss += batch_loss

                if exp_config.verbose and b % 50 == 0:
                    print('(%3d / %3d) loss = %.4f' % (b, num_batches, batch_loss))
            
            epoch_summary = {'loss': epoch_loss}
            
            # Evaluate if necessary
            if evaluator is not None and epoch >= exp_config.test_from and epoch % exp_config.test_step == 0:
                scores = evaluator.evaluate(self)
                epoch_summary.update(scores)
                
                if loggers is not None:
                    for logger in loggers:
                        logger.log_metrics(epoch_summary, epoch=epoch)

                ## Check early stop
                if early_stop is not None:
                    is_update, should_stop = early_stop.step(scores, epoch)
                    if should_stop:
                        break
            else:
                if loggers is not None:
                    for logger in loggers:
                        logger.log_metrics(epoch_summary, epoch=epoch)

        best_score = early_stop.best_score if early_stop is not None else scores
        return {'scores': best_score}
    
    def process_one_batch(self, users, pos_items, neg_items):
        self.update_ngcf_embedding()

        pos_scores = self.forward(users, pos_items)
        neg_scores = self.forward(users, neg_items)
        loss = -F.sigmoid(pos_scores - neg_scores).log().mean()
        return loss

    def predict_batch_users(self, user_ids):
        user_embeddings = F.embedding(user_ids, self.user_embeddings)
        item_embeddings = self.item_embeddings
        return user_embeddings @ item_embeddings.T

    def predict(self, eval_users, eval_pos, test_batch_size):
        self.update_ngcf_embedding()

        num_eval_users = len(eval_users)
        num_batches = int(np.ceil(num_eval_users / test_batch_size))
        pred_matrix = np.zeros(eval_pos.shape)
        perm = list(range(num_eval_users))
        with torch.no_grad():
            for b in range(num_batches):
                if (b + 1) * test_batch_size >= num_eval_users:
                    batch_idx = perm[b * test_batch_size:]
                else:
                    batch_idx = perm[b * test_batch_size: (b + 1) * test_batch_size]
                
                batch_users = eval_users[batch_idx]
                batch_users_torch = torch.LongTensor(batch_users).to(self.device)
                pred_matrix[batch_users] = self.predict_batch_users(batch_users_torch).detach().cpu().numpy()

        pred_matrix[eval_pos.nonzero()] = float('-inf')

        return pred_matrix

    ##################################### LightGCN Code
    def __dropout_x(self, x, keep_prob):
        size = x.size()
        index = x.indices().t()
        values = x.values()
        random_index = torch.rand(len(values)) + keep_prob
        random_index = random_index.int().bool()
        index = index[random_index]
        values = values[random_index]/keep_prob
        g = torch.sparse.FloatTensor(index.t(), values, size)
        return g
    
    def __dropout(self, keep_prob):
        if self.split:
            graph = []
            for g in self.Graph:
                graph.append(self.__dropout_x(g, keep_prob))
        else:
            graph = self.__dropout_x(self.Graph, keep_prob)
        return graph

    def _ngcf_embedding(self, graph):
        users_emb = self.user_embedding.weight
        items_emb = self.item_embedding.weight
        all_emb = torch.cat([users_emb, items_emb])

        embs = [all_emb]
        if self.node_dropout > 0:
            if self.training:
                g_droped = self.__dropout(graph, self.node_dropout)
            else:
                g_droped = graph        
        else:
            g_droped = graph    
        
        ego_emb = all_emb
        for k in range(self.num_layers):
            if self.split:
                temp_emb = []
                for f in range(len(g_droped)):
                    temp_emb.append(torch.sparse.mm(g_droped[f], ego_emb))
                side_emb = torch.cat(temp_emb, dim=0)
            else:
                side_emb = torch.sparse.mm(g_droped, ego_emb)
            
            sum_emb = torch.matmul(side_emb, self.weight_dict['W_gc_%d' % k]) + self.weight_dict['b_gc_%d' % k]
            
            bi_emb = torch.mul(ego_emb, side_emb)
            bi_emb = torch.matmul(bi_emb, self.weight_dict['W_bi_%d' % k]) + self.weight_dict['b_bi_%d' % k]

            ego_emb = F.leaky_relu(sum_emb + bi_emb, negative_slope=0.2)
            ego_emb = F.dropout(ego_emb, self.mess_dropout, training=self.training)
            
            norm_emb = F.normalize(ego_emb, p=2, dim=1)
            embs += [norm_emb]

        embs = torch.stack(embs, dim=1)
        
        ngcf_out = torch.mean(embs, dim=1)
        users, items = torch.split(ngcf_out, [self.num_users, self.num_items])
        return users, items
    
    def _split_A_hat(self, A):
        A_fold = []
        fold_len = (self.num_users + self.num_items) // self.num_folds
        for i_fold in range(self.num_folds):
            start = i_fold*fold_len
            if i_fold == self.num_folds - 1:
                end = self.num_users + self.num_items
            else:
                end = (i_fold + 1) * fold_len
            A_fold.append(self._convert_sp_mat_to_sp_tensor(A[start:end]).coalesce().to(self.device))
        return A_fold

    def _convert_sp_mat_to_sp_tensor(self, X):
        coo = X.tocoo().astype(np.float32)
        row = torch.Tensor(coo.row).long()
        col = torch.Tensor(coo.col).long()
        index = torch.stack([row, col])
        data = torch.FloatTensor(coo.data)
        return torch.sparse.FloatTensor(index, data, torch.Size(coo.shape))
        
    def getSparseGraph(self, rating_matrix):
        n_users, n_items = rating_matrix.shape
        print("loading adjacency matrix")
        
        filename = f'{self.data_name}_s_pre_adj_mat.npz'
        try:
            pre_adj_mat = sp.load_npz(os.path.join(self.path, filename))
            print("successfully loaded...")
            norm_adj = pre_adj_mat
        except :
            print("generating adjacency matrix")
            s = time.time()
            adj_mat = sp.dok_matrix((n_users + n_items, n_users + n_items), dtype=np.float32)
            adj_mat = adj_mat.tolil()
            R = rating_matrix.tolil()
            adj_mat[:n_users, n_users:] = R
            adj_mat[n_users:, :n_users] = R.T
            adj_mat = adj_mat.todok()
            # adj_mat = adj_mat + sp.eye(adj_mat.shape[0])
            
            rowsum = np.array(adj_mat.sum(axis=1))
            d_inv = np.power(rowsum, -0.5).flatten()
            d_inv[np.isinf(d_inv)] = 0.
            d_mat = sp.diags(d_inv)
            
            norm_adj = d_mat.dot(adj_mat)
            norm_adj = norm_adj.dot(d_mat)
            norm_adj = norm_adj.tocsr()
            end = time.time()
            print(f"costing {end-s}s, saved norm_mat...")
            sp.save_npz(os.path.join(self.path, filename), norm_adj)

        if self.split == True:
            Graph = self._split_A_hat(norm_adj)
            print("done split matrix")
        else:
            Graph = self._convert_sp_mat_to_sp_tensor(norm_adj)
            Graph = Graph.coalesce().to(self.device)
            print("don't split the matrix")
        return Graph


