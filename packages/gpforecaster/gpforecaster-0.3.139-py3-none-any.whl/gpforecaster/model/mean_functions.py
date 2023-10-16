import gpytorch
import torch


class PiecewiseLinearMean(gpytorch.means.Mean):
    def __init__(self, changepoints, device, k, m, b, random_init):
        super().__init__()
        self.device = device
        self.changepoints = changepoints
        if random_init:
            k = torch.rand(1).reshape((1, 1))
            m = torch.rand(1).reshape((1, 1))
            b = torch.rand(1)
        else:
            k = torch.tensor(k).reshape((1, 1))
            m = torch.tensor(m).reshape((1, 1))
            b = torch.tensor(b)
        self.register_parameter(name="k", parameter=torch.nn.Parameter(k))
        self.register_parameter(name="m", parameter=torch.nn.Parameter(m))
        self.register_parameter(
            name="b",
            parameter=torch.nn.Parameter(torch.tile(b, (len(changepoints),))),
        )

    def forward(self, x):
        x = x.to(device=self.device).float()
        A = (
            0.5
            * (
                1.0
                + torch.sgn(torch.tile(x.reshape((-1, 1)), (1, 4)) - self.changepoints)
            )
        ).float()

        b = self.b.to(device=self.device)
        k = self.k.to(device=self.device)
        m = self.m.to(device=self.device)

        res = (k + torch.matmul(A, b.reshape((-1, 1)))) * x + (
            m + torch.matmul(A, (-self.changepoints.float() * b))
        ).reshape(-1, 1)

        return res.reshape((-1,))


class ConstantMean(gpytorch.means.Mean):
    def __init__(self, constant=0.0):
        super().__init__()
        self.constant = torch.nn.Parameter(torch.tensor([constant]))

    def forward(self, x):
        return self.constant.expand(x.size(0))


class ZeroMean(gpytorch.means.Mean):
    def forward(self, x):
        res = torch.zeros_like(x)
        return res.reshape((-1,))
