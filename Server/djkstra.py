import math
import heapq
# Calculate Euclidean distance between two points
def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
def dijkstra(start, end, obstacles):
    graph = {}  # The graph representation with coordinates as keys
    distances = {}  # Distances from start to each node
    previous = {}  # Previous node in the optimal path
    priority_queue = []  # Priority queue for Dijkstra's algorithm

    # Build the graph
    graph[start] = []  # Initialize the graph with the start node
    graph[end] = []  # Include the end node in the graph
    for point, _ in distances.items():
        if point != start:
            graph[point] = []  # Initialize the graph with other points

    # Add connections between neighboring points, excluding obstacles
    for point1 in graph:
        for point2 in graph:
            if point1 != point2 and point1 not in obstacles and point2 not in obstacles:
                graph[point1].append(point2)

    # Initialize distances to infinity for all nodes except start
    for point in graph:
        distances[point] = math.inf
    distances[start] = 0

    # Add the start node to the priority queue
    heapq.heappush(priority_queue, (distances[start], start))

    while priority_queue:
        current_distance, current_point = heapq.heappop(priority_queue)

        # If we have reached the end point, reconstruct the path and return it
        if current_point == end:
            path = []
            while current_point in previous:
                path.insert(0, current_point)
                current_point = previous[current_point]
            path.insert(0, start)
            return path

        for neighbor in graph[current_point]:
            distance_to_neighbor = distances[current_point] + distance(current_point, neighbor)

            # If a shorter path to the neighbor is found, update the distance and previous node
            if distance_to_neighbor < distances[neighbor]:
                distances[neighbor] = distance_to_neighbor
                previous[neighbor] = current_point
                heapq.heappush(priority_queue, (distance_to_neighbor, neighbor))

    # No path found
    return None

# Example usage
start_point = (0.0, 0.0)
end_point = (5.0, 5.0)
obstacle_points = [(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]

obstacles = [tuple(point) for point in obstacle_points]  # Convert obstacle points to tuples

path = dijkstra(start_point, end_point, obstacles)
print("Shortest path from", start_point, "to", end_point, ":")
print(path)
