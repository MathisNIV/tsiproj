from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
import random 

def main():
    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    m = Mesh.load_obj('among.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -5
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('amongt.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)
    
    
    #chargement texture mur
    m = Mesh.load_obj('mur.obj')
    m.normalize()
    texture = glutils.load_texture('murv2.png')
    vao = m.load_to_gpu()
    
    #mur droite
    for i in range(40):
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]
        tr.translation.z = -24+2*i
        tr.translation.x = +4
        tr.rotation_center.z = 0.2
        o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)
    for j in range(40):
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]+2
        tr.translation.z = -24+2*j
        tr.translation.x = +4
        tr.rotation_center.z = 0.2
        o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)
    for j in range(40):
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]+4
        tr.translation.z = -24+2*j
        tr.translation.x = +4
        tr.rotation_center.z = 0.2
        o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)

    #mur gauche
    for i in range(40):
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]
        tr.translation.z = -24+2*i
        tr.translation.x = -4
        tr.rotation_center.z = 0.2
        o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)
    for j in range(40):
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]+2
        tr.translation.z = -24+2*j
        tr.translation.x = -4
        tr.rotation_center.z = 0.2
        o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)
    for j in range(40):
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]+4
        tr.translation.z = -24+2*j
        tr.translation.x = -4
        tr.rotation_center.z = 0.2
        o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)

    #obstacle
    for j in range(5):
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1] + random.randint(0, 4)
        tr.translation.z = 2*j + random.randint(0, 24)
        tr.translation.x = random.randint(-3, 3)
        tr.rotation_center.z = 0.2
        o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)
        
    #plan sol
    m = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('pavé.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D(translation=pyrr.Vector3([0, 0, 50])))
    viewer.add_object(o)
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D(translation=pyrr.Vector3([0, 0, 100])))
    viewer.add_object(o)

    """ vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('Bonjour les', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    o = Text('3ETI', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o) """

    viewer.run()


if __name__ == '__main__':
    main()