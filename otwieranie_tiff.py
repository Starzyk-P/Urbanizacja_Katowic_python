import rasterio
import matplotlib.pyplot as plt


with rasterio.open('**') as src:
    img = src.read(1)

plt.imshow(img, cmap='gray')
plt.colorbar()
plt.show()