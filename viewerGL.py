#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
import time
from cpe3d import Object3D
import random as random

class ViewerGL:
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(1600, 900, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.touch = {}

    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()
            #self.colision()

            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                obj.draw()
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action
    
    def add_object(self, obj):
        self.objs.append(obj)

    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)
    

    def update_key(self):
        # commace joueur 
        if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0 and self.objs[0].transformation.translation.y < 4: # monter
            # tm = 1000
            # td = 1000
            # for i in range(tm):
            #     self.objs[0].transformation.translation += \
            #         pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0.2, 0]))
            # time.sleep(1)
            # for i in range(td):
            #     self.objs[0].transformation.translation -= \
            #         pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0.2, 0]))
            self.objs[0].transformation.translation += \
                 pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0.25, 0]))
        if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0 and self.objs[0].transformation.translation.y >1: # descendre
            self.objs[0].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0.25, 0]))
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0: # gauche
            self.objs[0].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.125, 0, 0]))
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0: # droite
            self.objs[0].transformation.translation -= \
                 pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.125, 0, 0]))

#commande dev
        if glfw.KEY_W in self.touch and self.touch[glfw.KEY_W] > 0:
            self.objs[0].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.25]))
        if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0:
            self.objs[0].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.25]))
        if glfw.KEY_A in self.touch and self.touch[glfw.KEY_A] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        if glfw.KEY_D in self.touch and self.touch[glfw.KEY_D] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1

        if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
        if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1
        if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1

        # movement du personnage vers l'avant
        # self.objs[0].transformation.translation += \
        #     pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.1]))
        
        # gestion de la caméra
        self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
        self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 5])

        # gestion des plateau1
        if self.objs[0].transformation.translation.z - self.objs[-3].transformation.translation.z > 25:
            self.objs[-3].transformation.translation.z += 150
        # gestion des plateau2
        if self.objs[0].transformation.translation.z - self.objs[-2].transformation.translation.z > 25:
            self.objs[-2].transformation.translation.z += 150
        # gestion des plateau3
        if self.objs[0].transformation.translation.z - self.objs[-1].transformation.translation.z > 25:
            self.objs[-1].transformation.translation.z +=  150
                   
        # gestion mur
        for i in range(241):
            if self.objs[0].transformation.translation.z - self.objs[i].transformation.translation.z > 25:
                self.objs[i].transformation.translation.z += 80
        #collision mur
        print(self.objs[0].transformation.translation.x)
        if self.objs[0].transformation.translation.x <= -2.25:
            self.objs[0].transformation.translation.x = -2.25
        elif self.objs[0].transformation.translation.x >= 2.25:
            self.objs[0].transformation.translation.x = 2.25

        #movement obstacle
        for i in range(241,246):
            if self.objs[0].transformation.translation.z - self.objs[i].transformation.translation.z > 25:
                self.objs[i].transformation.translation.z += 50 + random.randint(-1, 1)

                if 0 < self.objs[i].transformation.translation.y < 4 and self.objs[i].transformation.translation.y != self.objs[i-1].transformation.translation.y:
                    self.objs[i].transformation.translation.y += random.randint(-1, 1)
                elif self.objs[i].transformation.translation.y == 4 and self.objs[i].transformation.translation.y != self.objs[i-1].transformation.translation.y:
                   self.objs[i].transformation.translation.y += -random.randint(0, 4)
                elif self.objs[i].transformation.translation.y == 0 and self.objs[i].transformation.translation.y != self.objs[i-1].transformation.translation.y:
                    self.objs[i].transformation.translation.y += random.randint(0, 4)
                   
                if -3 < self.objs[i].transformation.translation.x < 3 and self.objs[i].transformation.translation.y != self.objs[i-1].transformation.translation.y:
                    self.objs[i].transformation.translation.x += random.randint(-1, 1)
                elif self.objs[i].transformation.translation.x == 3 and self.objs[i].transformation.translation.y != self.objs[i-1].transformation.translation.y:
                   self.objs[i].transformation.translation.x += -1
                elif self.objs[i].transformation.translation.x == -3 and self.objs[i].transformation.translation.y != self.objs[i-1].transformation.translation.y:
                   self.objs[i].transformation.translation.x += 1
                   
        #collision obstacle
        for i in range(241,246):
            if self.objs[0].transformation.translation.z == self.objs[i].transformation.translation.z and self.objs[0].transformation.translation.y == self.objs[i].transformation.translation.y and self.objs[0].transformation.translation.x == self.objs[i].transformation.translation.x:
                self.objs[0].transformation.translation.x = self.objs[i].transformation.translation.x
                self.objs[0].transformation.translation.y = self.objs[i].transformation.translation.y
                self.objs[0].transformation.translation.z = self.objs[i].transformation.translation.z
        print("x",self.objs[242].transformation.translation.x)
        print("y",self.objs[242].transformation.translation.y)
