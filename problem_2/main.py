#! /bin/python

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.backends.backend_pdf import PdfPages
from scipy.fftpack import fft2, fftshift, ifft2
from scipy import ndimage

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

def make_kernel(periodogram, delta):

    if (delta < 0 or delta > 1):
        print("error")
        pass

    thresold = np.percentile(periodogram, 100*delta)

    kernel = np.ones(shape = periodogram.shape)
    kernel[periodogram < thresold] = 0

    return kernel

def residuals(original_img, corrupted_img):
    differense = original_img - corrupted_img
    abs_differense = np.sqrt(np.sum(differense*np.conj(differense)))

    norm = np.sqrt(np.sum(original_img*np.conj(original_img)))

    return (abs_differense/norm).real


# open as array 
img = Image.open('123.jpg')
 
# convert to numpy array
img = np.asarray(img)
#convert to gray colormap
img = (0.30*img[:, :, 0] + 0.59*img[:, :, 1] + 0.11*img[:, :, 2])

fourier_img = fft2(img)
original_img = ifft2(fourier_img)

periodogram = (fourier_img*np.conj(fourier_img)).real


corrupted_imgs = []
parts = []

for delta in np.linspace(0, .99999, 100):
    kernel = make_kernel(periodogram, delta)

    parts.append(delta)
    corrupted_imgs.append(ifft2(fourier_img*kernel))



fig1 = plt.figure()

plt.rcParams['image.cmap'] = 'gray' 
plt.axis('off')
plt.imshow(img)


fig2 = plt.figure()

plt.rcParams['image.cmap'] = 'gray' 
plt.axis('off')
plt.imshow(np.abs(fourier_img.real), norm=colors.LogNorm())


residuals_list = []

for num, img in enumerate(corrupted_imgs):

    residual = residuals(img, original_img)

    residuals_list.append(residual)

    plt.figure()

    plt.rcParams['image.cmap'] = 'gray' 
    plt.axis('off')

    plt.text(10, 50, f"del part: {parts[num]*100}%")
    plt.text(10, 80, f"residuals: {residual}")

    plt.imshow(img.real)




plt.figure()

plt.title("Residuals vs part of fourier coefficients")
plt.xlabel("Part of deleted fourier coefficients, %")
plt.ylabel("Residuals")
plt.grid(visible = True)


plt.gca().invert_xaxis()
plt.axis('on')
plt.xscale('log')

plt.plot(parts, residuals_list)


save_image("images.pdf")
