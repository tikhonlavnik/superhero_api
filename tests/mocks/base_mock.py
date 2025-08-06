mock_hero_body = {
    "name": "Batman",
    "powerstats": {
        "intelligence": "100",
        "strength": "80",
        "speed": "70",
        "power": "90",
    },
}


class MockHero:
    def __init__(self):
        self.id = 1
        self.name = "Batman"
        self.intelligence = 81
        self.strength = 40
        self.speed = 29
        self.power = 63

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "intelligence": self.intelligence,
            "strength": self.strength,
            "speed": self.speed,
            "power": self.power,
        }


class MockRepo:
    async def get_list(self, filters):
        return [MockHero()]

    async def create(self, data):
        return type(
            "obj",
            (object,),
            {
                "id": 1,
                "name": "Batman",
                "to_dict": lambda self: {
                    "id": 1,
                    "name": "Batman",
                    "intelligence": 100,
                    "strength": 80,
                    "speed": 70,
                    "power": 90,
                },
            },
        )()


class MockRepoFailed:
    async def get_list(self, filters):
        return []


class MockApiService:
    async def get_hero_data(self, name: str = "Some name"):
        return {
            "id": "69",
            "name": "Batman",
            "powerstats": {
                "intelligence": "81",
                "strength": "40",
                "speed": "29",
                "durability": "55",
                "power": "63",
                "combat": "90",
            },
        }


class MockApiServiceFailed:
    async def get_hero_data(self, name: str):
        return None
