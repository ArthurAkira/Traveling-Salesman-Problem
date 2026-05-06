import time

def benchmark(func, grafo):
    start_time = time.time()
    result = func(grafo)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time