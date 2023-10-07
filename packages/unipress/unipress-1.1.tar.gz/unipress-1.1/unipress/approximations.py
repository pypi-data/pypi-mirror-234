#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################### 
#   Copyright 2023 Konrad Sakowski
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
####################################################################################
#
"""
	This module contains approximations.
"""

import numpy
import scipy.integrate

def tau_scoul1(theta, gamma, tau_srh):
	"""
		This is an approximation of the Shockley-Read-Hall recombination capture time accounting for the attraction of the minority carrier by the Coulomb force.

		Parameters:

		* *theta* --- capture length to Coulomb length ratio; a number
		* *gamma* --- Coulomb length to screening distance ratio; a number
		* *tau_srh* --- original SRH parameter, without Coulomb force accounted for

		This procedure approximates is supposed to give quite values with the precision of 35\% for parameters *theta* and *gamma* within range [0.01, 100]. Outside this integral, the approximation may be highly inaccurate.

		Return: Shockley-Read-Hall recombination capture time accounting for thee attraction of the minority carrier by the Coulomb force
	"""
	
	loggamma = numpy.log(gamma);
	P1 = 0.949 + 0.049 * loggamma;
	P2 = 0.861 - 0.169 * loggamma;
	P3 = 0.475 + 0.005327 * loggamma + 0.001699 * loggamma**2;
	
	thetaP1 = theta**P1;
	
	return tau_srh * ( thetaP1 / (thetaP1 + P2) )**P3;


def tau_scoul2(theta, gamma, tau_srh):
	"""
		This is an approximation of the Shockley-Read-Hall recombination capture time accounting for the attraction of the minority carrier by the Coulomb force.

		Parameters:

		* *theta* --- capture length to Coulomb length ratio; a number
		* *gamma* --- Coulomb length to screening distance ratio; a number
		* *tau_srh* --- original SRH parameter, without Coulomb force accounted for

		This procedure shall work for any positive *theta* and *gamma*.
		However, it relies on a numerical quadrature.
		If the quadrature fails, the results will be inaccurate.

		Return: Shockley-Read-Hall recombination capture time accounting for thee attraction of the minority carrier by the Coulomb force
	"""
	podc = lambda y: numpy.sqrt(1 / (1 - numpy.exp(-gamma*theta)/theta + numpy.exp(-gamma*theta*y)/(y*theta) ) );

	return tau_srh * scipy.integrate.quad(podc, 0, 1)[0];


