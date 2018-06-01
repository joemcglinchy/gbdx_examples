from gbdxtools import LandsatImage
from skimage import filters
from skimage.filters.rank import entropy
from skimage.morphology import disk
import dask.array as da

img = LandsatImage('LC80370302014268LGN00') 
print img.shape 
aoi = img.aoi(bbox=[-109.84, 43.19, -109.59, 43.34]) 
# print aoi.shape 
# aoi.plot(bands=[3,2,1])

# extract the first band
b1 = aoi[1,:,:]
# b1 = img[1,:,:]
ent_b1 = entropy(b1, disk(5))
ent_da = da.from_array(ent_b1, chunks=(100))


## plot using matplotlib
from matplotlib import pyplot as plt

plt.subplot(1, 2, 1)
plt.imshow(ent_b1)
plt.title('entropy')


plt.subplot(1, 2, 2)
plt.imshow(b1)

plt.show()

