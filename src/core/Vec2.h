#pragma once
#include <cmath>

struct Vec2 {
    double x, y;
    
    Vec2(double x = 0, double y = 0) : x(x), y(y) {}
    
    Vec2 operator+(const Vec2& other) const { return Vec2(x + other.x, y + other.y); }
    Vec2 operator-(const Vec2& other) const { return Vec2(x - other.x, y - other.y); }
    Vec2 operator*(double scalar) const { return Vec2(x * scalar, y * scalar); }
    Vec2 operator/(double scalar) const { return Vec2(x / scalar, y / scalar); }
    
    Vec2& operator+=(const Vec2& other) { x += other.x; y += other.y; return *this; }
    Vec2& operator-=(const Vec2& other) { x -= other.x; y -= other.y; return *this; }
    
    double dot(const Vec2& other) const { return x * other.x + y * other.y; }
    double magnitude() const { return std::sqrt(x*x + y*y); }
    double magnitudeSquared() const { return x*x + y*y; }
    
    Vec2 normalized() const { 
        double mag = magnitude(); 
        return mag > 0 ? Vec2(x/mag, y/mag) : Vec2(0, 0); 
    }
};
