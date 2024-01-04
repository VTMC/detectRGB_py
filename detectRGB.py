import rawpy
import imageio

path = "E:/VTMC_GitHub/StoredProject_LibRaw_0.21.2/StoredProject_LibRaw_0.21.2/LibRaw-0.21.2/testFile/test_A80.dng"
# path = "E:/VTMC_GitHub/StoredProject_LibRaw_0.21.2/StoredProject_LibRaw_0.21.2/LibRaw-0.21.2/testFile/test_A80_averageWhiteBalanced.tiff"

with rawpy.imread(path) as rp:
    rgb = rp.postprocess() #gamma=(1,1), no_auto_bright=True, output_bps=16
    print(len(rgb))
    print(rgb)

# Extract each R,G,B Channels to save Separately
r = rgb[:,:,0]
g = rgb[:,:,1]
b = rgb[:,:,2]

# Save each R,G,B Channels Separately
imageio.imsave(path + "_r.tiff", r)
imageio.imsave(path + "_g.tiff", g)
imageio.imsave(path + "_b.tiff", b)

#imageio.imsave(path + ".jpg", rgb)
