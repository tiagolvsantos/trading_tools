import time

start = time.time()
import inquirer
print(f'inquirer: {time.time() - start} seconds')

start = time.time()
from src.implementation import interactive_impl
print(f'interactive_impl: {time.time() - start} seconds')

start = time.time()
from src.implementation import charts_impl
print(f'charts_impl: {time.time() - start} seconds')

start = time.time()
from src.implementation import tradfi_impl
print(f'tradfi_impl: {time.time() - start} seconds')

start = time.time()
from src.implementation import crypto_impl
print(f'crypto_impl: {time.time() - start} seconds')

start = time.time()
from src.implementation import links_impl
print(f'links_impl: {time.time() - start} seconds')

start = time.time()
from src.implementation import reports_impl
print(f'reports_impl: {time.time() - start} seconds')

start = time.time()
from src.implementation import jobs_impl
print(f'jobs_impl: {time.time() - start} seconds')



#########################################
import cProfile
import pstats

# Profile the import statement
profiler = cProfile.Profile()
profiler.enable()
import src.implementation.charts_impl
profiler.disable()

# Save the stats to a file
profiler.dump_stats("charts_impl_stats")

# Read the stats file and print it
p = pstats.Stats("charts_impl_stats")
p.sort_stats("time").print_stats()