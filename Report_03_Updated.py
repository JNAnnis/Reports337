# -*- coding: utf-8 -*-

"""
Report 3: Mauna Loa Carbon Dioxide Levels

Since March 1958, the average monthly mol fractions of CO2 present in the
atmosphere have been measured at the NOAA Mauna Loa Observatory and are made
available to the public.

Note: Mol fraction = # of CO2 molecules per 1,000,000 of dry air = parts per
million (ppm)

Data used is the Mauna Loa CO2 monthly mean data available at
esrl.noaa.gov/gmd/ccgg/trends/data/html
"""

import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
from scipy import stats


# Load in the data
data = np.loadtxt('co2_mm_mlo.txt', skiprows = 72)
year = data[:,2]
co2 = data[:,4]


#Plot the data
plt.figure(figsize = (12, 8))
plt.plot(year, co2, color = 'blue')

plt.title(r'Mauna Loa Mean Monthly $CO_2$ Levels', fontsize = 22)
plt.xlabel('Year', fontsize = 18, labelpad = 20)
plt.ylabel('$CO_2$ Level (ppm)', fontsize = 18, labelpad = 20)

ax1 = plt.gca()
ax1.tick_params(axis = 'both', labelsize = 14)


# Linear regression with plot
slope, intercept, rValue, pValue, stdErr = stats.linregress(year, co2)
linReg = intercept + slope*year

plt.figure(figsize = (12, 8))
plt.plot(year, co2, color = 'blue')
plt.plot(year, linReg, color = 'darkorange')

plt.title('Linear Regression', fontsize = 22)
plt.xlabel('Year', fontsize = 18, labelpad = 20)
plt.ylabel('$CO_2$ Level (ppm)', fontsize = 18, labelpad = 20)

ax2 = plt.gca()
ax2.tick_params(axis = 'both', labelsize = 14)

print('The r value for the linear regression is', rValue, '\n')


# Plot the linear regression residuals
linResid = co2 - linReg

plt.figure(figsize = (12, 8))
plt.plot(year, linResid, color = 'darkgreen', marker = '.', ls = 'none')

plt.title('Linear Regression Residuals', fontsize = 22)
plt.xlabel('Year', fontsize = 18)
plt.ylabel('Residual', fontsize = 18)

ax3 = plt.gca()
ax3.tick_params(axis = 'both', labelsize = 14)


# Quadratic Regression
coeff2, stats2 = poly.polyfit(year, co2, 2, full = True)
quadFit = poly.polyval(year, coeff2)
resid2 = stats2[0]

# Cubic Regression
coeff3, stats3 = poly.polyfit(year, co2, 3, full = True)
cubeFit = poly.polyval(year, coeff3)
resid3 = stats3[0]

# Quartic Regression
coeff4, stats4 = poly.polyfit(year, co2, 4, full = True)
quartFit = poly.polyval(year, coeff3)
resid4 = stats4[0]


# Compare the polynomial regressions graphically
plt.figure(figsize = (16, 8))
plt.subplots_adjust(wspace = 0.5)

plt.subplot(131)
plt.plot(year, co2, color = 'gray', label = 'Data')
plt.plot(year, quadFit, '-', color = 'red', linewidth = 2, label = 'Quad-Reg')

plt.title('Quadratic Regression', fontsize = 20)
plt.xlabel('Year', fontsize = 18)
plt.ylabel('$CO_2$ Level (ppm)', fontsize = 18, labelpad = 10)
plt.legend()

plt.subplot(132)
plt.plot(year, co2, color = 'gray', label = 'Data')
plt.plot(year, cubeFit, '-', color = 'green', linewidth = 2, label = 'Cubic-Reg')

plt.title('Cubic Regression', fontsize = 20)
plt.xlabel('Year', fontsize = 18)
plt.ylabel('$CO_2$ Level (ppm)', fontsize = 18, labelpad = 10)
plt.legend()

plt.subplot(133)
plt.plot(year, co2, color = 'gray', label = 'Data')
plt.plot(year, quartFit, '-', color = 'blue', linewidth = 2, label = 'Quart-Reg')

plt.title('Quartic Regression', fontsize = 20)
plt.xlabel('Year', fontsize = 18)
plt.ylabel('$CO_2$ Level (ppm)', fontsize = 18, labelpad = 10)
plt.legend()


# Print the residuals to see if higher polynomial is a better fit
print('Sum of squared residuals:')
print('Quadratic:', resid2[0])
print('Cubic:', resid3[0])
print('Quartic:', resid4[0])
print('\n')


# Predict the CO2 levels for each model at years 2050 and 2100
# Quadratic
quad50 = coeff2[0] + coeff2[1]*2050 + coeff2[2]*2050**2
quad100 = coeff2[0] + coeff2[1]*2100 + coeff2[2]*2100**2

# Cubic
cube50 = coeff3[0] + coeff3[1]*2050 + coeff3[2]*2050**2 + coeff3[3]*2050**3
cube100 = coeff3[0] + coeff3[1]*2100 + coeff3[2]*2100**2 + coeff3[3]*2100**3

# Quartic
quart50 = coeff4[0] + coeff4[1]*2050 + coeff4[2]*2050**2 + coeff4[3]*2050**3 + coeff4[4]*2050**4
quart100 = coeff4[0] + coeff4[1]*2100 +coeff4[2]*2100**2 + coeff4[3]*2100**3 + coeff4[4]*2100**4

print("{}\t{}\t{}\t{}".format('Year', 'Quad', 'Cubic', 'Quartic'))
print("{}\t{:.2f}\t{:.2f}\t{:.2f}".format('2050', quad50, cube50, quart50))
print("{}\t{:.2f}\t{:.2f}\t{:.2f}".format('2050', quad100, cube100, quart100))


# Analyze the seasonal variation
# Done with quartic model only since it had the best fit (smallest resid)
quartResid = co2 - quartFit
month = data[:,1]
monthName = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 
             'Oct', 'Nov', 'Dec']

# Calculate the mean monthly residuals for the quartic fit
meanMonthly = [np.mean(quartResid[month==i]) for i in range(1, 13)]

# Plot the quartic residuals and the corresponding mean monthly residual
plt.figure(figsize = (12, 8))

plt.plot(np.arange(1, 13), meanMonthly, color = 'orangered', label = 'Mean Monthly')
plt.scatter(month, quartResid, color = 'darkblue', marker = '.', label = 'Residual')

plt.xlim(0, 13)
plt.xticks(np.arange(1, 13), labels = monthName)

plt.title('Mean Monthly Residual vs. Month', fontsize = 20)
plt.xlabel('Month', fontsize = 16, labelpad = 20)
plt.ylabel('Residual', fontsize = 16, labelpad = 20)
plt.legend()

ax4 = plt.gca()
ax4.tick_params(axis = 'both', labelsize = 14)
