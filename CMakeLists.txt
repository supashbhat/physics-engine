cmake_minimum_required(VERSION 3.15)
project(PhysicsEngine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Collect all source files
file(GLOB_RECURSE SRC_FILES "src/*.cpp")

add_executable(physics_engine ${SRC_FILES})

# If you want to add tests later
enable_testing()
# add_executable(tests tests/test_integrators.cpp)
# target_link_libraries(tests physics_engine)
