class Point:

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def get_tuple(self):
        return self.lat, self.lon

    def comparar_puntos(self, x):
        return abs(self.lat - x.lat), abs(self.lon - x.lon)

    @staticmethod
    def generar_punto_dict(punto: dict):
        return Point(punto['lat'], punto['lon'])

    @staticmethod
    def generar_lista_puntos(lista: list, inv: bool = False):
        i = 0 if inv else 1
        return [Point(x[i], x[1 - i]) for x in lista]

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.lat == other.lat and self.lon == other.lon

    def __hash__(self):
        return hash(self.lat) ^ hash(self.lon)

    def __repr__(self):
        return "Lat: {} Lon: {}".format(self.lat, self.lon)

    def __lt__(self, other):
        return (self.lat < other.lat and self.lon < other.lon) or ((self.lat - other.lat + self.lon - other.lon) < 0)

    def __add__(self, other):
        if isinstance(self, Point):
            p = Point(self.lat + other.lat, self.lon + other.lon)
        elif len(other) == 2 and (isinstance(other, list) or isinstance(other, tuple)):
            p = Point(self.lat + other[0], self.lon + other[1])
        elif other.get('lat') is not None and other.get('lon') is not None:
            p = Point(self.lat + other['lat'], self.lon + other['lon'])
        else:
            raise Exception(f'Not a point, f{type(other)} detected')
        return p

    def __sub__(self, other):
        if isinstance(self, Point):
            p = Point(self.lat - other.lat, self.lon - other.lon)
        elif len(other) == 2 and (isinstance(other, list) or isinstance(other, tuple)):
            p = Point(self.lat - other[0], self.lon - other[1])
        elif other.get('lat') is not None and other.get('lon') is not None:
            p = Point(self.lat - other['lat'], self.lon - other['lon'])
        else:
            raise Exception(f'Not a point, f{type(other)} detected')
        return p


Punto = Point
