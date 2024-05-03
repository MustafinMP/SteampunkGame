from scene.scene import Scene
import json
import os


def load_game_container(filename: str) -> dict:
    file = open(filename)
    container = json.load(file)
    file.close()
    return container


class ProgressStorage:
    @staticmethod
    def save_progress(scene: Scene) -> None:
        location_name: str = scene.location_name
        player_position: list[int, int] = scene.player.game_position
        data = {
            'location_name': location_name,
            'player_position': player_position
        }
        i = 0
        fullname = os.path.join('data/save_containers', f'container{0}.json')
        while os.path.isfile(fullname):
            i += 1
            fullname = os.path.join('data/save_containers', f'container{i}.json')
        with open(fullname, "w") as file:
            json.dump(data, file)

    @staticmethod
    def load_progress(game, container_filename: str) -> Scene:
        container: dict = load_game_container(container_filename)
        location_name: str = container['location_name']
        player_position: list[int, int] = container['player_position']
        widget = Scene(game, location_name, player_position)
        return widget

    @staticmethod
    def last_container() -> str:
        i = 0
        fullname = os.path.join('data/save_containers', f'container{i}.json')
        while os.path.isfile(fullname):
            i += 1
            fullname = os.path.join('data/save_containers', f'container{i}.json')
        fullname = os.path.join('data/save_containers', f'container{i - 1}.json')
        return fullname

    @staticmethod
    def have_containers() -> bool:
        return os.path.isfile(os.path.join('data/save_containers', 'container0.json'))
