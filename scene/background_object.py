from .scene_object import SceneObject


class BackgroundObject(SceneObject):
    def __init__(self, scene, position: list[int, int] | tuple[int, int], image: str) -> None:
        super().__init__(scene, position, image, image)

    def collide_shadow(self, other_object: SceneObject) -> bool:
        return False
