import pymunk
import pygame

class Ragdoll:
    def __init__(self, space, x, y):
        self.bodies = []
        self.shapes = []
        self.constraints = []

        # Create basic parts
        self.head = pymunk.Body(1, 100)
        self.head.position = (x, y)
        self.head_shape = pymunk.Circle(self.head, 20)
        space.add(self.head, self.head_shape)

        self.torso = pymunk.Body(1, 100)
        self.torso.position = (x, y + 50)
        self.torso_shape = pymunk.Segment(self.torso, (0, -30), (0, 30), 5)
        space.add(self.torso, self.torso_shape)

        # Constraint: head <-> torso
        neck_joint = pymunk.PinJoint(self.head, self.torso, (0, 20), (0, -30))
        space.add(neck_joint)

        self.bodies += [self.head, self.torso]
        self.shapes += [self.head_shape, self.torso_shape]
        self.constraints += [neck_joint]

    def draw(self, screen):
        for shape in self.shapes:
            if isinstance(shape, pymunk.Circle):
                pos = shape.body.position
                pygame.draw.circle(screen, (255, 224, 189), (int(pos[0]), int(pos[1])), int(shape.radius))
            elif isinstance(shape, pymunk.Segment):
                a = shape.body.position + shape.a.rotated(shape.body.angle)
                b = shape.body.position + shape.b.rotated(shape.body.angle)
                pygame.draw.line(screen, (0, 0, 0), (int(a.x), int(a.y)), (int(b.x), int(b.y)), int(shape.radius * 2))
