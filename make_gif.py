import os
import imageio
images = []
filenames = sorted(f for f in os.listdir() if f.endswith('.png'))

for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('output_movie.gif', images, duration=0.2)
