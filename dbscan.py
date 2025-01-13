import pygame
import numpy as np


def dist(pointA, pointB):
    return np.sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)

def drawing():
    """Основной цикл программы, позволяющий рисовать точки, запускать DBSCAN и отображать результаты."""
    points = []  
    pygame.init()  
    screen = pygame.display.set_mode((600, 400))  
    screen.fill((255, 255, 255))  
    pygame.display.update()  
    last_coordinates = (0, 0) 
    running = True  
    is_drawing = False  
    result = [] 
    
    while running:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False  
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    is_drawing = True  
            if event.type == pygame.MOUSEBUTTONUP: 
                is_drawing = False  
            if is_drawing:  
                coordinates = pygame.mouse.get_pos() 
                if dist(coordinates, last_coordinates) > 5:  
                    last_coordinates = coordinates  
                    points.append(coordinates)  
                    pygame.draw.circle(screen, (0, 0, 255), coordinates, 5)  
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    result = dbScan(points, 30, 2)  # Кластеризация точек с радиусом 30 и минимальным числом соседей 2
                    # Отображение точек с их флажками (зеленые, желтые, красные)
                    show_color_points(result[1], result[2], result[3], screen) 
                if event.key == pygame.K_a: 
                    show_cluster_points(result[0], screen)  
                if event.key == pygame.K_ESCAPE: 
                    screen.fill((255, 255, 255))  
                    points = [] 
            
            pygame.display.update()  
    pygame.quit() 
    return points 


# Функция поиска соседей для заданной точки
def find_neighbors(radius, center, points):
    return [point for point in points if 0 < dist(center, point) < radius]  # Возвращает список точек-соседей

def dbScan(points, radius, min_neighbors):
    green_points = []  # Основные точки (Core Points)
    yellow_points = []  # Граничные точки (Border Points)
    red_points = []  # Шумовые точки (Noise Points)
    points_with_clusters = []  # Список точек с номерами кластеров

    visited_points = set()  # Множество для отслеживания посещенных точек
    clusters = {}  # Словарь для хранения кластеров
    cluster_id = 0  # Текущий номер кластера

    # Обрабатываем каждую точку
    for point in points: 
        if point in visited_points:  # Пропускаем, если точка уже обработана
            continue

        neighbors = find_neighbors(radius, point, points)  
        if len(neighbors) >= min_neighbors:  
            cluster_id += 1  # Увеличиваем номер текущего кластера
            clusters[cluster_id] = []  # Создаем новый кластер
            green_points.append(point)  # Отмечаем точку как Core Point
            points_with_clusters.append((point, cluster_id))  # Добавляем точку с номером кластера
            clusters[cluster_id].append(point)  # Добавляем точку в кластер
            visited_points.add(point)  # Помечаем точку как посещенную

            # Расширение кластера
            queue = neighbors.copy()  # Создаем очередь из соседей
            while queue: # Пока в очереди есть элементы
                neighbor = queue.pop(0)  # Извлекаем соседа из очереди
                if neighbor not in visited_points:  # Если сосед еще не посещен
                    visited_points.add(neighbor)  # Помечаем соседа как посещенного
                    sub_neighbors = find_neighbors(radius, neighbor, points)  # Ищем его соседей
                    if len(sub_neighbors) >= min_neighbors:  # Если соседей достаточно для кластера
                        green_points.append(neighbor)  # Отмечаем точку как Core Point
                        queue.extend(sub_neighbors)  # Добавляем их в очередь
                    else: # Если сосед является Border Point
                        yellow_points.append(neighbor)  # Иначе это Border Point
                    # Привязываем соседа к текущему кластеру
                    points_with_clusters.append((neighbor, cluster_id))  # Добавляем точку в текущий кластер
                    clusters[cluster_id].append(neighbor)  # Добавляем соседа в кластер
        else: # Если точка не попала в кластер
            red_points.append(point)  # Если соседей недостаточно, это Noise Point
            visited_points.add(point)  # Помечаем точку как посещенную

    return points_with_clusters, green_points, yellow_points, red_points  # Возвращаем результаты


def show_color_points(green_points, yellow_points, red_points, screen):
    """Отображение точек с учетом их флажков (зеленый, желтый, красный)."""
    screen.fill((255, 255, 255))  
    for point in green_points:
        pygame.draw.circle(screen, (0, 255, 0), point, 5)  
    for point in yellow_points:
        pygame.draw.circle(screen, (255, 255, 0), point, 5) 
    for point in red_points:
        pygame.draw.circle(screen, (255, 0, 0), point, 5) 
    pygame.display.update()  


def show_cluster_points(points_with_clusters, screen):
    """Отображение точек с учетом кластеров."""
    screen.fill((255, 255, 255))  
    cluster_colors = {}  

    for point, cluster_id in points_with_clusters: 
        if cluster_id not in cluster_colors:  
            cluster_colors[cluster_id] = (
                np.random.randint(0, 255), 
                np.random.randint(0, 255),
                np.random.randint(0, 255),
            )
        pygame.draw.circle(screen, cluster_colors[cluster_id], point, 5) 
    pygame.display.update() 


if __name__ == "__main__":
    drawing() 
