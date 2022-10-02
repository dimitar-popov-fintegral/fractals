import time
import ursina as urs
import math
import itertools as iter
import ursina.prefabs.video_recorder as vr
import random
import numpy

env = 32
N = 8
max_iter = 4


def rotate_3d_y(vectors, theta):
    if isinstance(vectors, list):
        vectors = numpy.array(vectors)
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    rotator = numpy.array(
        [[cos_theta, 0, sin_theta],
        [0, 1, 0],
        [-sin_theta, 0, cos_theta]]
    )
    return vectors.dot(rotator)


def rotate_3d_x(vectors, theta):
    if isinstance(vectors, list):
        vectors = numpy.array(vectors)
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    rotator = numpy.array(
        [[1, 0, 0],
         [0, cos_theta, -sin_theta],
         [0, sin_theta, cos_theta]]
    )
    return vectors.dot(rotator)



def inside_fractal(x, y, z) -> bool:
    if z == 0:
        return False
    x, y, z = x/env, y/env, z/env
    for _ in range(max_iter):
        r = (x*x + y*y + z*z) ** 0.5
        if r > 2:
            return False
        theta = math.atan2((x*x + y*y) ** 0.5, z)
        phi = math.atan2(y, x)
        x += r**N * math.sin(theta*N) * math.cos(phi*N)
        y += r**N * math.sin(theta*N) * math.sin(phi*N)
        z += r**N * math.cos(theta*N)
    if not a:
        return True
    return True
    

def input(key):
    if key == '5':
        recorder.start_recording()
    if key == '6':
        recorder.stop_recording()
    if key == '7':
        print("starting")
        seq.start()


if __name__ == "__main__":
    points_a = []
    points_b = []
    for x in range(env):
        scale_x = random.uniform(1,1)
        for y in range(env):
            scale_y = random.uniform(1,1)
            a = False
            for z in range(env):
                scale_z = random.uniform(1,1)
                a = inside_fractal(x, y, z)
                if not a:
                    for x1, x2, x3 in iter.product([-1, 1], repeat=3):
                        if random.uniform(0, 1) > 0.9:
                            points_b.append((x*x1, y*x2, z*x3))
                    continue
                for m1, m2, m3 in iter.product([-1, 1], repeat=3):
                    points_a.append((scale_x * x * m1, scale_y * y * m2, scale_z * z * m3))
    

    app = urs.Ursina()
    urs.window.borderless = False
    urs.window.size = (600, 400)
    urs.window.color = urs.color.white
    e = urs.Entity(
        model=urs.Mesh(
            vertices=points_a,
            mode='point',
            thickness=0.001
        ),
        color=urs.color.gray
    )
    """
    edge = urs.Entity(
        model=urs.Mesh(
            vertices=rotate_3d_y(points_a, 45),
            mode='point',
            thickness=0.01,
        ),
        color=urs.color.light_gray
    )
    """

    def transform(ent, theta, by):
        ent.model.vertices = by(e.model.vertices, theta)
        ent.model.generate()
        time.sleep(0.01)
        return        

        
    seq = urs.Sequence(loop=True)
    seq.append(
        urs.Func(transform, e, theta=12.5, by=rotate_3d_y)
    )
    seq.append(
        urs.Func(transform, e, theta=12.5, by=rotate_3d_x)
    )

    urs.EditorCamera()
    recorder = vr.VideoRecorder(duration=2, fps=90)
    app.run()
