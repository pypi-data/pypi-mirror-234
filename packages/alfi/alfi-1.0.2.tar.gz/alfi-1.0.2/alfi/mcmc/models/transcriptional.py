import tensorflow as tf
from tensorflow import math as tfm
from tensorflow_probability import distributions as tfd

from alfi.datasets import DataHolder
from alfi.utilities.tf import rotate, logit, logistic, LogisticNormal, inverse_positivity, \
    save_object
from alfi.configuration import MCMCConfiguration
from alfi.mcmc.parameter import Parameter
from alfi.mcmc.samplers import HMCSampler, LatentGPSampler, DelaySampler, GibbsSampler
from alfi.mcmc.samplers.mixed import MixedSampler
from alfi.mcmc.gp.gp_kernels import GPKernelSelector
from alfi.mcmc.models import MCMCLFM

import numpy as np
import pickle

PI = tf.constant(np.pi, dtype='float64')
f64 = np.float64


class TranscriptionRegulationLFM(MCMCLFM):
    """
    An updated version of the Metropolis-Hastings model from Titsias et al. (2012) using a mixed sampler
    """
    def __init__(self, data: DataHolder, options: MCMCConfiguration):
        super().__init__(data, options)
        self.N_p = data.t_discretised.shape[0]
        step_sizes = self.options.initial_step_sizes
        logistic_step_size = step_sizes['nuts'] if 'nuts' in step_sizes else 0.00001
        self.subsamplers = list()
        self.dtype = 'float64'
        # Kinetics
        # if options.kinetic_exponential:
        #     kinetic_transform = lambda x: tf.exp(logit(x))
        # else:
        kinetic_transform = logit

        basal_rate = Parameter(
            'basal',
            LogisticNormal(0.01, 30),
            tf.random.uniform((self.num_outputs, 1), 0.75, 0.85, dtype=self.dtype),
            transform=kinetic_transform
        )
        sensitivity = Parameter(
            'sensitivity',
            LogisticNormal(0.01, 30),
            tf.random.uniform((self.num_outputs, 1), 0.75, 0.85, dtype=self.dtype),
            transform=kinetic_transform
        )
        decay_rate = Parameter(
            'decay',
            LogisticNormal(0.01, 30),
            tf.random.uniform((self.num_outputs, 1), 0.75, 0.85, dtype=self.dtype),
            transform=kinetic_transform
        )
        kinetics = [basal_rate, decay_rate, sensitivity]

        # Add optional kinetic parameters
        if options.initial_conditions:
            self.initial_conditions = Parameter(
                'initial',
                LogisticNormal(0.01, 30),
                tf.random.uniform((self.num_outputs, 1), 0.75, 0.85, dtype=self.dtype),
                transform=kinetic_transform
            )
            kinetics.append(self.initial_conditions)
        if options.translation:
            self.protein_decay = Parameter(
                'protein_decay',
                LogisticNormal(0.1, 7),
                0.8 * tf.ones((self.num_tfs, 1), dtype=self.dtype),
                transform=logit
            )
            kinetics.append(self.protein_decay)

        kinetics_subsampler = HMCSampler(self.likelihood, kinetics, logistic_step_size)
        self.subsamplers.append(kinetics_subsampler)

        # Weights
        if options.weights:
            self.weights = Parameter(
                'w',
                LogisticNormal(f64(-2), f64(2)),
                logistic(1 * tf.ones((self.num_outputs, self.num_tfs), dtype=self.dtype))
            )
            self.weights_biases = Parameter(
                'w_0',
                LogisticNormal(f64(-0.8), f64(0.8)),
                logistic(0 * tf.ones(self.num_outputs, dtype=self.dtype))
            )
            weights = [self.weights, self.weights_biases]
            weights_subsampler = HMCSampler(self.likelihood, weights, logistic_step_size)
            self.subsamplers.append(weights_subsampler)

        # Latent function & GP hyperparameters
        self.kernel_selector = GPKernelSelector(data, options)
        kernel_initial = self.kernel_selector.initial_params()

        f_step_size = step_sizes['latents'] if 'latents' in step_sizes else 20
        latent_likelihood = self.tfs_likelihood if options.latent_data_present else None
        latents_initial = 0.3 * tf.ones((self.num_replicates, self.num_tfs, self.N_p), dtype=self.dtype)

        latents_initial = [latents_initial, *kernel_initial]

        latents = Parameter('latent', None, latents_initial)
        latents_sampler = LatentGPSampler(self.likelihood, latent_likelihood,
                                          latents, self.kernel_selector,
                                          f_step_size*tf.ones(self.N_p, dtype=self.dtype),
                                          kernel_exponential=options.kernel_exponential)

        self.subsamplers.append(latents_sampler)

        if options.delays:
            delay_prior = tfd.InverseGamma(f64(0.01), f64(0.01)) #TODO choose between these two
            delay_prior = tfd.Exponential(f64(0.3))
            delay = Parameter('delay', delay_prior,
                              0.6 * tf.ones(self.num_tfs, dtype=self.dtype))
            delay_sampler = DelaySampler(self.likelihood, delay, 0, 10)
            self.subsamplers.append(delay_sampler)
        σ2_f = None
        if not options.preprocessing_variance:
            def f_sq_diff_fn():
                f_pred = inverse_positivity(self.parameter_state['latent'][0])
                sq_diff = tfm.square(self.data.f_obs - tf.gather(f_pred, self.data.common_indices, axis=2))
                return tf.reduce_sum(sq_diff, axis=0)
            σ2_f = Parameter('σ2_f',
                             tfd.InverseGamma(f64(0.01), f64(0.01)),
                             1e-4*tf.ones((self.num_tfs,1), dtype=self.dtype))
            σ2_f_sampler = GibbsSampler(σ2_f, f_sq_diff_fn, self.N_p)
            self.subsamplers.append(σ2_f_sampler)
        # White noise for genes
        if not options.preprocessing_variance:
            def m_sq_diff_fn():
                m_pred = self.predict_m(**self.parameter_state)
                sq_diff = tfm.square(self.data.m_obs - tf.gather(m_pred, self.data.common_indices, axis=2))
                return tf.reduce_sum(sq_diff, axis=0)
            σ2_m = Parameter('σ2_m', tfd.InverseGamma(f64(0.01), f64(0.01)),
                             1e-3 * tf.ones((self.num_outputs, 1), dtype=self.dtype))
            σ2_m_sampler = GibbsSampler(σ2_m, m_sq_diff_fn, self.N_p)
        else:
            σ2_m = Parameter('σ2_m', LogisticNormal(f64(1e-5), f64(1)),
                             0.7 * tf.ones((self.num_outputs, 1), dtype=self.dtype),
                             transform=logit)
            σ2_m_sampler = HMCSampler(self.likelihood, [σ2_m], logistic_step_size)

        self.subsamplers.append(σ2_m_sampler)

        def iteration_callback(current_state):
            self.parameter_state = current_state

        self.sampler = MixedSampler(self.subsamplers, iteration_callback=iteration_callback)

    def sample(self, T=2000, **kwargs):
        return self.sampler.sample(T, **kwargs)

    @tf.function
    def calculate_protein(self, fbar, protein_decay, delay):  # Calculate p_i vector
        t_discretised = self.data.t_discretised
        f_i = inverse_positivity(fbar)
        δ_i = tf.reshape(protein_decay, (-1, 1))
        if self.options.delays:
            # Add delay
            delay = tf.cast(delay, 'int32')

            for r in range(self.num_replicates):
                f_ir = rotate(f_i[r], -delay)
                mask = ~tf.sequence_mask(delay, f_i.shape[2])
                f_ir = tf.where(mask, f_ir, 0)
                mask = np.zeros((self.num_replicates, 1, 1), dtype=self.dtype)
                mask[r] = 1
                f_i = (1 - mask) * f_i + mask * f_ir

        # Approximate integral (trapezoid rule)
        resolution = t_discretised[1] - t_discretised[0]
        sum_term = tfm.multiply(tfm.exp(δ_i * t_discretised), f_i)
        cumsum = 0.5 * resolution * tfm.cumsum(sum_term[:, :, :-1] + sum_term[:, :, 1:], axis=2)
        integrals = tf.concat([tf.zeros((self.num_replicates, self.num_tfs, 1), dtype=self.dtype), cumsum], axis=2)
        exp_δt = tfm.exp(-δ_i * t_discretised)
        p_i = exp_δt * integrals
        return p_i

    @tf.function
    def predict_m(self,
                  initial, basal, decay, sensitivity,
                  protein_decay, latent, **optional_parameters):
        # tf.print(initial, basal, decay, sensitivity)
        if self.options.kinetic_exponential:
            initial = tf.exp(initial)
            basal = tf.exp(basal)
            decay = tf.exp(decay)
            sensitivity = tf.exp(sensitivity)
        # tf.print('p', initial, basal, decay, sensitivity)
        t_discretised = self.data.t_discretised
        fbar = latent[0]
        p_i = inverse_positivity(fbar)
        if self.options.translation:
            delay = optional_parameters['delay'] if self.options.delays else None
            p_i = self.calculate_protein(fbar, protein_decay, delay)

        # Calculate m_pred
        resolution = t_discretised[1] - t_discretised[0]
        if self.options.weights:
            w = optional_parameters['w']
            w_0 = optional_parameters['w_0']
            interactions = tf.matmul(w, tfm.log(p_i + 1e-100)) + w_0
            G = tfm.sigmoid(interactions)  # TF Activation Function (sigmoid)
        else:
            G = tf.tile(p_i, (1, self.num_outputs, 1))

        sum_term = G * tfm.exp(decay * t_discretised)
        integrals = tf.concat([tf.zeros((self.num_replicates, self.num_outputs, 1), dtype=self.dtype),  # Trapezoid rule
                               0.5 * resolution * tfm.cumsum(sum_term[:, :, :-1] + sum_term[:, :, 1:], axis=2)], axis=2)
        exp_dt = tfm.exp(-decay * t_discretised)
        integrals = tfm.multiply(exp_dt, integrals)

        m_pred = basal / decay + sensitivity * integrals
        if self.options.initial_conditions:
            m_pred += tfm.multiply((initial - basal / decay), exp_dt)
        return m_pred

    @tf.function
    def _genes(self, σ2_m=None, **parameter_state):
        m_pred = self.predict_m(σ2_m=σ2_m, **parameter_state)
        # tf.print('paramstate', parameter_state)
        sq_diff = tfm.square(self.data.m_obs - tf.gather(m_pred, self.data.common_indices, axis=2))

        variance = tf.reshape(σ2_m, (-1, 1))
        # tf.print(variance)
        if self.preprocessing_variance:
            variance = variance + self.data.σ2_m_pre  # add PUMA variance
        log_lik = -0.5 * tfm.log(2 * PI * variance) - 0.5 * sq_diff / variance
        log_lik = tf.reduce_mean(log_lik)
        return log_lik

    @tf.function  # (experimental_compile=True)
    def likelihood(self, **parameters):
        """
        Likelihood of the form:
        N(m(t), s(t))
        where m(t) = b/d + (a - b/d) exp(-dt) + s int^t_0 G(p(u); w) exp(-d(t-u)) du
        """
        parameter_state = {**self.parameter_state, **parameters}
        return self._genes(**parameter_state)

    @tf.function  # (experimental_compile=True)
    def tfs_likelihood(self, **parameters):
        """
        Computes log-likelihood of the transcription factors.
        """
        parameter_state = {**self.parameter_state, **parameters}
        # tf.print(
        #     'param', parameters['latent'],
        #     'self', self.parameter_state['latent'],
        #     'state', parameter_state['latent']
        #  )
        σ2_f = parameter_state['σ2_f']
        latent = parameter_state['latent']

        # assert self.options.tf_mrna_present
        if not self.preprocessing_variance:
            variance = tf.reshape(σ2_f, (-1, 1))
        else:
            variance = self.data.σ2_f_pre
        f_pred = inverse_positivity(latent[0])
        sq_diff = tfm.square(self.data.f_obs - tf.transpose(tf.gather(tf.transpose(f_pred), self.data.common_indices)))
        log_lik = -0.5 * tfm.log(2 * PI * variance) - 0.5 * sq_diff / variance
        log_lik = tf.reduce_sum(log_lik)

        return log_lik

    def sample_proteins(self, results, num_results):
        p_samples = list()
        for i in range(1, num_results + 1):
            delta = results['delay'][i] if results['delay'] is not None else None
            p_samples.append(self.likelihood.calculate_protein(results.fbar[-i],
                                                               results.k_fbar[-i], delta))
        return np.array(p_samples)

    def sample_latents(self, results, num_results, step=1):
        m_preds = list()
        for i in range(1, num_results, step):
            m_preds.append(self.predict_m_with_results(results, i))
        return np.array(m_preds)

    def results(self, burnin=0):
        results = dict()
        for i, subsampler in enumerate(self.subsamplers):
            group_samples = self.sampler.samples[i]
            for j, param in enumerate(subsampler.param_group):
                samples = group_samples[j]
                if type(samples) is list:
                    samples = [s.numpy()[-burnin:] for s in samples]
                else:
                    samples = samples.numpy()[-burnin:]
                results[param.name] = param.transform(samples)

        return results

    def predict_m_with_results(self, results, i=1):
        parameter_state = self.parameter_state
        for key in results:
            result = results[key]
            if type(result) is list:
                parameter_state[key] = [result[0][-1]]
            else:
                parameter_state[key] = result[-1]
        return self.predict_m(**parameter_state)

    def save(self, name):
        save_object({'samples': self.samples, 'is_accepted': self.is_accepted}, f'custom-{name}')

    @staticmethod
    def load(name, args):
        model = TranscriptionRegulationLFM(*args)

        import os
        path = os.path.join(os.getcwd(), 'saved_models')
        fs = [os.path.join(path, f) for f in os.listdir(path) if f.startswith(f'custom-{name}')]
        files = sorted(fs, key=os.path.getmtime)
        with open(files[-1], 'rb') as f:
            saved_model = pickle.load(f)
            model.samples = saved_model['samples']
            model.is_accepted = saved_model['is_accepted']
        for param in model.active_params:
            index = model.state_indices[param.name]
            param_samples = model.samples[index]
            if type(param_samples) is list:
                param_samples = [[param_samples[i][-1] for i in range(len(param_samples))]]

            param.value = param_samples[-1]

        return model

    @staticmethod
    def initialise_from_state(args, state):
        model = TranscriptionRegulationLFM(*args)
        model.is_accepted = state.is_accepted
        model.samples = state.samples
        return model
