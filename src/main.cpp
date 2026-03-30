#include <iostream>
#include <vector>
#include "core/Vec2.h"
#include "core/RigidBody.h"

int main() {
    std::cout << "Physics Engine v0.1\n";
    std::cout << "====================\n\n";
    
    // Create a falling sphere
    RigidBody sphere(1.0, 0.8);  // mass 1kg, restitution 0.8
    sphere.position = Vec2(0, 10);
    sphere.velocity = Vec2(2, 0);
    
    Vec2 gravity(0, -9.81);
    
    // Simulate for 2 seconds
    double dt = 0.01;
    for (double t = 0; t < 2.0; t += dt) {
        sphere.applyForce(gravity);
        sphere.integrate(dt);
        
        std::cout << "t = " << t << " | pos: (" 
                  << sphere.position.x << ", " 
                  << sphere.position.y << ") | vel: ("
                  << sphere.velocity.x << ", "
                  << sphere.velocity.y << ")\n";
    }
    
    return 0;
}
