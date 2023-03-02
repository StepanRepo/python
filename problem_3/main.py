#! /bin/python

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.backends.backend_pdf import PdfPages
from scipy.fftpack import fft2, ifft2, fftshift, ifftshift

def save_image(filename):
	# PdfPages is a wrapper around pdf
	# file so there is no clash and create
	# files with no error.
    with PdfPages(filename) as p:

        # get_fignums Return list of existing
        # figure numbers
        fig_nums = plt.get_fignums()
        figs = [plt.figure(n) for n in fig_nums]

        # iterating over the numbers in list
        for fig in figs:

            # and saving the files
            fig.savefig(p, format='pdf', bbox_inches='tight', pad_inches = 0)




# open as array 
hdu_list = fits.open("noised.fits")
 
# convert to numpy array
img = np.asarray(hdu_list[0].data)

hdu_list.close()


fourier_img = fft2(img)


abs_f = fftshift((fourier_img*np.conj(fourier_img)).real)

fourier_img = fftshift(fourier_img)
fourier_img[804, 881] = 0
fourier_img[834, 911] = 0
fourier_img = ifftshift(fourier_img)



original_img = ifft2(fourier_img).real




fig1 = plt.figure()

plt.axis('off')
plt.imshow(img, norm=colors.LogNorm(), cmap = "gray")


fig2 = plt.figure()

plt.axis('off')
plt.imshow(abs_f, norm=colors.LogNorm())
plt.gca().invert_yaxis()

fig3 = plt.figure()

plt.axis('off')
plt.imshow(original_img, norm=colors.LogNorm(), cmap = "gray")


save_image("images.pdf")
#plt.show()
