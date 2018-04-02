import numpy as np
import sympy as sp

X, Y, Z, LA = sp.symbols('X, Y, Z, LA')

class scheme():
    _name = 'generic'

    def __init__(self, Nx = 200):
        self._define_scheme()
        self.nv = self.v.shape[0]
        self.d = self.v.shape[1]
        self.M = np.zeros((self.nv, self.nv))
        self.iM = np.zeros((self.nv, self.nv))
        self.R = np.zeros((self.nv, self.nv))
        self.G = np.zeros((self.nv, self.nv), dtype = 'complex128')
        self.dG = np.zeros((self.nv, self.nv))

        self.vxi = np.linspace(0, 2*np.pi, Nx)
        self.vvp = np.zeros((self.nv*self.vxi.size,), dtype = 'complex128')

    def _define_scheme(self):
        pass

    def fix_parameters_generic(self):
        for i in range(self.nv):
            for j in range(self.nv):
                self.M[i, j] = self.P[i].subs({LA: self.la,
                                          X: self.v[j,min(0,self.d-1)],
                                          Y: self.v[i,min(1,self.d-1)],
                                          Z: self.v[i,min(2,self.d-1)]
                                          })
        self.iM[:] = np.linalg.inv(self.M)
        self.dG[:] = np.dot(self.iM, np.dot(self.R, self.M))

    def eigenvalues(self):
        for i in range(self.vxi.size):
            xi = self.vxi[i]
            for k in range(self.nv):
                self.G[k,:] = np.exp(-self.v[k,0]*1j*xi) * self.dG[k,:]
            self.vvp[self.nv*i:self.nv*(i+1)] = np.linalg.eig(self.G)[0]


class D1Q2(scheme):
    _name = 'D1Q2'

    def _define_scheme(self):
        self.v = np.array([[-1], [1]])
        self.P = sp.Matrix([1, LA*X])

        self.param = {'la': 1., 'c': 1., 's': 1.}
        self.p_model = [
            {
                'type': 'slider',
                'variable': 's',
                'description': r'relaxation parameter $s$',
                'value': self.param['s'],
                'min': 0.,
                'max': 2.,
                'step': 0.01,
                'readout_format': '4.2f',
            },
            {
                'type': 'slider',
                'variable': 'c',
                'description': r'equilibrium parameter $c$',
                'value': self.param['c'],
                'min': 0.,
                'max': 1.5,
                'step': 0.01,
                'readout_format': '4.2f',
            },
            {
                'type': 'slider',
                'variable': 'la',
                'description': r'scheme velocity $\lambda$',
                'value': self.param['la'],
                'min': 0.,
                'max': 1.5,
                'step': 0.01,
                'readout_format': '4.2f',
            },
        ]

    def compute_eqeq(self):
        c, la, s = self.param['c'], self.param['la'], self.param['s']
        d = (1./s-.5) * (la**2 - c**2)
        self.eqeq = """
Equivalent equation        du       du              d^2u
                           -- + {0:3.1f} -- ={1:8.1e} dt ---- + O(dt^2).
                           dt       dx              dx^2
        """.format(c, d)

    def fix_parameters(self, param):
        self.la = self.param['la'] = param['la']
        self.c = self.param['c'] = param['c']
        self.s = self.param['s'] = param['s']
        self.R[:] = np.array([[1,0], [self.s*self.c, 1-self.s]])
        self.fix_parameters_generic()

class D1Q3o(scheme):
    _name = 'D1Q3 (1)'

    def _define_scheme(self):
        self.v = np.array([[-1], [0], [1]])
        self.P = sp.Matrix([1, LA*X, LA**2*X**2/2])

        self.param = {'la': 1., 'ca': 1., 'sa': 1., 'cb': 1., 'sb': 1.}
        self.p_model = [
            {
                'type': 'slider',
                'variable': 'sa',
                'description': r'relaxation parameter $s_1$',
                'value': self.param['sa'],
                'min': 0.,
                'max': 2.,
                'step': 0.01,
                'readout_format': '4.2f',
            },
            {
                'type': 'slider',
                'variable': 'sb',
                'description': r'relaxation parameter $s_2$',
                'value': self.param['sb'],
                'min': 0.,
                'max': 2.,
                'step': 0.01,
                'readout_format': '4.2f',
            },
            {
                'type': 'slider',
                'variable': 'ca',
                'description': r'equilibrium parameter $c_1$',
                'value': self.param['ca'],
                'min': 0.,
                'max': 1.5,
                'step': 0.01,
                'readout_format': '4.2f',
            },
            {
                'type': 'slider',
                'variable': 'cb',
                'description': r'equilibrium parameter $c_2$',
                'value': self.param['cb'],
                'min': 0.,
                'max': 1.5,
                'step': 0.01,
                'readout_format': '4.2f',
            },
            {
                'type': 'slider',
                'variable': 'la',
                'description': r'scheme velocity $\lambda$',
                'value': self.param['la'],
                'min': 0.,
                'max': 1.5,
                'step': 0.01,
                'readout_format': '4.2f',
            },
        ]

    def compute_eqeq(self):
        ca, cb, la, sa, sb = self.param['ca'], self.param['cb'], self.param['la'], self.param['sa'], self.param['sb']
        d = (1./sa-.5) * (2*cb*la**2 - ca**2)
        sigmaa, sigmab = 1./sa-.5, 1./sb-.5
        e = la**2 * (1 - 12 * sigmab * sigmaa) + 2 * ca**2 * (1 - 12 * sigmaa**2) + 3 * cb * (4*sigmab*sigmaa + 8*sigmaa**2 - 1)
        self.eqeq = """
Equivalent equation        du       du              d^2u                d^3u
                           -- + {0:3.1f} -- ={1:8.1e} dt ---- +{2:8.1e} dt^2 ---- O(dt^3).
                           dt       dx              dx^2                dx^3
        """.format(ca, d, e)

        """
        dt^2 (d^3u/dx^3) ca/12 * (
        la**2 * (1 - 12 * sigmab * sigmaa) + 2 * ca**2 * (1 - 12 * sigmaa**2)
        + 3 * cb * (4*sigmab*sigmaa + 8*sigmaa**2 - 1)
        )
        """


    def fix_parameters(self, param):
        self.la = self.param['la'] = param['la']
        self.ca = self.param['ca'] = param['ca']
        self.cb = self.param['cb'] = param['cb']
        self.sa = self.param['sa'] = param['sa']
        self.sb = self.param['sb'] = param['sb']
        self.R[:] = np.array([[1,0,0], [self.sa*self.ca, 1-self.sa, 0], [self.sb*self.cb, 0, 1-self.sb]])
        self.fix_parameters_generic()


class D1Q3d(scheme):
    _name = 'D1Q3 (2)'

    def _define_scheme(self):
        self.v = np.array([[-1], [0], [1]])
        self.P = sp.Matrix([1, LA*X, LA**2*X**2/2])

        self.param = {'la': 1., 'c': 1., 's': 1.}
        self.p_model = [
            {
                'type': 'slider',
                'variable': 's',
                'description': r'relaxation parameter $s$',
                'value': self.param['s'],
                'min': 0.,
                'max': 2.,
                'step': 0.01,
                'readout_format': '4.2f',
            },
            {
                'type': 'slider',
                'variable': 'c',
                'description': r'equilibrium parameter $c$',
                'value': self.param['c'],
                'min': 0.,
                'max': 1.5,
                'step': 0.01,
                'readout_format': '4.2f',
            },
            {
                'type': 'slider',
                'variable': 'la',
                'description': r'scheme velocity $\lambda$',
                'value': self.param['la'],
                'min': 0.,
                'max': 1.5,
                'step': 0.01,
                'readout_format': '4.2f',
            },
        ]

    def compute_eqeq(self):
        c, la, s = self.param['c'], self.param['la'], self.param['s']
        d = (1./s-.5) * (la**2 - 2*c**2)
        self.eqeq = """
Equivalent equations       du   dv            dv       du                d^2u
                           -- + -- = O(dt^2), -- + {0:3.1f} --  = {1:8.1e} dt ---- + O(dt^2).
                           dt   dx            dt       dx                dx^2
        """.format(2*c, d)

    def fix_parameters(self, param):
        self.la = self.param['la'] = param['la']
        self.c = self.param['c'] = param['c']
        self.s = self.param['s'] = param['s']
        self.R[:] = np.array([[1,0,0], [0,1,0], [self.s*self.c, 0, 1-self.s]])
        self.fix_parameters_generic()
